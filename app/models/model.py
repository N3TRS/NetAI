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
    if not request.code.strip():
        raise HTTPException(
            status_code=422,
            detail="No se proporcionó código para analizar. Por favor, escribe o pega el código en el editor antes de enviar.",
        )
    if not request.prompt.strip():
        raise HTTPException(
            status_code=422,
            detail="La solicitud está vacía. Por favor, escribe una pregunta sobre el código.",
        )

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
