from google import genai
from typing import Any
import os
import json
import datetime
import time
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
MODEL = "gemini-2.5-flash-lite"

def _clean_json_text(text: str) -> str:
    """Strip markdown code fences the LLM sometimes wraps around JSON."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def _call_gemini(prompt: str, retries: int = 4) -> str | None:
    """Call Gemini with retry logic and rate-limit backoff."""
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            return response.text
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "Too Many Requests" in err_str:
                wait = 10 * (attempt + 1)
                print(f"Rate limited, waiting {wait}s before retry (attempt {attempt + 1}/{retries})...")
                time.sleep(wait)
            else:
                if attempt == retries - 1:
                    print(f"Gemini call failed: {e}")
                    return None
    return None

def _robust_generate(prompt: str) -> Any:
    """Call Gemini and parse the response as JSON."""
    raw = _call_gemini(prompt)
    if raw is None:
        return None
    try:
        return json.loads(_clean_json_text(raw))
    except json.JSONDecodeError as e:
        print(f"JSON parse failed: {e}")
        # one more try
        raw = _call_gemini(prompt)
        if raw is None:
            return None
        try:
            return json.loads(_clean_json_text(raw))
        except json.JSONDecodeError:
            print(f"JSON parse failed on retry too. Raw response: {raw[:200]}")
            return None

def extract_tasks(user_text: str) -> list[dict]:
    today_date = datetime.date.today().strftime("%Y-%m-%d")
    prompt = (
        f"You are a task extraction system. Today's date is {today_date}. "
        f"Given the following text, extract every distinct task mentioned. "
        f"Return ONLY a JSON array, no other text, where each object has exactly these keys: "
        f"task_name (string), due_date (string, format YYYY-MM-DD, inferred relative to today's date above), "
        f"priority (one of: High, Medium, Low, default Medium if not stated), "
        f"subject_tag (string, a short category like 'DSA', 'DBMS', 'GenAI', 'Work', etc. inferred from context). "
        f"Text: {user_text}"
    )
    result = _robust_generate(prompt)
    return result if isinstance(result, list) else []

def generate_search_queries(goal: str) -> list[str]:
    prompt = (
        f"Given this research goal, output 3 short, distinct search engine queries "
        f"as a JSON array of strings, nothing else. Goal: {goal}"
    )
    result = _robust_generate(prompt)
    return result if isinstance(result, list) else []

def synthesize_research(goal: str, raw_results: list[dict]) -> dict:
    prompt = (
        f"Given this research goal: '{goal}', and the following search results: "
        f"{json.dumps(raw_results)}, synthesize these into a JSON object with exactly these keys:\n"
        f"- 'intro' (string)\n"
        f"- 'comparison_table' (array of objects with consistent keys: name, price, notable_feature)\n"
        f"- 'key_findings' (array of strings)\n"
        f"- 'sources' (array of objects with keys: title, url)\n"
        f"Return ONLY the JSON object, nothing else."
    )
    result = _robust_generate(prompt)
    return result if isinstance(result, dict) else {}

def generate_prd(idea: str) -> dict:
    prompt = (
        f"Given this project idea: '{idea}', generate a product requirements document as a "
        f"JSON object with exactly these keys: 'problem_statement' (string), "
        f"'target_users' (array of strings), 'core_features' (array of 3-5 strings). "
        f"Return ONLY the JSON object, nothing else."
    )
    result = _robust_generate(prompt)
    return result if isinstance(result, dict) else {}

def generate_task_breakdown(prd: dict) -> list[dict]:
    today_date = datetime.date.today().strftime("%Y-%m-%d")
    prompt = (
        f"Given this PRD: {json.dumps(prd)}, generate a list of 8-12 concrete build tasks "
        f"spaced out starting from today ({today_date}) across 2-4 weeks. "
        f"Return ONLY a JSON array of objects with exactly these keys: "
        f"'task_name' (string), 'due_date' (YYYY-MM-DD), 'priority' (High/Medium/Low), "
        f"'subject_tag' (string, a short category for this task like 'Backend', 'Frontend', 'Database', 'Testing', etc.). "
        f"Nothing else."
    )
    result = _robust_generate(prompt)
    return result if isinstance(result, list) else []

def generate_milestones(tasks: list[dict]) -> list[dict]:
    prompt = (
        f"Group these tasks into 3-4 dated milestones: {json.dumps(tasks)}. "
        f"Return ONLY a JSON array of objects with exactly these keys: "
        f"'milestone_title' (string), 'target_date' (YYYY-MM-DD), "
        f"'task_names' (array of strings matching the input tasks). Nothing else."
    )
    result = _robust_generate(prompt)
    return result if isinstance(result, list) else []

def generate_risks(prd: dict) -> list[str]:
    prompt = (
        f"Given this PRD: {json.dumps(prd)}, list 3-5 plausible risks "
        f"as a JSON array of short strings. Nothing else."
    )
    result = _robust_generate(prompt)
    return result if isinstance(result, list) else []
