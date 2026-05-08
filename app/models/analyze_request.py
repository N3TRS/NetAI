from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    prompt: str = Field(..., max_length=2000)
    code: str = Field(..., max_length=32000)
