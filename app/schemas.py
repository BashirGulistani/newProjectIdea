from datetime import datetime
from pydantic import BaseModel, Field
from app.models import SignalKind

class UserCreate(BaseModel):
    display_name: str = Field(min_length=1, max_length=80)

class UserOut(BaseModel):
    id: int
    display_name: str
    api_key: str
    created_at: datetime

    class Config:
        from_attributes = True

class SignalCreate(BaseModel):
    sender_id: int
    recipient_id: int
    kind: SignalKind
    ttl_minutes: int | None = Field(default=None, ge=1, le=60 * 24 * 30) 

class SignalOut(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    kind: SignalKind
    created_at: datetime
    expires_at: datetime | None
    seen: bool
    seen_at: datetime | None

    class Config:
        from_attributes = True

class MarkSeenOut(BaseModel):
    id: int
    seen: bool
    seen_at: datetime | None

    class Config:
        from_attributes = True






from app.models import Role

class OrgCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)







