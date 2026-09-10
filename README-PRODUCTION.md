# Robin — Production-style integration

This layout keeps the original Robin modules intact and adds a FastAPI application layer plus a Vite/React frontend.

## Local development

### Backend
From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env
# copy your provider credentials into .env
uvicorn backend.app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. API docs are at http://localhost:8000/docs.

Set `DEFAULT_MODEL` to one of the model keys supported by the original `llm_utils.py`, or provide the model in the UI.

## Architecture

`frontend -> FastAPI /api/v1 -> services -> original Robin search/LLM/scraping modules -> GraphSense integration`

The original Streamlit `ui.py` remains in the repository for backward compatibility.
