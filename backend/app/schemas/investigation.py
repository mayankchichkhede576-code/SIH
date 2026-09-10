from datetime import datetime
from pydantic import BaseModel, Field

class InvestigationCreate(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    model: str | None = None
    max_results: int = Field(default=20, ge=1, le=100)
    preset: str = "threat_intel"
    custom_instructions: str = ""

class InvestigationResponse(BaseModel):
    id: int
    query: str
    refined_query: str | None
    status: str
    model: str | None
    summary: str | None
    results: list[dict]
    created_at: datetime

class FollowupRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)
    history: list[dict] = []

class FollowupResponse(BaseModel):
    answer: str
