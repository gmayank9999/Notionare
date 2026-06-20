from notion_client import Client
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

print("Testing Notion API Connection...")
try:
    notion = Client(auth=os.environ["NOTION_API_KEY"])
    result = notion.data_sources.query(data_source_id=os.environ["TASKS_DB_ID"])
    print(f"[OK] Notion Connected successfully. Found {len(result['results'])} existing rows in Tasks DB.")
except Exception as e:
    print(f"[FAIL] Notion Connection Failed: {e}")

print("\nTesting Gemini API Connection...")
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content("Say hello in exactly one word.")
    print(f"[OK] Gemini Connected successfully. Response: {response.text.strip()}")
except Exception as e:
    print(f"[FAIL] Gemini Connection Failed: {e}")