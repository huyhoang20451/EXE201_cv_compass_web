from sqlmodel import Session
from .repository import (get_jds_by_user_name as repo_get_jds_by_user_name,
                         add_jd as repo_add_jd)
from fastapi import Depends
from typing import Annotated, List
from .schemas import jd, JD_form
from Core.Auth.schemas import user
from Core.Auth.dependencies import get_current_user

def get_jds_by_user_name(session: Session, username: str) -> List[jd]:
    return repo_get_jds_by_user_name(session, username)

def add_jd(session: Session, jd: JD_form) -> jd:
    return repo_add_jd(session, jd)