# DarkTrace Intel

AI-assisted threat intelligence workspace for authorized cybersecurity research and dark-web OSINT investigations.

DarkTrace accepts an investigation query, refines it with an LLM, gathers configured search results, filters the most relevant sources, and produces a grounded analyst summary. The project includes a FastAPI backend, a React/Vite frontend, SQLite persistence, and support for hosted or local LLM providers.

## What It Does

- Refines analyst queries into focused search terms
- Collects results from configured intelligence sources
- Uses an LLM to rank relevant sources
- Scrapes selected pages for analysis context
- Generates Markdown investigation summaries
- Stores completed investigations in SQLite
- Supports follow-up analysis using saved investigation context
- Works with OpenRouter and local Ollama models

## Architecture

```text
React/Vite frontend :5173
					|
					| REST API
					v
FastAPI backend :8000
					|
					+--> LLM provider
					|      +--> OpenRouter
					|      +--> Ollama
					|
					+--> Search and scraping pipeline
					|
					+--> SQLite investigation storage
```

The investigation pipeline is:

```text
User query
	-> Query refinement
	-> Source search
	-> Result filtering
	-> Page scraping
	-> Evidence-grounded summary
	-> SQLite persistence
	-> Frontend report
```

## Requirements

- Windows, macOS, or Linux
- Python 3.12+
- Node.js 20+
- An LLM provider: OpenRouter, Ollama, or another configured provider
- Tor/proxy and search-source access where required by the configured search pipeline

## Quick Start

### Backend

From the `backend` directory:

```powershell
cd backend
python -m venv .venv
\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

The API is available at `http://127.0.0.1:8000`.

API documentation is available at `http://127.0.0.1:8000/docs`.

### Frontend

Open a second terminal from the `frontend` directory:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Open `http://localhost:5173` in a browser.

The frontend uses `http://127.0.0.1:8000/api/v1` by default. To change it:

```powershell
$env:VITE_API_URL = "http://127.0.0.1:8000/api/v1"
npm.cmd run dev
```

## Configuration

Create a local `backend/.env` file. Never commit this file.

Start from the template:

```powershell
Copy-Item backend/.env.example backend/.env
```

Example configuration:

```env
ENVIRONMENT=development
DATABASE_URL=sqlite:///./robin.db
DEFAULT_MODEL=nex-agi/nex-n2.5-mini:free
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_API_KEY=
```

Put your real provider key only in `backend/.env`. The repository ignore rules exclude `.env` files, databases, virtual environments, dependencies, build output, logs, and local caches.

## OpenRouter

The configured free model is:

```text
nex-agi/nex-n2.5-mini:free
```

Set `OPENROUTER_API_KEY` in `backend/.env`, restart the backend, and use the model name in the frontend investigation form.

OpenRouter uses the OpenAI-compatible endpoint:

```text
https://openrouter.ai/api/v1
```

## Ollama

Install Ollama, then download a local model:

```powershell
ollama pull llama3.2
ollama list
```

Add this to `backend/.env`:

```env
OLLAMA_BASE_URL=http://127.0.0.1:11434
DEFAULT_MODEL=llama3.2
```

Ollama models are discovered through `/api/tags`. No API key is required for local Ollama usage.

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | Service metadata |
| `GET` | `/api/v1/health` | Health check |
| `POST` | `/api/v1/investigations` | Run an investigation |
| `GET` | `/api/v1/investigations` | List saved investigations |
| `GET` | `/api/v1/investigations/{id}` | Retrieve one investigation |
| `POST` | `/api/v1/investigations/{id}/followup` | Ask a grounded follow-up question |

Example request:

```powershell
$body = @{
	query = "ransomware threat actor"
	model = "nex-agi/nex-n2.5-mini:free"
	max_results = 5
} | ConvertTo-Json

Invoke-RestMethod `
	-Uri "http://127.0.0.1:8000/api/v1/investigations" `
	-Method Post `
	-ContentType "application/json" `
	-Body $body
```

## Response

An investigation returns the original query, refined query, selected model, status, source results, generated summary, and creation timestamp:

```json
{
	"id": 1,
	"query": "ransomware threat actor",
	"refined_query": "ransomware threat actor groups",
	"status": "completed",
	"model": "nex-agi/nex-n2.5-mini:free",
	"summary": "## Input Query\n...",
	"results": [],
	"created_at": "2026-09-11T00:00:00Z"
}
```

## Project Structure

```text
backend/
	app/
		api/          FastAPI routes
		core/         Application settings
		db/           SQLAlchemy session setup
		models/       Database models
		schemas/      Request and response schemas
		services/     Investigation orchestration and storage
frontend/
	src/
		main.jsx      React application
		services/     Backend API client
		styles/       DarkTrace visual theme
llm.py            LLM prompts and analysis operations
llm_utils.py      Provider registry and model discovery
search.py         Search-source integration
scrape.py         Page scraping pipeline
config.py         Environment-based provider configuration
```

## Security and Responsible Use

- Use this project only for authorized defensive research and OSINT work.
- Do not commit API keys, passwords, cookies, or private investigation data.
- Rotate any credential that has been exposed in chat, logs, screenshots, or commits.
- Treat dark-web content as untrusted input.
- Validate findings against independent sources before taking action.

## Development

Build the frontend before deployment:

```powershell
cd frontend
npm.cmd run build
```

Run the backend health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/v1/health
```

