from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv()

notion = Client(auth=os.environ.get("NOTION_API_KEY", ""))
TASKS_DB_ID = os.environ.get("TASKS_DB_ID", "")
AGENT_LOG_DB_ID = os.environ.get("AGENT_LOG_DB_ID", "")

def create_task(task_name, due_date, priority) -> None:
    properties = {
        "Name": {"title": [{"text": {"content": task_name}}]},
        "Priority": {"select": {"name": priority}},
        "Status": {"select": {"name": "Not Started"}},
        "Source": {"select": {"name": "Agent"}},
    }
    
    if due_date and due_date.lower() != "none" and due_date.lower() != "null":
        properties["Due Date"] = {"date": {"start": due_date}}
        
    notion.pages.create(
        parent={"database_id": TASKS_DB_ID},
        properties=properties
    )
