from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import get_db
from app.auth import require_api_key, require_user_or_403
from app.models import Signal, SignalKind, User

router = APIRouter(prefix="/stats", tags=["stats"])





