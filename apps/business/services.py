from sqlmodel import Session
from .repository import (get_jds_by_user_name as repo_get_jds_by_user_name,
                         add_jd as repo_add_jd)
from fastapi import Depends
from typing import Annotated, List
from .schemas import JD_form, OCR_result
from Core.Auth.schemas import user
from Core.Auth.dependencies import get_current_user
from OCR import OCR

def get_jds_by_user_name(session: Session, username: str) -> List[JD_form]:
    return repo_get_jds_by_user_name(session, username)

def add_jd(session: Session, jd: JD_form) -> JD_form:
    return repo_add_jd(session, jd)

def OCR(image, JD: str) -> OCR_result:
    result = OCR(image, JD)
    return OCR_result(**result)