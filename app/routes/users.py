from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.schemas import UserCreate, UserOut
from app.auth import require_api_key

