from datetime import date
from pydantic import BaseModel, HttpUrl, ConfigDict

class jd(BaseModel):
    id: int
    company_logo: str
    job_title: str
    company_name: str
    salary: str
    location: str
    details: dict

    model_config = ConfigDict(from_attributes=True)

class JD_form(BaseModel)
    company_logo: str
    job_title: str
    company_name: str
    salary: str
    location: str
    details: dict

    model_config = ConfigDict(from_attributes=True)