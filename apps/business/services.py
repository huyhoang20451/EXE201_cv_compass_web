from sqlmodel import Session
from .repository import (get_jds_by_user_name as repo_get_jds_by_user_name,
                         add_jd as repo_add_jd,
                         get_cvs_by_jd_id as repo_get_cvs_by_jd_id,
                         get_jd_by_id as repo_get_jd_by_id)
from fastapi import Depends
from typing import Annotated, List
from .schemas import JD_form, OCR_result, jd_CV
from Core.Auth.schemas import user
from Core.Auth.dependencies import get_current_user
from Core.OCR import compare

def get_jds_by_user_name(session: Session, username: str) -> List[JD_form]:
    return repo_get_jds_by_user_name(session, username)

def add_jd(session: Session, jd: JD_form) -> JD_form:
    return repo_add_jd(session, jd)

def OCR(image, JD: str) -> OCR_result:
    result = compare(image, JD)
    return OCR_result(**result)

def get_cvs_by_jd_id(session: Session, jd_id: int) -> List[jd_CV]:
    return repo_get_cvs_by_jd_id(session, jd_id)

import mimetypes

def detect_file_type(url: str):
    mime, _ = mimetypes.guess_type(url)
    if mime is None:
        return "unknown"
    elif mime.startswith("image/"):
        return "image"
    elif mime == "application/pdf":
        return "pdf"
    else:
        return "other"
    
def get_jd_by_id(session: Session, jd_id: int) -> str:
    jd = repo_get_jd_by_id(session, jd_id)
    parts = []
    if jd.job_description: parts.append(f"Mô tả công việc: {jd.job_description}")
    if jd.requirements: parts.append(f"Yêu cầu: {jd.requirements}")
    return "\n".join(parts)
