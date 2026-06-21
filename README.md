# Notionaire

**An Autonomous AI Command Center for Notion.**

Notionaire turns your Notion workspace from a passive note-taking tool into an intelligent, self-managing system. Instead of manually creating tasks, writing documents, and tracking deadlines — just type a sentence and let the AI handle the rest.

---

## Features

### Intelligent Task Extraction
Type a natural-language sentence like *"Finish the DSA assignment by Wednesday, high priority"* and Notionaire will extract the task name, calculate the due date, infer the priority, tag the subject, and create a structured entry in your Notion Tasks database — automatically.

### Automated Research Agent
Give it a research topic. Notionaire searches the live internet via DuckDuckGo, collects results from multiple queries, synthesizes them using Google Gemini into a structured report with comparison tables, key findings, and cited sources — then writes it as a fully formatted Notion page.

### Idea-to-Workspace Generator
Describe a project idea in one sentence. Notionaire runs a **4-stage agentic pipeline** to generate:
- A Product Requirements Document (PRD)
- 8–12 engineering tasks with staggered deadlines
- Grouped milestones
- A risk assessment

All written to your Notion workspace as interconnected, cross-linked pages.

### Chat with Your Workspace (RAG)
Ask questions about your own data — *"What are the risks of the attendance system?"* — and get accurate answers sourced exclusively from your Notion pages and tasks. Powered by Retrieval-Augmented Generation: the system fetches your data from Notion, parses the block content, and injects it into the AI prompt as context.

### Project Monitor
Scans your Tasks database for scheduling conflicts. If multiple high-priority tasks share the same deadline, it flags them and logs a warning to Notion. Runs locally on demand, or automatically every hour in the cloud via GitHub Actions.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Engine | Google Gemini (`gemini-2.5-flash-lite`) |
| Backend | Python, FastAPI, Uvicorn |
| Database | Notion API (`notion-client` SDK) |
| Web Search | DuckDuckGo (`ddgs`) |
| Frontend | React + Vite (premium UI) / Streamlit (rapid prototype) |
| CI/CD | GitHub Actions (automated monitoring) |

---

## Architecture

```
Notionare/
├── llm_client.py                  # Gemini API wrapper with exponential backoff
├── notion_client_wrapper.py       # Notion block builder & database operations
├── search_tool.py                 # DuckDuckGo search interface
├── feature1_task_creator.py       # NLP task extraction
├── feature2_research_agent.py     # Web research + synthesis pipeline
├── feature3_monitor.py            # Deadline conflict detection
├── feature4_workspace_generator.py # 4-stage agentic workspace pipeline
├── feature5_rag_chat.py           # RAG engine with Notion block parsing
├── api.py                         # FastAPI server (5 REST endpoints)
├── chat_app.py                    # Streamlit UI
├── frontend/                      # React + Vite premium UI
│   └── src/
│       ├── App.jsx
│       └── index.css
├── .github/workflows/monitor.yml  # Automated hourly monitor (GitHub Actions)
├── e2e_test.py                    # End-to-end test suite
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- A [Notion Integration](https://www.notion.so/my-integrations) with access to your workspace
- A [Google Gemini API Key](https://aistudio.google.com/apikey)

### 1. Clone the repository

```bash
git clone https://github.com/gmayank9999/Notionare.git
cd Notionare
```

### 2. Set up the Python environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
NOTION_API_KEY=your_notion_integration_token
TASKS_DB_ID=your_tasks_database_id
AGENT_LOG_DB_ID=your_agent_log_database_id
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Set up Notion databases

Create two databases in your Notion workspace:

**Tasks Database** with these properties:
| Property | Type |
|----------|------|
| Name | Title |
| Status | Select (`Not Started`, `In Progress`, `Done`) |
| Priority | Select (`High`, `Medium`, `Low`) |
| Due Date | Date |
| Subject/Tag | Rich Text |
| Source | Select (`Agent`, `Manual`) |

**Agent Log Database** with these properties:
| Property | Type |
|----------|------|
| Name | Title |
| Type | Select (`Research`, `Action`, `Alert`) |
| Timestamp | Date |
| Summary | Rich Text |
| Linked Page | URL |

Share both databases with your Notion integration.

### 5. Start the backend

```bash
python api.py
```

The API server starts on `http://localhost:8000`.

### 6. Start the frontend

**Option A — React (Premium UI):**
```bash
cd frontend
npm install
npm run dev
```
Opens on `http://localhost:5173`.

**Option B — Streamlit:**
```bash
streamlit run chat_app.py
```
Opens on `http://localhost:8501`.

---

## API Endpoints

| Method | Endpoint | Payload | Description |
|--------|----------|---------|-------------|
| POST | `/api/task` | `{ "user_text": "..." }` | Extract and create tasks from natural language |
| POST | `/api/research` | `{ "goal": "..." }` | Research a topic and create a Notion report |
| POST | `/api/workspace` | `{ "idea": "..." }` | Generate a full project workspace |
| POST | `/api/chat` | `{ "query": "..." }` | Ask a question about your workspace (RAG) |
| POST | `/api/monitor` | `{}` | Scan for scheduling conflicts |

---

## Cloud Monitoring (GitHub Actions)

The project includes a GitHub Actions workflow that runs the Project Monitor every hour automatically. To enable it:

1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Add these repository secrets:
   - `NOTION_API_KEY`
   - `TASKS_DB_ID`
   - `AGENT_LOG_DB_ID`
   - `GEMINI_API_KEY`

The workflow will run on schedule and can also be triggered manually from the Actions tab.

---

## How It Works

```
User Input (plain English)
       │
       ▼
  FastAPI Backend
       │
       ├──► Google Gemini (AI processing)
       ├──► DuckDuckGo (web search)
       │
       ▼
  Notion API
       │
       ├──► Tasks Database (structured task entries)
       └──► Agent Log Database (PRDs, research, alerts)
```

The system uses **Agentic Chaining** for the workspace generator (output of one AI call feeds into the next), **Retrieval-Augmented Generation** for the chat feature (Notion data injected into prompts), and **Exponential Backoff** for resilient API handling.

