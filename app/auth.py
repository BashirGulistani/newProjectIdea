from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.models import Membership, Role


def require_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    db: Session = Depends(get_db),
) -> User:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key")
    user = db.query(User).filter(User.api_key == x_api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return user

def require_user_or_403(
    user_id: int,
    auth_user: User,
):
    if auth_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: user mismatch")






_ROLE_RANK = {
    Role.VIEWER: 1,
    Role.MEMBER: 2,
    Role.ADMIN: 3,
    Role.OWNER: 4,
}


