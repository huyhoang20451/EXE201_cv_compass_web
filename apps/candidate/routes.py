# Chứa API
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Request, Cookie
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import Session
from .services import (search_jobs, 
                       get_cvs, 
                       get_jds, 
                       update_coin,
                       get_jd_by_id)
from db import get_session
from Core.Auth.schemas import user
from .schemas import JobResponse, JobSearchRequest, candidate_CV
from Core.Auth.dependencies import templates, get_current_user, decode_token, authorize_role

router = APIRouter(tags=["candidate"])

# Home
@router.get("/")
async def home():
    return ("candidate_home.html")

# Home sau khi log in
@router.get("/home-logged-in", response_class=HTMLResponse)
async def home(request: Request, 
               user_info: user = Depends(authorize_role(["candidate"])), 
               session: Session = Depends(get_session)):
    job_descriptions = get_jds(session)
    return templates.TemplateResponse("home_logged_in.html", {"request": request, "job_descriptions": job_descriptions, "username": user_info.username})

@router.get("/aboutus-logged-in", response_class=HTMLResponse)
async def about_us(request: Request,
                   user_info: user = Depends(authorize_role(["candidate"]))):
    return templates.TemplateResponse("aboutus-logged-in.html", {"request": request, "username": user_info.username})

@router.get("/pricing-user-logged-in", response_class=HTMLResponse)
def pricing(request: Request,
            user_info: user = Depends(authorize_role(["candidate"]))):
    return templates.TemplateResponse("pricing-user-logged-in.html", {"request": request, "username": user_info.username})

@router.get("/ocr-scan-logged-in", response_class=HTMLResponse)
def ocr_scan(request: Request,
             user_info: user = Depends(authorize_role(["candidate"]))):
    return templates.TemplateResponse("ocr-scan.html", {"request": request, "username": user_info.username})

@router.get("/find_job")
async def find_job():
    return ("find_job.html")

@router.get("/cv_ocr")
async def cv_ocr():
    return ("cv_ocr.html")

@router.get("/pricing")
async def pricing():
    return ("pricing.html")

# Thanh tìm kiếm job
@router.post("/jobs_search", response_model=list[JobResponse])
async def search_jobs(search_params: JobSearchRequest, 
                      session: Session = Depends(get_session)):
    try:
        jobs = search_jobs(session, search_params)
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")

# Màn hình chi tiết JD
@router.get("/job-detail/{job_id}", response_class=HTMLResponse)
def job_detail(request: Request,
               job_id: int,
               user_info: user = Depends(authorize_role(["candidate"])),
               session: Session = Depends(get_session)):
    jd = get_jd_by_id(session, job_id)
    if not jd:
        raise HTTPException(status_code=404, detail="Job not found")
    return templates.TemplateResponse("job-detail.html", {"request": request, "job": jd, "username": user_info.username})

# Lấy tất cả CVs theo username lấy từ token
@router.get("/get_cvs", response_model= List[candidate_CV])
async def get_cvs(session: Session = Depends(get_session)):
    return get_cvs(session)

# Trừ coin vào database
@router.get("/deduct-coin")
async def deduct_coin(amount: int, user_info: user = Depends(authorize_role(["candidate"])), session: Session = Depends(get_session)):
    coin = user_info.coin
    if coin < amount:
        return JSONResponse(content={"success": False, "msg": "Bạn không đủ coin."})
    new_coin = coin - amount
    update_coin(session, user_info.username, new_coin)
    return JSONResponse(content={"success": True, "coin": new_coin})

# Lấy số coin trong database
@router.get("/get-coin")
async def get_coin(user_info: user = Depends(authorize_role(["candidate"]))):
    coin = user_info.coin
    return JSONResponse(content={"success": True, "coin": coin})

@router.get("/create-free-cv", response_class=HTMLResponse)
def create_free_cv(request: Request, user_info: user = Depends(authorize_role(["candidate"]))):
    return templates.TemplateResponse("create-free-cv.html", {"request": request})