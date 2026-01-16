from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Organization, Team, Membership, Role, User
from app.schemas import OrgCreate, OrgOut, TeamCreate, TeamOut, MembershipCreate, MembershipOut
from app.auth import require_api_key, require_org_role
from app.audit import write_audit

router = APIRouter(prefix="/orgs", tags=["orgs"])


@router.post("", response_model=OrgOut)
def create_org(
    payload: OrgCreate,
    request: Request,
    db: Session = Depends(get_db),
    auth_user: User = Depends(require_api_key),
):
    org = Organization(name=payload.name.strip())
    db.add(org)
    db.commit()
    db.refresh(org)

    m = Membership(
        user_id=auth_user.id,
        org_id=org.id,
        team_id=None,
        role=Role.OWNER,
        is_active=True,
    )
    db.add(m)
    db.commit()

    write_audit(
        db,
        event_type="org.created",
        actor_user_id=auth_user.id,
        org_id=org.id,
        target_type="org",
        target_id=org.id,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        payload={"name": org.name},
    )
    return org



@router.post("/{org_id}/teams", response_model=TeamOut)
def create_team(
    org_id: int,
    payload: TeamCreate,
    request: Request,
    db: Session = Depends(get_db),
    auth_user: User = Depends(require_api_key),
):
    require_org_role(db, auth_user.id, org_id, min_role=Role.ADMIN)

    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Org not found")

    team = Team(org_id=org_id, name=payload.name.strip())
    db.add(team)
    db.commit()
    db.refresh(team)

    write_audit(
        db,
        event_type="team.created",
        actor_user_id=auth_user.id,
        org_id=org_id,
        team_id=team.id,
        target_type="team",
        target_id=team.id,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        payload={"name": team.name},
    )
    return team

@router.post("/{org_id}/members", response_model=MembershipOut)
def add_member(
    org_id: int,
    payload: MembershipCreate,
    request: Request,
    db: Session = Depends(get_db),
    auth_user: User = Depends(require_api_key),
):
    require_org_role(db, auth_user.id, org_id, min_role=Role.ADMIN)


    u = db.query(User).filter(User.id == payload.user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")



    team_id = payload.team_id
    if team_id is not None:
        team = db.query(Team).filter(Team.id == team_id, Team.org_id == org_id).first()
        if not team:
            raise HTTPException(status_code=400, detail="Team not found in org")

    existing = (
        db.query(Membership)
        .filter(Membership.org_id == org_id, Membership.user_id == payload.user_id, Membership.team_id == team_id)
        .first()
    )
    if existing:
        existing.role = payload.role
        existing.is_active = True
        db.commit()
        db.refresh(existing)

        write_audit(
            db,
            event_type="member.updated",
            actor_user_id=auth_user.id,
            org_id=org_id,
            team_id=team_id,
            target_type="membership",
            target_id=existing.id,
            ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            payload={"user_id": payload.user_id, "role": payload.role.value, "team_id": team_id},
        )
        return existing


    m = Membership(
        user_id=payload.user_id,
        org_id=org_id,
        team_id=team_id,
        role=payload.role,
        is_active=True,
    )
    db.add(m)
    db.commit()
    db.refresh(m)

    write_audit(
        db,
        event_type="member.added",
        actor_user_id=auth_user.id,
        org_id=org_id,
        team_id=team_id,
        target_type="membership",
        target_id=m.id,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        payload={"user_id": payload.user_id, "role": payload.role.value, "team_id": team_id},
    )
    return m


@router.get("/{org_id}/teams", response_model=list[TeamOut])
def list_teams(
    org_id: int,
    db: Session = Depends(get_db),
    auth_user: User = Depends(require_api_key),
):
    require_org_role(db, auth_user.id, org_id, min_role=Role.VIEWER)
    return db.query(Team).filter(Team.org_id == org_id).order_by(Team.id.asc()).all()




