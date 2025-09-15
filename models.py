# Chứa các models của database
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone, date

class User_db(SQLModel, table=True):
    __tablename__ = "user"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, max_length=100, unique=True)
    hashed_password: str = Field(nullable=False, max_length=255)
    role: str = Field(nullable=False, max_length=50)  # "candidate" hoặc "business"

    # Các trường chỉ dành cho business
    company_name: Optional[str] = Field(default=None, max_length=100)
    company_logo: Optional[str] = Field(default=None, max_length=255)
    location: Optional[str] = Field(default=None, max_length=100)
    coin: Optional[int] = Field(default=0)

class jd_db(SQLModel, table=True):
    __tablename__ = "jd"
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, max_length=100)
    details: str = Field(nullable=False, max_length=1000)
    location: str = Field(nullable=False, max_length=1000)
    salary: int = Field(nullable=False)
    business_id: int = Field(foreign_key="User.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

class candidate_CV_db(SQLModel, table=True):
    __tablename__ = "candidate_CV"

    cv_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="candidate.id")   # liên kết với bảng users
    URL: str = Field(max_length=255)

class jd_CV_db(SQLModel, table=True):
    __tablename__ = "jd_CV"

    cv_id: Optional[int] = Field(default=None, primary_key=True)
    jd_id: int = Field(foreign_key="jd.id")   # liên kết với bảng job
    URL: str = Field(max_length=255)