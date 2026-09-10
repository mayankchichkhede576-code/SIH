import json
from sqlalchemy.orm import Session
from app.models.investigation import Investigation

def create(db: Session, payload: dict):
    item = Investigation(
        query=payload["query"], refined_query=payload.get("refined"), status="completed",
        model=payload.get("model"), summary=payload.get("summary"),
        result_json=json.dumps(payload.get("results", []), ensure_ascii=False, default=str),
    )
    db.add(item); db.commit(); db.refresh(item); return item

def serialize(item):
    return {
        "id": item.id, "query": item.query, "refined_query": item.refined_query,
        "status": item.status, "model": item.model, "summary": item.summary,
        "results": json.loads(item.result_json or "[]"), "created_at": item.created_at,
    }
