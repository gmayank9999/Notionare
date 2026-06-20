from llm_client import generate_prd, generate_task_breakdown, generate_milestones, generate_risks
from notion_client_wrapper import create_task, create_workspace_pages

def process_workspace_idea(idea: str) -> str:
    print(f"Generating workspace for idea: {idea}")
    
    print("1. Generating PRD...")
    prd = generate_prd(idea)
    if not prd:
        return "Failed to generate PRD."
        
    print("2. Generating Task Breakdown...")
    tasks = generate_task_breakdown(prd)
    
    print("3. Generating Milestones...")
    milestones = generate_milestones(tasks)
    
    print("4. Generating Risks...")
    risks = generate_risks(prd)
    
    print("Writing Workspace Pages to Notion...")
    urls = create_workspace_pages(prd, milestones, risks)
    
    if tasks:
        print(f"Creating {len(tasks)} tasks in the database...")
        for t in tasks:
            try:
                create_task(t.get("task_name"), t.get("due_date"), t.get("priority", "Medium"))
            except Exception as e:
                print(f"Failed to create task '{t.get('task_name')}': {e}")
                
    return f"Workspace generated successfully! View your PRD here: {urls.get('prd_url')}"
