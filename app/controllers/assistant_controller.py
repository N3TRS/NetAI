import logging
import time
import uuid

from fastapi import APIRouter, HTTPException
from groq import APIError

from ..analysis import chatAnalysis
from ..middleware.injection_guard import detect_injection, is_supported_language
from ..models.analyze_request import AnalyzeRequest

logger = logging.getLogger("netai")
router = APIRouter()


@router.post("/analyze", tags=["assistant"])
async def analyze(request: AnalyzeRequest):
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

    if detect_injection(request.prompt) or detect_injection(request.code):
        raise HTTPException(status_code=400, detail="Solicitud no válida.")

    if not is_supported_language(request.code):
        raise HTTPException(
            status_code=400,
            detail="Solo se admite código en TypeScript, Python o Java.",
        )

    request_id = str(uuid.uuid4())[:8]
    start = time.time()

    try:
        response = chatAnalysis.chatAnalysis(request.prompt, request.code)
        duration = round((time.time() - start) * 1000)
        logger.info(
            f"[{request_id}] analyze code_len={len(request.code)} "
            f"prompt_len={len(request.prompt)} duration={duration}ms"
        )
        return {"status": "success", "analysis": response}
    except APIError:
        logger.error(f"[{request_id}] Groq API error", exc_info=True)
        raise HTTPException(status_code=503, detail="AI Service unavailable temporary")
    except Exception:
        logger.error(f"[{request_id}] Unexpected error", exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing analysis")


@router.get("/health")
async def health_check():
    return {"status": "healthy"}
