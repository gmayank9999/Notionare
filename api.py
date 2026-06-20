from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import feature1_task_creator
import feature2_research_agent
import feature4_workspace_generator
import feature5_rag_chat

app = FastAPI(title="Notionaire API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow frontend to access the API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    user_text: str

class ResearchRequest(BaseModel):
    goal: str

class WorkspaceRequest(BaseModel):
    idea: str

class ChatRequest(BaseModel):
    query: str

@app.post("/api/task")
def create_task(req: TaskRequest):
    try:
        summary = feature1_task_creator.process_user_input(req.user_text)
        return {"success": True, "message": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/research")
def conduct_research(req: ResearchRequest):
    try:
        summary = feature2_research_agent.process_research_goal(req.goal)
        return {"success": True, "message": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workspace")
def generate_workspace(req: WorkspaceRequest):
    try:
        summary = feature4_workspace_generator.process_workspace_idea(req.idea)
        return {"success": True, "message": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
def chat_with_workspace(req: ChatRequest):
    try:
        answer = feature5_rag_chat.process_rag_chat(req.query)
        return {"success": True, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/monitor")
def monitor_tasks():
    try:
        import feature3_monitor
        tasks = feature3_monitor.get_open_tasks()
        alerts = feature3_monitor.detect_conflicts(tasks)
        
        if alerts:
            for alert in alerts:
                feature3_monitor.post_alert(alert)
            return {"success": True, "message": f"Found {len(alerts)} conflicts and logged them to Notion:\n\n" + "\n\n".join(alerts)}
        else:
            return {"success": True, "message": "No scheduling conflicts detected. Workspace is healthy."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
