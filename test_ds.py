from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.environ["NOTION_API_KEY"])
TASKS_DB_ID = os.environ["TASKS_DB_ID"]

print("Attempting to query as data_source...")
try:
    res = notion.data_sources.query(data_source_id=TASKS_DB_ID)
    print(f"Success! Found {len(res['results'])} items.")
except Exception as e:
    print(f"Failed query as data_source: {e}")

print("Attempting to create a page in data_source...")
try:
    res2 = notion.pages.create(
        parent={"data_source_id": TASKS_DB_ID},
        properties={
            "Name": {"title": [{"text": {"content": "Test Task from API"}}]},
            "Status": {"select": {"name": "Not Started"}}
        }
    )
    print("Success create with data_source_id!")
except Exception as e:
    print(f"Failed create with data_source_id: {e}")
    try:
        res3 = notion.pages.create(
            parent={"database_id": TASKS_DB_ID},
            properties={
                "Name": {"title": [{"text": {"content": "Test Task from API 2"}}]},
                "Status": {"select": {"name": "Not Started"}}
            }
        )
        print("Success create with database_id!")
    except Exception as e2:
        print(f"Failed create with database_id: {e2}")
