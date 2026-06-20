from notion_client_wrapper import notion, TASKS_DB_ID, post_alert
from collections import defaultdict

def get_open_tasks():
    response = notion.data_sources.query(
        data_source_id=TASKS_DB_ID,
        filter={
            "property": "Status",
            "select": {
                "does_not_equal": "Done"
            }
        }
    )
    return response.get("results", [])

def detect_conflicts(tasks: list) -> list[str]:
    date_to_high_priority_tasks = defaultdict(list)
    for task in tasks:
        props = task.get("properties", {})
        
        priority_prop = props.get("Priority", {}).get("select")
        priority = priority_prop.get("name") if priority_prop else "Medium"
        
        date_prop = props.get("Due Date", {}).get("date")
        due_date = date_prop.get("start") if date_prop else None
        
        title_prop = props.get("Name", {}).get("title", [])
        task_name = title_prop[0].get("plain_text", "Unnamed Task") if title_prop else "Unnamed Task"
        
        if due_date and priority == "High":
            date_to_high_priority_tasks[due_date].append(task_name)
            
    alerts = []
    for date, conflict_tasks in date_to_high_priority_tasks.items():
        if len(conflict_tasks) >= 2:
            task_names = "', '".join(conflict_tasks)
            alerts.append(f"Conflict detected: '{task_names}' are all due on {date} and marked High Priority.")
            
    return alerts

def main():
    print("Checking for task conflicts...")
    tasks = get_open_tasks()
    alerts = detect_conflicts(tasks)
    
    if alerts:
        for alert in alerts:
            print(f"Posting alert: {alert}")
            post_alert(alert)
    else:
        print("No conflicts detected.")

if __name__ == "__main__":
    main()
