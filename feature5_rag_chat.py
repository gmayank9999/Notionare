from notion_client_wrapper import notion, AGENT_LOG_DB_ID
from llm_client import _call_gemini
import json

def get_workspace_context() -> str:
    """Fetch recent pages from the Agent Log to use as context for RAG."""
    try:
        response = notion.data_sources.query(
            data_source_id=AGENT_LOG_DB_ID,
            page_size=10 # Get up to 10 recent pages
        )
        pages = response.get("results", [])
    except Exception as e:
        print(f"Failed to query Notion DB for RAG: {e}")
        pages = []
        
    from notion_client_wrapper import TASKS_DB_ID
    try:
        tasks_response = notion.data_sources.query(
            data_source_id=TASKS_DB_ID,
            page_size=20 # Get up to 20 recent tasks
        )
        tasks = tasks_response.get("results", [])
    except Exception as e:
        print(f"Failed to query Tasks DB for RAG: {e}")
        tasks = []

    context = []
    
    # Process Tasks
    for task in tasks:
        props = task.get("properties", {})
        title_prop = props.get("Name", {}).get("title", [])
        title = title_prop[0].get("plain_text", "Untitled") if title_prop else "Untitled"
        
        date_prop = props.get("Due Date", {}).get("date")
        due_date = date_prop.get("start") if date_prop else "No Due Date"
        
        status_prop = props.get("Status", {}).get("select")
        status = status_prop.get("name") if status_prop else "No Status"
        
        priority_prop = props.get("Priority", {}).get("select")
        priority = priority_prop.get("name") if priority_prop else "No Priority"
        
        context.append(f"Task: {title} | Status: {status} | Priority: {priority} | Due Date: {due_date}\n---")

    # Process Pages
    for page in pages:
        props = page.get("properties", {})
        title_prop = props.get("Name", {}).get("title", [])
        title = title_prop[0].get("plain_text", "Untitled") if title_prop else "Untitled"
        page_type = props.get("Type", {}).get("select", {}).get("name", "Unknown")
        
        # Get blocks
        try:
            blocks = notion.blocks.children.list(block_id=page["id"]).get("results", [])
        except Exception as e:
            print(f"Failed to read blocks for page {title}: {e}")
            blocks = []
            
        page_content = []
        for block in blocks:
            btype = block.get("type")
            if not btype: continue
            
            # Simple text extraction for common block types
            rich_text = []
            if btype in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item", "to_do"]:
                rich_text = block.get(btype, {}).get("rich_text", [])
                
            text = "".join([rt.get("plain_text", "") for rt in rich_text])
            if text:
                page_content.append(text)
                
        # If it's a table, try to extract rows
        for block in blocks:
            if block.get("type") == "table":
                try:
                    table_rows = notion.blocks.children.list(block_id=block["id"]).get("results", [])
                    for row in table_rows:
                        if row.get("type") == "table_row":
                            cells = row.get("table_row", {}).get("cells", [])
                            row_text = " | ".join(["".join([rt.get("plain_text", "") for rt in cell]) for cell in cells])
                            if row_text:
                                page_content.append(f"Row: {row_text}")
                except Exception:
                    pass
                
        full_text = "\n".join(page_content)
        context.append(f"Document Title: {title}\nType: {page_type}\nContent:\n{full_text}\n---")
        
    return "\n\n".join(context)

def process_rag_chat(user_query: str) -> str:
    """Processes a user question by reading Notion workspace and asking Gemini."""
    context = get_workspace_context()
    
    prompt = (
        f"You are the Notionaire AI assistant. Your goal is to answer the user's question based on the content of their Notion workspace.\n\n"
        f"WORKSPACE CONTEXT (Recent Documents):\n{context}\n\n"
        f"USER QUESTION: {user_query}\n\n"
        f"INSTRUCTIONS:\n"
        f"1. Answer the question directly using ONLY the information provided in the workspace context above.\n"
        f"2. If the answer is not in the context, politely say that you don't have that information in the recent Notion logs.\n"
        f"3. Keep your answer concise, helpful, and properly formatted in Markdown."
    )
    
    answer = _call_gemini(prompt, retries=3)
    if answer is None:
        return "I'm sorry, I'm having trouble connecting to the AI service right now. Please try again."
        
    return answer

if __name__ == "__main__":
    # Test it
    q = "What were the key features of the smart attendance system we planned?"
    print(f"Q: {q}")
    print(f"A: {process_rag_chat(q)}")
