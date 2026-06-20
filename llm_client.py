import google.generativeai as genai
import os
import json
import datetime
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))
model = genai.GenerativeModel("gemini-2.0-flash")

def extract_tasks(user_text: str) -> list[dict]:
    today_date = datetime.date.today().strftime("%Y-%m-%d")
    prompt = f"""You are a task extraction system. Today's date is {today_date}. Given the following text, extract every distinct task mentioned. Return ONLY a JSON array, no other text, where each object has exactly these keys: task_name (string), due_date (string, format YYYY-MM-DD, inferred relative to today's date above), priority (one of: High, Medium, Low, default Medium if not stated). Text: {user_text}"""
    
    for attempt in range(2):
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            
            # Clean up markdown formatting if the LLM includes it
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
                
            return json.loads(text.strip())
        except Exception as e:
            if attempt == 1:
                print(f"Failed to extract tasks: {e}")
                return []
    return []

def generate_search_queries(goal: str) -> list[str]:
    prompt = f"Given this research goal, output 3 short, distinct search engine queries as a JSON array of strings, nothing else. Goal: {goal}"
    for attempt in range(2):
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            return json.loads(text.strip())
        except Exception as e:
            if attempt == 1:
                print(f"Failed to generate search queries: {e}")
                return []
    return []

def synthesize_research(goal: str, raw_results: list[dict]) -> dict:
    prompt = f"""Given this research goal: '{goal}', and the following search results: {json.dumps(raw_results)}, synthesize these into a JSON object with exactly these keys:
- 'intro' (string)
- 'comparison_table' (array of objects with consistent keys: name, price, notable_feature)
- 'key_findings' (array of strings)
- 'sources' (array of objects with keys: title, url)
Return ONLY the JSON object, nothing else."""
    for attempt in range(2):
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            return json.loads(text.strip())
        except Exception as e:
            if attempt == 1:
                print(f"Failed to synthesize research: {e}")
                return {}
    return {}
