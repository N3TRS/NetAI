import logging
from fastapi import APIRouter
from pydantic import BaseModel, field_validator
from app.analysis.drawAnalysis import drawAnalysis

logger = logging.getLogger("netai")
router = APIRouter()


class DrawRequest(BaseModel):
    prompt: str
    sessionId: str

    @field_validator("prompt", "sessionId")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


@router.post("/draw")
async def draw_endpoint(request: DrawRequest):
    result = await drawAnalysis(request.prompt, request.sessionId)
    return {"status": "success", "response": result}
