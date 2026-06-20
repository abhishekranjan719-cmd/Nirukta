# nirukt — Agentic Orchestration Platform

> *nirukt* (निरुक्त) — the ancient Sanskrit discipline of decoding hidden meaning from compressed knowledge. This platform does the same for your business data.

## What is nirukt?

nirukt is an enterprise agentic intelligence platform that lets business users ask complex questions in plain language and receive grounded, multi-step answers — without writing SQL, opening a BI tool, or waiting on an analyst.

Underneath the conversational surface sits a LangGraph-based orchestration engine that plans, executes, and self-evaluates its own work until a question is genuinely answered.

---

## Two Products

### Intelligence Workspace
For business users — Chat, Reports, Dashboards, Automations, Alerts.

### Control Center
For AI engineers, product managers, and platform admins — Agents, Prompts, Evaluation, Accuracy, Knowledge Base, Models, Cost Analytics, Observability, Governance, Users, Settings.

---

## Branch Structure — read this first

This repo currently has work split across two branches:

| Branch | Contents |
|---|---|
| `main` | The nirukt app scaffold — routing shell, all 22 page stubs, design tokens, shared components (Logo, StatusDot, DashletCard, etc), FastAPI route shells, agent/tool stubs. **This is what's being actively built screen by screen.** |
| `master` | Two things pushed from existing prior work: the `z/` folder (a working LangGraph ReAct agent, FastAPI backend, LiteLLM proxy, Langfuse v3, full Docker infra stack) and the `kaara-zuna` frontend (Sidebar, Header, ChatPanel, DashboardLayout — real working React components from an earlier prototype). |

**Why two branches right now:** `master` holds genuinely working code that predates nirukt's current design system and naming. `main` is the clean nirukt build following the locked design system (background `#E8F0DE`, dashlets `#FDF0E2`, text `#44546A`) and the waterfall build sequence. As each screen on `main` reaches the point of needing real backend logic, the equivalent working code from `master`'s `z/` engine gets ported over and adapted — rather than merging the branches wholesale.

---

## Design System

| Token | Value |
|---|---|
| Background | `#E8F0DE` (white + 15% green) |
| Dashlets | `#FDF0E2` (light orange) |
| Text | `#44546A` (blue-grey, single colour everywhere) |
| Status — healthy | `#639922` (green dot) |
| Status — warning | `#BA7517` (amber dot) |
| Font | Inter — imported once in `index.css`, applied globally |

Full spec: [`docs/design/DESIGN_SYSTEM.md`](docs/design/DESIGN_SYSTEM.md)

UI mantra: less code, less bugs. No clutter. Every screen guides the next action invisibly. Minimal scrolling.

---

## Brand

- Name: **nirukt** — always lowercase, no exceptions
- Logo: `frontend/src/components/shared/Logo.tsx` — "The Decode" mark. Left half is fragmented/compressed data, a decode axis divides it from the resolved N on the right, marked with diamond connection nodes and a data pulse on the diagonal.
- Logo asset (SVG, favicon): `frontend/src/assets/brand/logo.svg`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite + Tailwind CSS + TypeScript |
| Backend | FastAPI (Python) |
| Orchestration | LangGraph |
| LLM | Azure OpenAI GPT-4 (via LiteLLM proxy) |
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
nirukt/
├── frontend/                       # React + Vite + Tailwind (main branch)
│   ├── public/
│   │   └── favicon.svg
│   └── src/
│       ├── assets/brand/           # Logo SVG source
│       ├── components/shared/      # Logo, StatusDot, DashletCard, SideNav, TopBar
│       ├── pages/workspace/        # Intelligence Workspace — 10 screens
│       ├── pages/control-center/   # Control Center — 12 screens
│       ├── hooks/
│       ├── context/                # AuthContext
│       └── utils/                  # tokens.ts, api.ts
├── backend/                        # FastAPI (main branch — scaffold)
│   └── app/
│       ├── api/routes/
│       ├── agents/                 # planner, evaluator, router stubs
│       ├── tools/                  # nl2sql, document_qa, python_repl, etc
│       ├── models/                 # AgentState
│       └── core/                   # config
├── docs/
│   ├── planning/                   # Guidebook, orchestration approach
│   └── design/                     # DESIGN_SYSTEM.md
└── infrastructure/
    ├── k8s/
    └── docker/
```

---

## Build Sequence — waterfall

1. **Phase 0** — Project scaffold ✅
2. **Phase 1** — Intelligence Workspace UI (10 screens)
   - [x] 01 — Login
   - [ ] 02 — Intelligence Home
   - [ ] 03 — Conversation Workspace
   - [ ] 04 — Agent Execution Timeline
   - [ ] 05 — Intelligence Results
   - [ ] 06 — Drill Down / Root Cause
   - [ ] 07 — Report Builder
   - [ ] 08 — Action Center
   - [ ] 09 — Alert Centre
   - [ ] 10 — Conversation History
3. **Phase 2** — Control Center UI (12 screens) — not started
4. **Phase 3** — Backend integrations — not started
   - Azure OpenAI (LLM)
   - Pinecone + RAG (Document QA)
   - VannaAI (NL2SQL)
   - Langfuse (Observability)

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
