from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from apps.candidate.routes import router as candidate_router
from Core.Auth.routes import router as auth_router
from Core.Auth.dependencies import authorize_role, templates
from db import init_db, get_session
from sqlmodel import Session

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Đăng ký router của từng module
app.include_router(candidate_router, prefix="/candidate")
app.include_router(auth_router, prefix="/auth")
@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/items/", response_model=None)
async def read_items(user = Depends(authorize_role(["admin"]))):
    return ("authorized")

# Trang chủ
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about-us")
async def about_us():
    return("about-us.html")
