from fastapi import APIRouter
from pydantic import BaseModel
from ..analysis import chatAnalysis

model = APIRouter()


class AnalyzeRequest(BaseModel):
    prompt: str
    code: str


@model.post("/analyze", tags=["models"])
async def ai_analysis(request: AnalyzeRequest):
    return chatAnalysis.chatAnalysis(request.prompt, request.code)
