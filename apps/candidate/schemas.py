# Chứa các models của dữ liệu giữa các API
from datetime import date
from pydantic import BaseModel, HttpUrl, ConfigDict

class JobSearchRequest(BaseModel):
    keyword: str | None = None
    location: str | None = None

class JobResponse(BaseModel):
    title: str
    description: str
    location: str
    salary: float
    image: HttpUrl

    model_config = ConfigDict(from_attributes=True)

class candidate_CV(BaseModel):
    cv_id: int
    user_id: int
    URL: str

    model_config = ConfigDict(from_attributes=True)

class jd(BaseModel):
    id: int
    company_logo: str
    job_title: str
    company_name: str
    salary: str
    location: str
    details: dict

    model_config = ConfigDict(from_attributes=True)
