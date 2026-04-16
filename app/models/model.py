from fastapi import APIRouter
from pydantic import BaseModel
from ..analysis import chatAnalysis
from groq import APIError
from fastapi import HTTPException


model = APIRouter()


class AnalyzeRequest(BaseModel):
    prompt: str
    code: str


@model.post("/analyze", tags=["models"])
async def ai_analysis(request: AnalyzeRequest):
    try:
        response = chatAnalysis.chatAnalysis(request.prompt, request.code)
        return {"status": "success", "analysis": response}
    except APIError as e:
        raise HTTPException(status_code=503, detail="AI Service unavailable temporary")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing analysis")


@model.get("/health")
async def health_check():
    return {"status": "healthy"}
