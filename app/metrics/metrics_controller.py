from fastapi import APIRouter
from fastapi.responses import Response
from .metrics_service import get_metrics

router = APIRouter()


@router.get("/metrics")
def metrics():
    data, content_type = get_metrics()
    return Response(content=data, media_type=content_type)
