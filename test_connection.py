from notion_client import Client
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# --- Notion Connection Test ---
print("Testing Notion API Connection...")
try:
    notion = Client(auth=os.environ["NOTION_API_KEY"])
    result = notion.data_sources.query(data_source_id=os.environ["TASKS_DB_ID"])
    print(f"[OK] Notion - Tasks DB connected. Found {len(result['results'])} existing rows.")
except Exception as e:
    print(f"[FAIL] Notion connection failed: {e}")

try:
    result2 = notion.data_sources.query(data_source_id=os.environ["AGENT_LOG_DB_ID"])
    print(f"[OK] Notion - Agent Log DB connected. Found {len(result2['results'])} existing rows.")
except Exception as e:
    print(f"[FAIL] Notion Agent Log connection failed: {e}")

# --- Gemini Connection Test ---
print("\nTesting Gemini API Connection...")
try:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello in exactly one word."
    )
    print(f"[OK] Gemini connected. Response: {response.text.strip()}")
except Exception as e:
    print(f"[FAIL] Gemini connection failed: {e}")