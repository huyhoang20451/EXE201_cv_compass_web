from sqlmodel import Session, select
from models import User_db, jd_db
from .schemas import jd, JD_form
from typing import List

def get_jds_by_user_name(session: Session, username: str) -> List[jd]:
    statement = (
        select(jd_db)
        .join(User_db, jd_db.business_id == User_db.id)
        .where(User_db.username == username)
    )
    results = session.exec(statement).all()
    jds = [jd.model_validate(jd_in_db) for jd_in_db in results]
    return jds

def add_jd(session: Session, jd: JD_form) -> jd:
    jd_db = jd_db(**jd.model_dump())  # Pydantic v2 -> dùng model_dump()
    
    session.add(jd_db)
    session.commit()
    session.refresh(jd_db)  # để lấy id vừa tạo
    
    return jd.model_validate(jd_db)