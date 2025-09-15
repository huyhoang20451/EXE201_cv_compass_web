# Chứa API
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session
from .services import get_jds_by_user_name, add_jd
from db import get_session
from Core.Auth.dependencies import templates, authorize_role
from Core.Auth.schemas import user
from .schemas import JD_form
router = APIRouter(tags=["employer"])

@router.get("/business-home", response_class=HTMLResponse)
async def business_home(request: Request):
    return templates.TemplateResponse("home-business.html", {"request": request})

@router.get("/business-dashboard", response_class=HTMLResponse)
async def business_dashboard(request: Request,
                             user_info: user = Depends(authorize_role(["business"]))):
    return templates.TemplateResponse("business_dashboard.html", {"request": request, "username": user_info.username, "company": user_info.company_name})

@router.get("/pricing-business-logged-in", response_class=HTMLResponse)
async def pricing_business_logged_in(request: Request, 
                                     user_info: user = Depends(authorize_role(["business"]))):
    return templates.TemplateResponse("pricing_business_logged_in.html", {"request": request, "username": user_info.username, "company": user_info.company_name})

@router.get("/job-storage", response_class=HTMLResponse)
async def job_storage(request: Request, 
                      user_info: user = Depends(authorize_role(["business"]))):
    username = user_info.username
    job_descriptions = get_jds_by_user_name(Session, username)
    return templates.TemplateResponse("job-storage.html", {"request": request, "company": user_info.company_name, "username": username, "job_descriptions": job_descriptions})

@router.post("/submit-job", response_class=HTMLResponse)
async def submit_job(request: Request, 
                     user_info: user = Depends(authorize_role(["business"])),
                     session: Session = Depends(get_session)):
    form = await request.form()
    jd_form = dict(form)
    jd_form = JD_form(**jd_form)
    jd = add_jd(session, jd_form)
    return RedirectResponse(url="/business-dashboard", status_code=303)

@router.get("/dang-tuyen-ngay", response_class=HTMLResponse)
def dang_tuyen_ngay(request: Request, 
                    user_info: user = Depends(authorize_role(["business"]))):
    return templates.TemplateResponse("form-dang-tuyen-ngay.html", {"request": request, "username": user_info.username, "company": user_info.company_name})

@router.get("/cv-detail-business", response_class=HTMLResponse)
def cv_detail_business(request: Request, 
                       user_info: user = Depends(authorize_role(["business"]))):
    return templates.TemplateResponse("cv-detail-business.html", {"request": request, "username": user_info.username, "company": user_info.company_name})