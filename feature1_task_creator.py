from llm_client import extract_tasks
from notion_client_wrapper import create_task

def process_user_input(user_text: str) -> str:
    tasks = extract_tasks(user_text)
    if not tasks:
        return "Sorry, I couldn't extract any tasks from your message."
        
    created_count = 0
    for t in tasks:
        task_name = t.get("task_name")
        due_date = t.get("due_date")
        priority = t.get("priority", "Medium")
        subject_tag = t.get("subject_tag", "")
        if task_name:
            try:
                create_task(task_name, due_date, priority, subject_tag)
                created_count += 1
            except Exception as e:
                print(f"Failed to create task '{task_name}': {e}")
                
    return f"Successfully created {created_count} task(s) in Notion!"
