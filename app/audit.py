import json
from typing import Any, Dict
from sqlalchemy.orm import Session
from app.models import AuditEvent

def write_audit(
    db: Session,
    *,
    event_type: str,
    actor_user_id: int | None,
    org_id: int | None = None,
    team_id: int | None = None,
    target_type: str | None = None,
    target_id: int | None = None,
    ip: str | None = None,
    user_agent: str | None = None,
    payload: Dict[str, Any] | None = None,
) -> AuditEvent:

