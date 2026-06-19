# Nirukta — Agentic Orchestration Platform

> *Nirukta (निरुक्त)* — the ancient Sanskrit discipline of decoding hidden meaning from compressed knowledge. This platform does the same for your business data.

## What is Nirukta?

Nirukta is an enterprise agentic intelligence platform that lets business users ask complex questions in plain language and receive grounded, multi-step answers — without writing SQL, opening a BI tool, or waiting on an analyst.

Underneath the conversational surface sits a LangGraph-based orchestration engine that plans, executes, and self-evaluates its own work until a question is genuinely answered.

---

## Two Products

### Intelligence Workspace
For business users — Chat, Reports, Dashboards, Automations, Alerts.

### Control Center
For AI engineers, product managers, and platform admins — Agents, Prompts, Evaluation, Accuracy, Knowledge Base, Models, Cost Analytics, Observability, Governance, Users, Settings.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite + Tailwind CSS |
| Backend | FastAPI (Python) |
| Orchestration | LangGraph |
| LLM | Azure OpenAI GPT-4 |
| NL2SQL | VannaAI |
| Vector DB | Pinecone |
| State / Cache | Redis |
| Observability | Langfuse |
| Monitoring | Prometheus + Grafana |
| Deployment | Azure Kubernetes Service |
| CI/CD | Azure DevOps |

---

## Project Structure

```
nirukta/
├── frontend/          # React + Vite + Tailwind
│   └── src/
│       ├── components/shared/   # Shared UI components
│       ├── pages/workspace/     # Intelligence Workspace screens
│       ├── pages/control-center/ # Control Center screens
│       ├── hooks/               # Custom React hooks
│       ├── context/             # App-wide context providers
│       └── utils/               # Helpers and constants
├── backend/           # FastAPI
│   └── app/
│       ├── api/routes/  # API endpoints
│       ├── agents/      # LangGraph agent nodes
│       ├── tools/       # Specialized tool integrations
│       ├── services/    # Business logic services
│       ├── models/      # Pydantic models
│       └── core/        # Config, auth, middleware
├── docs/              # Documentation and planning
│   ├── planning/      # Guidebook, epics, task breakdown
│   └── design/        # Design system, wireframes
└── infrastructure/    # Deployment config
    ├── k8s/           # Kubernetes manifests
    └── docker/        # Dockerfiles
```

---

## Build Sequence

1. **Phase 0** — Project scaffold (this repo)
2. **Phase 1** — Intelligence Workspace UI (10 screens, waterfall)
3. **Phase 2** — Control Center UI (12 screens, waterfall)
4. **Phase 3** — Backend integrations
   - Azure OpenAI (LLM)
   - Pinecone + RAG (Document QA)
   - VannaAI (NL2SQL)
   - Langfuse (Observability)

---

## Design System

| Token | Value |
|---|---|
| Background | `#E8F0DE` (white + 15% green) |
| Dashlets | `#FDF0E2` (light orange) |
| Text | `#44546A` (blue-grey, single colour everywhere) |
| Status — healthy | `#639922` (green dot) |
| Status — warning | `#BA7517` (amber dot) |

---

## Getting Started

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## License
Private — All rights reserved.
