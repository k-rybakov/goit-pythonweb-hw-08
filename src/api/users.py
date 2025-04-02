from fastapi import APIRouter, Depends, Request
from src.schemas import User
from src.services.auth import get_current_user
from slowapi.util import get_remote_address
from slowapi import Limiter

router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)


@router.get("/me", response_model=User)
@limiter.limit("5/minute")
async def me(request: Request, user: User = Depends(get_current_user)):
    return user
