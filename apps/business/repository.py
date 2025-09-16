from sqlmodel import Session, select
from models import User_db, jd_db
from .schemas import JD_form
from typing import List

def get_jds_by_user_name(session: Session, username: str) -> List[JD_form]:
    statement = (
        select(jd_db)
        .join(User_db, jd_db.business_id == User_db.id)
        .where(User_db.username == username)
    )
    results = session.exec(statement).all()
    jds = [JD_form.model_validate(jd_in_db) for jd_in_db in results]
    return jds

def add_jd(session: Session, jd: JD_form) -> JD_form:
    db_obj  = jd_db(**jd.model_dump())  # Pydantic v2 -> dùng model_dump()
    
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)  # để lấy id vừa tạo
    
    return JD_form.model_validate(db_obj)