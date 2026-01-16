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

    """
    Append-only audit event. Never update or delete these in code.
    """
    evt = AuditEvent(
        event_type=event_type,
        actor_user_id=actor_user_id,
        org_id=org_id,
        team_id=team_id,
        target_type=target_type,
        target_id=target_id,
        ip=ip,
        user_agent=user_agent,
        payload_json=json.dumps(payload or {}, ensure_ascii=False),
    )
    db.add(evt)
    db.commit()
    db.refresh(evt)
    return evt
