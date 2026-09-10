import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.investigation import InvestigationCreate, InvestigationResponse, FollowupRequest, FollowupResponse
from app.services.robin_service import RobinService
from app.services.storage import create, serialize
from app.models.investigation import Investigation
from app.core.config import settings

router = APIRouter(prefix="/investigations", tags=["Investigations"])
service = RobinService()

@router.post("", response_model=InvestigationResponse)
async def investigate(payload: InvestigationCreate, db: Session = Depends(get_db)):
    model = payload.model or settings.default_model
    if not model:
        raise HTTPException(400, "No LLM model selected. Configure DEFAULT_MODEL or send model.")
    try:
        result = await service.investigate(payload.query, model, payload.max_results, payload.preset, payload.custom_instructions)
    except Exception as exc:
        raise HTTPException(500, f"Investigation failed: {exc}") from exc
    item = create(db, {**result, "query": payload.query, "model": model})
    return serialize(item)

@router.get("", response_model=list[InvestigationResponse])
def list_investigations(db: Session = Depends(get_db)):
    return [serialize(x) for x in db.query(Investigation).order_by(Investigation.created_at.desc()).limit(100).all()]

@router.get("/{investigation_id}", response_model=InvestigationResponse)
def get_investigation(investigation_id: int, db: Session = Depends(get_db)):
    item = db.get(Investigation, investigation_id)
    if not item: raise HTTPException(404, "Investigation not found")
    return serialize(item)

@router.post("/{investigation_id}/followup", response_model=FollowupResponse)
async def followup(investigation_id: int, payload: FollowupRequest, db: Session = Depends(get_db)):
    item = db.get(Investigation, investigation_id)
    if not item: raise HTTPException(404, "Investigation not found")
    if not item.model: raise HTTPException(400, "Investigation has no model recorded")
    try:
        results = json.loads(item.result_json or "[]")
        answer = await service.followup(item.query, item.refined_query or item.query, results, [], item.summary or "", payload.message, payload.history, item.model)
        return {"answer": answer}
    except Exception as exc:
        raise HTTPException(500, f"Follow-up failed: {exc}") from exc
