# Logic nghiệp vụ
from sqlmodel import Session
from .repository import (search_jobs as repo_search_jobs,
                         get_cvs as repo_get_cvs,
                         get_jds as repo_get_jds,
                         update_coin as repo_update_coin,
                         get_jd_by_id as repo_get_jd_by_id)
from fastapi import Depends
from typing import Annotated, List
from .schemas import JobSearchRequest, JobResponse, jd, candidate_CV
from Core.Auth.schemas import user
from Core.Auth.dependencies import get_current_user

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

def get_jd_by_id(session: Session) -> jd:
    return repo_get_jd_by_id(session, id)