from fastapi import  HTTPException
from fastapi.templating import Jinja2Templates
from google import genai
from google.genai import types
from app.config import config


templates = Jinja2Templates(directory="templates")

client = genai.Client(api_key=config.API_KEY)
modelName = config.MODEL_NAME
systemInstruction = config.SYSTEM_INSTRUCTION


def returnTemplate(request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
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
                system_instruction=systemInstruction
            ),
            contents=prompt,
        )
        text = result.text
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'Gemini API error: {e}')

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "prompt": prompt,
            "result": text,
            "model": modelName,
        },
    )
