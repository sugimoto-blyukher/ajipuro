from pydantic import BaseModel


class GenerateRequest(BaseModel):
    prompt: str
    
class GenerateResponse(BaseModel):
    prompt: str
    model: str
    response: str
    
