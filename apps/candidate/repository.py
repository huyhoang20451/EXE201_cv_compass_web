# Truy vấn cơ sỏ dữ liệu
from sqlmodel import Session, select
from models import User_db, jd_db, candidate_CV_db
from .schemas import candidate_CV, jd
from sqlalchemy import or_
from typing import List, Optional

# Lấy tất cả JD theo keyword và location trong database
def search_jobs(session: Session, 
                keyword: str = None, 
                location: str = None):
    statement = select(jd_db)
    if keyword:
        keyword_pattern = f"%{keyword}"
        statement = statement.where(or_(jd_db.title.ilike(keyword_pattern), jd_db.description.ilike(keyword_pattern)))
    if location:
        location_pattern = f"%{location}"
        statement = statement.where(jd_db.location.ilike(location_pattern))
    result = session.exec(statement).all()
    return result

# Lấy tất cả CV theo username trong database
def get_cvs(session: Session, 
            username: str) -> List[candidate_CV]:
    statement = (   
        select(candidate_CV_db)
        .join(User_db, candidate_CV_db.user_id == User_db.id)
        .where(User_db.username == username)
    )
    results = session.exec(statement).all()
    CVs = [candidate_CV.model_validate(cv) for cv in results] # Chuyển sang Pydantic model
    return CVs

# Lấy tất cả JD trong database
def get_jds(session: Session) -> List[jd]:
    statement = select(jd_db)
    results = session.exec(statement)
    jds = [jd.model_validate(jd_in_db) for jd_in_db in results]
    return jds

def get_jd_by_id(session: Session, id: int) -> jd:
    statement = select(jd_db).where(jd_db.id == id)
    result = session.exec(statement).first()
    result_jd = jd.model_validate(result)
    return result_jd

# Cập nhật coin mới vào database
def update_coin(session: Session, 
                username: str, 
                new_coin: int) -> Optional[int]:

    statement = select(User_db).where(User_db.username == username)
    result = session.exec(statement).first()

    if result is None:
        return None  # không tìm thấy user

    # Update coin
    result.coin = new_coin
    session.add(result)
    session.commit()
    session.refresh(result)

    return result.coin