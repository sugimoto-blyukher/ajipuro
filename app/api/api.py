from fastapi import  HTTPException
from fastapi.templating import Jinja2Templates
from google import genai
from google.genai import types
from app.config import config


templates = Jinja2Templates(directory="templates")

client = genai.Client(api_key="AIzaSyCoRv_ksEZWLV2AyLjzNiFjTz17azqca1s")
modelName = config.MODEL_NAME


def returnTemplate(request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "prompt": "",
            "result": None,
            "model": modelName,
        },
    )


def return_text(request, prompt):
    try:
        result = client.models.generate_content(
            model=modelName,
            config=types.GenerateContentConfig(
                system_instruction="あなたはソ連のプラウダの編集員だ。promptの内容をソ連のアジプロ風に変換しろ、それだけ出力すればいい"),
            contents=prompt,
        )
        text = result.text
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'Gemini API error: {e}')

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "prompt": prompt,
            "result": text,
            "model": modelName,
        },
    )