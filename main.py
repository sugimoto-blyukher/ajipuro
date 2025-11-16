from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from dotenv import load_dotenv
from app.prompt import GenerateRequest, GenerateResponse
from google import genai
import os
from google.genai import types

load_dotenv()



API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("環境変数 GEMINI_API_KEY が設定されていません。")


client = genai.Client()

MODEL_NAME = "gemini-2.5-flash"

app = FastAPI(title="Gemini JSON API")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "prompt": "",
            "result": None,
            "model": MODEL_NAME,
        },
    )

@app.post("/", response_model=GenerateResponse, response_class=HTMLResponse)
async def generate_text(
    request: Request,
    prompt: str = Form(...)
):
    
    try:
        result = client.models.generate_content(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction="あなたはソ連のプラウダの編集員だ。promptの内容をソ連のアジプロ風に変換しろ、それだけ出力すればいい"),
            contents=prompt,
        )
        text = result.text
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Gemini API error: {e}")
    

    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "prompt": prompt,
            "result": text,
            "model": MODEL_NAME,
        },
    )
