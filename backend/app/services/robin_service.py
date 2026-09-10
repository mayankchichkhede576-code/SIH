import asyncio
import json
import sys
from pathlib import Path

# Keep the original Robin modules untouched. Add project root to Python path.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from llm import get_llm, refine_query, filter_results, generate_summary, build_followup_context, answer_followup
from search import get_search_results
from scrape import scrape_multiple

class RobinService:
    async def investigate(self, query: str, model: str, max_results: int, preset: str, custom_instructions: str):
        llm = await asyncio.to_thread(get_llm, model)
        refined = await asyncio.to_thread(refine_query, llm, query)
        results = await asyncio.to_thread(get_search_results, refined)
        results = results[:max_results]
        filtered = await asyncio.to_thread(filter_results, llm, refined, results)
        if filtered:
            results = filtered
        scraped = await asyncio.to_thread(scrape_multiple, results)
        # Original scraper may return structured data; preserve it for grounding.
        content = json.dumps(scraped, ensure_ascii=False, default=str)
        summary = await asyncio.to_thread(generate_summary, llm, query, content, preset, custom_instructions)
        return {"refined": refined, "results": results, "scraped": scraped, "summary": summary}

    async def followup(self, query, refined, sources, scraped, summary, message, history, model, preset="threat_intel"):
        llm = await asyncio.to_thread(get_llm, model)
        context = build_followup_context(query, refined, sources, scraped, summary)
        # Keep history simple and grounded; original function accepts LangChain messages,
        # so the API converts plain records when possible.
        from langchain_core.messages import HumanMessage, AIMessage
        messages = []
        for item in history[-10:]:
            role, content = item.get("role"), item.get("content", "")
            if role == "user": messages.append(HumanMessage(content=content))
            elif role == "assistant": messages.append(AIMessage(content=content))
        answer = await asyncio.to_thread(answer_followup, llm, message, context, messages, preset, "")
        return answer
