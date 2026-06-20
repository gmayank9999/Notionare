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
        parent={"data_source_id": TASKS_DB_ID},
        properties=properties
    )

def post_alert(message: str) -> None:
    notion.pages.create(
        parent={"data_source_id": AGENT_LOG_DB_ID},
        properties={
            "Name": {"title": [{"text": {"content": "Schedule Conflict Warning"}}]},
            "Type": {"select": {"name": "Alert"}},
            "Summary": {"rich_text": [{"text": {"content": message}}]}
        }
    )

def create_research_page(title: str, synthesized: dict) -> str:
    new_page = notion.pages.create(
        parent={"data_source_id": AGENT_LOG_DB_ID},
        properties={
            "Name": {"title": [{"text": {"content": title}}]},
            "Type": {"select": {"name": "Research"}}
        }
    )
    page_id = new_page["id"]
    page_url = new_page["url"]
    
    children = []
    children.append({
        "object": "block",
        "type": "heading_1",
        "heading_1": {"rich_text": [{"type": "text", "text": {"content": title}}]}
    })
    
    if synthesized.get("intro"):
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": synthesized["intro"]}}]}
        })
        
    comp_table = synthesized.get("comparison_table", [])
    if comp_table:
        table_rows = []
        table_rows.append({
            "object": "block",
            "type": "table_row",
            "table_row": {
                "cells": [
                    [{"type": "text", "text": {"content": "Name"}}],
                    [{"type": "text", "text": {"content": "Price"}}],
                    [{"type": "text", "text": {"content": "Notable Feature"}}]
                ]
            }
        })
        for item in comp_table:
            table_rows.append({
                "object": "block",
                "type": "table_row",
                "table_row": {
                    "cells": [
                        [{"type": "text", "text": {"content": item.get("name", "")}}],
                        [{"type": "text", "text": {"content": str(item.get("price", ""))}}],
                        [{"type": "text", "text": {"content": item.get("notable_feature", "")}}]
                    ]
                }
            })
            
        children.append({
            "object": "block",
            "type": "table",
            "table": {
                "table_width": 3,
                "has_column_header": False,
                "has_row_header": True,
                "children": table_rows
            }
        })
        
    findings = synthesized.get("key_findings", [])
    if findings:
        children.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Key Findings"}}]}
        })
        for finding in findings:
            children.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": finding}}]}
            })
            
    sources = synthesized.get("sources", [])
    if sources:
        children.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Sources"}}]}
        })
        for source in sources:
            title_str = source.get("title", source.get("url", ""))
            url_str = source.get("url", "")
            if not url_str.startswith("http"):
                url_str = "https://" + url_str
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": title_str + " ", "link": {"url": url_str}}}
                    ]
                }
            })

    notion.blocks.children.append(
        block_id=page_id,
        children=children
    )
    
    return page_url

