import logging
from fastapi import APIRouter, HTTPException
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
    try:
        result = await drawAnalysis(request.prompt, request.sessionId)
        return {"status": "success", "response": result}
    except Exception:
        logger.error("draw_endpoint error", exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing drawing request")
