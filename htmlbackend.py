import json
import os
from fastapi import FastAPI, HTTPException, Form, Request, requests
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import List
# File is not defined


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Đường dẫn folder templates
templates = Jinja2Templates(directory="templates")

# File JSON lưu user
USER_FILE = "database/users.json"
JD_FILE = "database/job-description.json"

# Load the model
class job_description(BaseModel):
    id: int
    company_logo: str
    job_title: str
    company_name: str
    salary: str
    location: str
    industry: str
    position: str
    company: str
    workplace: str
    job_description: List[str]
    requirements: List[str]
    benefits: List[str]
    working_time: str
    application_method: str
    deadline: str

# Hàm load các jd vào trang Cơ hội tuyển dụng
def load_jd() -> List[job_description]:
    with open(JD_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_job_detail_by_id(job_id: int) -> job_description | None:
    all_jobs = load_jd()
    job = next((item for item in all_jobs if item["id"] == job_id), None)
    return job

# Viết hàm load ra các vị trí có id = với tên đang đăng nhập
def load_jd_by_company(company: str) -> List[job_description]:
    all_jobs = load_jd()
    company_jobs = [job for job in all_jobs if job["company"] == company]
    return company_jobs 

# Băm mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==== Hàm tiện ích ====
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# ==== ROUTES ====

#---------------------------------

# Route đăng ký: nhận dữ liệu từ form

@app.post("/signup", response_class=HTMLResponse)
def signup(request: Request, username: str = Form(...), password: str = Form(...), role: str = Form("user"), company: str = Form(None)):
    users = load_users()
    if username in users:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Tên người dùng đã tồn tại"})

    hashed_pw = pwd_context.hash(password)
    user_data = {"username": username, "password": hashed_pw, "role": role, "coin": 10}
    if role == "business" and company:
        user_data["company"] = company
    users[username] = user_data
    save_users(users)

    # Chuyển về trang login và truyền thông báo thành công
    return templates.TemplateResponse("login.html", {"request": request, "success": "Đăng ký thành công"})
    
# Đăng nhập
@app.post("/login", response_class=HTMLResponse)
def login(username: str = Form(...), password: str = Form(...)):
    users = load_users()
    user = users.get(username)

    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=400, detail="Sai tên đăng nhập hoặc mật khẩu")

    user_role = user.get("role", "business")
    company = user.get("company", "")

    # Trả về trang HTML chào mừng
    if user_role == "business":
        return RedirectResponse(url=f"/business-dashboard?username={username}&role={user_role}&company={company}", status_code=303)
    else:
        return RedirectResponse(url=f"/home-logged-in?username={username}&role={user_role}", status_code=303)
#---------------------------------

# Trang đăng ký
@app.get("/signup", response_class=HTMLResponse)
def signup_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Xử lý đăng ký
@app.post("/signup")
def signup(username: str = Form(...), password: str = Form(...), role: str = Form("user"), company: str = Form(None)):
    users = load_users()
    if username in users:
        raise HTTPException(status_code=400, detail="Tên người dùng đã tồn tại")

    hashed_pw = pwd_context.hash(password)
    user_data = {"username": username, "password": hashed_pw, "role": role}
    if role == "business" and company:
        user_data["company"] = company
    users[username] = user_data
    save_users(users)

    return RedirectResponse(url="/login", status_code=303)

# Trang đăng nhập
@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Xử lý đăng nhập
@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    users = load_users()
    user = users.get(username)

    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=400, detail="Sai tên đăng nhập hoặc mật khẩu")

    # Lấy quyền người dùng
    user_role = user.get("role", "business")
    company = user.get("company", "")

    # Chuyển hướng kèm role (nếu cần dùng ở template, có thể truyền qua session hoặc query)
    if user_role == "business":
        return RedirectResponse(url=f"/business-dashboard?username={username}&role={user_role}&company={company}", status_code=303)
    else:
        return RedirectResponse(url=f"/home-logged-in?username={username}&role={user_role}", status_code=303)

#-------------------------chuyen trang khi da dang nhap---------------------------------------------
# Trang home (sau khi login)
@app.get("/home-logged-in", response_class=HTMLResponse)
def home_logged_in(request: Request, username: str):
    job_descriptions = load_jd()
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("home_logged_in.html", {"request": request, "job_descriptions": job_descriptions, "username": username})

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    # Load job descriptions
    job_descriptions = load_jd()
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("home.html", {"request": request, "job_descriptions": job_descriptions})

@app.get("/aboutus-logged-in", response_class=HTMLResponse)
def about_us(request: Request, username: str):
    return templates.TemplateResponse("aboutus-logged-in.html", {"request": request, "username": username})

@app.get("/pricing-user-loggedin", response_class=HTMLResponse)
def pricing(request: Request, username: str):
    return templates.TemplateResponse("pricing-user-loggedin.html", {"request": request, "username": username})

@app.get("/ocr-scan-logged-in", response_class=HTMLResponse)
def ocr_scan(request: Request, username: str):
    return templates.TemplateResponse("ocr-scan.html", {"request": request, "username": username})

@app.get('/top10-best-jd', response_class=HTMLResponse)
def top10_best_jd(request: Request, username: str):
    job_descriptions = load_jd()
    return templates.TemplateResponse("top10-best-jd.html", {
        "request": request,
        "username": username,
        "job_descriptions": job_descriptions
    })
    raise HTTPException(status_code=404, detail="Job not found")
    return templates.TemplateResponse("top10-best-jd.html", {"request": request, "username": username, "coin": coin, "job_description": job_description})

@app.get('/top10-best-jd-detail', response_class=HTMLResponse)
def top10_best_jd_detail(request: Request, username: str):
    job_description = load_jd()
    users = load_users()
    user = users.get(username)
    coin = user.get("coin", 0) if user else 0
    if not job_description:
        raise HTTPException(status_code=404, detail="Job not found")
    return templates.TemplateResponse("top10-best-jd-detail.html", {"request": request, "username": username, "coin": coin, "job_description": job_description})

#-----------------------------------------------------------------------------------------
#---------------------------- chuyen trang chua dang nhap---------------------------------------------
@app.get("/aboutus", response_class=HTMLResponse)
def about_us(request: Request):
    return templates.TemplateResponse("about-us.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    job_descriptions = load_jd()
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("home.html", {"request": request, "job_descriptions": job_descriptions})

@app.get("/pricing", response_class=HTMLResponse)
def pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})

# Viết trang khi click vào 1 job cần quan tâm, chuyển sang trang chi tiết
@app.get("/job-detail/{job_id}", response_class=HTMLResponse)
def job_detail(request: Request, username: str, job_id: int):
    job_descriptions = load_jd()
    
    # job_descriptions bây giờ là list dict, tìm job theo id
    job = next((item for item in job_descriptions if item["id"] == job_id), None)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Truyền job dict sang template
    return templates.TemplateResponse(
        "job-detail.html", 
        {"request": request, "job": job, "username": username}
    )

@app.get("/business-home", response_class=HTMLResponse)
def business_home(request: Request):
    return templates.TemplateResponse("home-business.html", {"request": request})

@app.get("/business-dashboard", response_class=HTMLResponse)
def business_dashboard(request: Request, username: str = None, company: str = None):
    # Nếu company chưa truyền qua query, lấy từ users.json
    if not company and username:
        users = load_users()
        user = users.get(username)
        company = user.get("company", "") if user else ""
    return templates.TemplateResponse("business_dashboard.html", {"request": request, "username": username, "company": company})

@app.get("/pricing-business-logged-in", response_class=HTMLResponse)
def pricing_business_logged_in(request: Request, username: str, company: str):
    return templates.TemplateResponse("pricing_business_logged_in.html", {"request": request, "username": username, "company": company})

@app.get("/top10-best-jd-unblur", response_class=HTMLResponse)
def top10_best_jd_unblur(request: Request, username: str):
    job_descriptions = load_jd()[:10]  # Lấy đúng 10 JD
    return templates.TemplateResponse("top10-best-jd-unblur.html", {"request": request, "job_descriptions": job_descriptions, "username": username})

@app.get("/api/deduct-coin")
def deduct_coin(username: str, amount: int):
    users = load_users()
    user = users.get(username)
    if not user:
        return JSONResponse(content={"success": False, "msg": "Không tìm thấy người dùng."})
    coin = user.get("coin", 0)
    if coin < amount:
        return JSONResponse(content={"success": False, "msg": "Bạn không đủ coin."})
    user["coin"] = coin - amount
    save_users(users)
    return JSONResponse(content={"success": True, "coin": user["coin"]})

@app.get("/api/get-coin")
def get_coin(username: str):
    users = load_users()
    user = users.get(username)
    if not user:
        return {"success": False, "msg": "Không tìm thấy người dùng.", "coin": 0}
    coin = user.get("coin", 0)
    return {"success": True, "coin": coin}

# When click on the job on top-10-best-jd-unblur, go to detail page with unblurred content
@app.get("/top10-best-jd-detail-unblur/job_id={job_id}", response_class=HTMLResponse)
def top10_best_jd_detail_unblur(request: Request, username: str, job_id: int):
    job_descriptions = load_jd()
    job = next((item for item in job_descriptions if item["id"] == job_id), None)
    users = load_users()
    user = users.get(username)
    coin = user.get("coin", 0) if user else 0
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return templates.TemplateResponse("top10-best-jd-detail-unblur.html", {"request": request, "job": job, "job_descriptions": job_descriptions, "username": username, "coin": coin})

@app.get("/create-free-cv", response_class=HTMLResponse)
def create_free_cv(request: Request):
    return templates.TemplateResponse("create-free-cv.html", {"request": request})

@app.get("/job-storage", response_class=HTMLResponse)
def job_storage(request: Request, company: str, username: str):
    job_descriptions = load_jd()
    users = load_users()
    user = users.get(username)
    company = user.get("company", "") if user else ""
    job_position = load_jd_by_company(company)
    return templates.TemplateResponse("job-storage.html", {"request": request, "company": company, "username": username, "job_position": job_position, "job_descriptions": job_descriptions})

@app.get("/job-storage/{job_id}", response_class=HTMLResponse)
def job_storage_detail(request: Request, company: str, username: str, job_id: int):
    job_descriptions = load_jd()
    users = load_users()
    user = users.get(username)
    company = user.get("company", "") if user else ""
    job_position = load_jd_by_company(company)
    job = get_job_detail_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return templates.TemplateResponse("job-storage.html", {"request": request, "company": company, "username": username, "job_position": job_position, "job_descriptions": job_descriptions, "job": job})

@app.post("/submit-job", response_class=HTMLResponse)
def submit_job(request: Request, 
               company_logo: str = Form(...), 
               job_title: str = Form(...), 
               company_name: str = Form(...), 
               salary: str = Form(...), 
               location: str = Form(...), 
               industry: str = Form(...), 
               position: str = Form(...), 
               company: str = Form(...), 
               workplace: str = Form(...), 
               job_description: str = Form(...), 
               requirements: str = Form(...), 
               benefits: str = Form(...), 
               working_time: str = Form(...), 
               application_method: str = Form(...), 
               deadline: str = Form(...), 
               username: str = Form(...)):
    job_descriptions = load_jd()
    new_id = max([job["id"] for job in job_descriptions], default=0) + 1
    # Tìm company_id cho công ty này, nếu chưa có thì gán mới
    company_ids = {job["company"]: job["company_id"] for job in job_descriptions if "company_id" in job}
    if company in company_ids:
        company_id = company_ids[company]
    else:
        company_id = max(company_ids.values(), default=0) + 1
    new_job = {
        "id": new_id,
        "company_id": company_id,
        "company_logo": company_logo,
        "job_title": job_title,
        "company_name": company_name,
        "salary": salary,
        "location": location,
        "industry": industry,
        "position": position,
        "company": company,
        "workplace": workplace,
        "job_description": job_description.split("\n"),
        "requirements": requirements.split("\n"),
        "benefits": benefits.split("\n"),
        "working_time": working_time,
        "application_method": application_method,
        "deadline": deadline
    }
    job_descriptions.append(new_job)
    with open(JD_FILE, "w", encoding="utf-8") as f:
        json.dump(job_descriptions, f, ensure_ascii=False, indent=4)
    return RedirectResponse(url=f"/job-storage?company={company}&username={username}", status_code=303)


@app.get("/dang-tuyen-ngay", response_class=HTMLResponse)
def dang_tuyen_ngay(request: Request, username: str):
    users = load_users()
    user = users.get(username)
    company = user.get("company", "") if user else ""
    return templates.TemplateResponse("form-dang-tuyen-ngay.html", {"request": request, "username": username, "company": company})

@app.get("/cv-detail-business", response_class=HTMLResponse)
def cv_detail_business(request: Request, username: str):
    users = load_users()
    user = users.get(username)
    company = user.get("company", "") if user else ""
    return templates.TemplateResponse("cv-detail-business.html", {"request": request, "username": username, "company": company})

# @app.get("/ho-so-cua-toi", response_class=HTMLResponse)
# def ho_so_cua_toi(request: Request, username: str):
#     users = load_users()
#     user = users.get(username)
#     return templates.TemplateResponse("ho-so-cua-toi.html", {"request": request, "username": username, "user": user})

@app.get("/edit-profile", response_class=HTMLResponse)
def edit_profile(request: Request, username: str):
    users = load_users()
    user = users.get(username)
    return templates.TemplateResponse("settings.html", {"request": request, "username": username, "user": user})

@app.get("/mycv-settings", response_class=HTMLResponse)
def mycv_settings(request: Request, username: str):
    users = load_users()
    user = users.get(username)
    return templates.TemplateResponse("mycv-settings.html", {"request": request, "username": username, "user": user})

@app.get("/system-settings", response_class=HTMLResponse)
def system_settings(request: Request, username: str):
    users = load_users()
    user = users.get(username)
    return templates.TemplateResponse("system-settings.html", {"request": request, "username": username, "user": user})

@app.get("/finding-jobs", response_class=HTMLResponse)
def finding_jobs(request: Request, username: str):
    users = load_users()
    user = users.get(username)
    return templates.TemplateResponse("finding-jobs.html", {"request": request, "username": username, "user": user})