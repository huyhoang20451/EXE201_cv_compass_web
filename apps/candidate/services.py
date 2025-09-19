# Logic nghiệp vụ
from sqlmodel import Session
from .repository import (search_jobs as repo_search_jobs,
                         get_cvs as repo_get_cvs,
                         get_jds as repo_get_jds,
                         update_coin as repo_update_coin,
                         get_jd_by_id as repo_get_jd_by_id,
                         get_candidate_cv_by_id as repo_get_candidate_cv_by_id,
                         add_cv_into_jd as repo_add_cv_into_jd,
                         add_cv_into_candidate as repo_add_cv_into_candidate)
from fastapi import Depends, UploadFile
from fastapi.responses import JSONResponse
from typing import Annotated, List
from .schemas import JobSearchRequest, JobResponse, jd, candidate_CV, jd_CV
from Core.Auth.schemas import user
from Core.Auth.dependencies import get_current_user
import os

def search_jobs(session: Session, 
                search_params: JobSearchRequest) -> list[JobResponse]:
    jobs = repo_search_jobs(session, 
                            search_params.keyword, 
                            search_params.location)
    return [JobResponse.model_validate(job) for job in jobs] # Chuyển sang Pydantic

def get_cvs(session: Session, 
            candidate_info: Annotated[user, Depends(get_current_user)]) -> List[candidate_CV]:
    username = candidate_info.username
    return repo_get_cvs(session, 
                        username)

def get_jds(session: Session) -> List[jd]:
    return repo_get_jds(session)

def update_coin (session: Session,
                 username: str,
                 coin: int) -> int:
    return repo_update_coin(session, username, coin)

def get_jd_by_id(session: Session, id: int) -> jd:
    return repo_get_jd_by_id(session, id)

def add_cv_into_candidate(session: Session, URL: str, user_id: int) -> candidate_CV:
    cv = repo_add_cv_into_candidate(session, URL, user_id)
    return cv

async def upload_cv(file: UploadFile, user_id: int, session: Session) -> str:

    UPLOAD_DIR = "uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        add_cv_into_candidate(session, file_location, user_id)
        # Đọc nội dung file
        content = await file.read()
        with open(file_location, "wb") as f:
            f.write(content)
        return file_location
    except Exception as e:
        raise RuntimeError(f"Lỗi khi upload CV: {e}")

def get_candidate_cv_by_id(session: Session, cv_id: int) -> candidate_CV:
    cv = repo_get_candidate_cv_by_id(session, cv_id)
    return cv

def add_cv_into_jd(session: Session, URL: str, jd_id: int) -> jd_CV:
    cv = repo_add_cv_into_jd(session, URL, jd_id)
    return cv
