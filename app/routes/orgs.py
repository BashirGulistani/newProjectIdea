from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Organization, Team, Membership, Role, User
from app.schemas import OrgCreate, OrgOut, TeamCreate, TeamOut, MembershipCreate, MembershipOut
from app.auth import require_api_key, require_org_role
from app.audit import write_audit

router = APIRouter(prefix="/orgs", tags=["orgs"])








