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





