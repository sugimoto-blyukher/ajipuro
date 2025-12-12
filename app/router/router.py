from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from app.api import api

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    api.returnTemplate(request)
@router.post("/", response_class=HTMLResponse)
async def generate_text(
    request: Request,
    prompt: str = Form(...)
):
    api.return_text(request, prompt)