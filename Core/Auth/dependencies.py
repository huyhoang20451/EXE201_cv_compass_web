from fastapi import Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
import jwt
from typing import Annotated, List
from ..config import settings
from sqlmodel import Session
from .repository import get_user_by_username as repo_get_user_by_username
from .schemas import user
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from db import get_session

templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Lấy username từ token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username, role
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Lấy thông tin từ token
def get_current_user(request: Request,
                     session: Session = Depends(get_session)) -> user:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    username, role = decode_token(token)
    user_info = repo_get_user_by_username(session, username)
    return user.model_validate(user_info, from_attributes=True)

# Factory function
def authorize_role(required_roles: List[str]):
    async def dependency(current_user: user = Depends(get_current_user)):
        if not current_user or current_user.role not in required_roles:
            raise RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        return current_user
    return dependency