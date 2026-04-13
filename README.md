# ENAE VET

Baseline documentation and project skeleton for the ENAE VET system. This ticket (`SCRUM-5` on the Jira SCRUM board) initially focused on architecture, tech stack, workflow, and documentation structure.

Since subsequent tickets (SCRUM-6 onwards), the project now includes an initial implementation of an AI-powered chatbot (LangChain-based), including session memory, RAG, and tool integration at a basic level.

---

## 1. Target architecture (high-level)

- **Web client (frontend)**: React/TypeScript UI for reception/admin users and, later, veterinarians.
- **Backend API (FastAPI)**: Single source of truth for business logic, validation, and authorization.
- **Relational database (PostgreSQL)**: Transactional persistence (clients, pets, appointments, services, users/roles, etc.).
- **Authentication & authorization**: Role-based access control (future).
- **Integrations (future)**: Email/WhatsApp notifications, calendar, payments.

### Separation of layers

- **Frontend**: UI, basic validation, API consumption.
- **Backend**: Business rules, validation, orchestration.
- **Database**: Normalized relational model with migrations.

### Environments

- Local  
- Staging  
- Production  

### Principles

- Backend = single source of truth  
- ADRs for architecture decisions  
- No secrets in repo  

---

## 2. Baseline tech stack

### Backend

- Python 3.12+
- FastAPI
- Pydantic
- SQLAlchemy + Alembic
- PostgreSQL
- pytest (+ pytest-cov)

### Frontend (planned)

- React + TypeScript
- TailwindCSS
- Playwright / Vitest

### Infra

- Docker
- GitHub Actions
- Environment variables

---

## 3. Workflow (SCRUM + Jira)

- Board: Jira (SCRUM)
- Flow: To Do → In Progress → Code Review → QA → Done

### Branching

- `feature/SCRUM-X-description`

### Definition of Done

- Code merged  
- Tests passing  
- Documentation updated  

---

## 4. Documentation index

- `README.md`
- `docs/architecture/`
- `docs/adr/`
- `docs/api/`
- `docs/db/`
- `docs/runbook/`
- `docs/security/`

### Domain (SCRUM-14 / VET-14)

- `docs/domain/glossary-and-preparation.md`
- `docs/domain/event-storming-sterilization-booking.md`
- `docs/domain/business-rules.md`

---

## 5. Out of scope (SCRUM-5)

- Modifying Cursor business rules  
- Full product features (initially)  
- Clinical decision-making logic  

---

## 6. Project layout

- `pyproject.toml`
- `src/enae_vet/app.py`
- `src/enae_vet/chatbot/server.py`
- `tests/`
- `docs/`

---

## 7. Getting started

bash
pip install -e ".[dev]"
pytest
uvicorn enae_vet.app:app --reload

## 8. Chatbot (SCRUM-6)

The chatbot evolved from the initial baseline:

LangChain-based chatbot
Session memory using session_id
Basic RAG integration
/rag_debug endpoint
Tool-ready structure
Run locally
set OPENAI_API_KEY=your_key_here
python -m enae_vet.chatbot.server

Open in browser:

http://localhost:5051

## 9. AI Chatbot (LangChain-based) — Current Implementation

The ENAE VET system includes an AI chatbot focused on veterinary sterilization assistance.

Architecture (AI layer)
LLM (Language Model)
Handles natural language understanding and responses
System Prompt
Defines behavior as veterinary assistant (non-diagnostic)
Session Memory (VET-10)
Maintains conversation context via session_id
RAG (Retrieval-Augmented Generation) (VET-11)
Source: preoperative instructions
Pipeline:
fetch
parse
inject into context
Tools (VET-12)
Availability (mock JSON)
Designed for future calendar integration
Backend endpoints
GET / → chatbot UI
GET /health → health check
POST /ask_bot → chatbot interaction
GET /rag_debug → debug RAG context
Example request
{
  "session_id": "uuid",
  "message": "Can I sterilize my dog if she is in heat?"
}
Example capabilities

The chatbot can:

Answer sterilization questions
Provide preoperative guidance
Detect risk situations
Maintain conversation context
Use RAG to improve responses
Important note
Informational only
Not a veterinary diagnosis
Escalates to human when needed

## 10. Future work

Real calendar integration (VET-13)
Advanced RAG pipeline
Database integration
Deployment improvements (Vercel)

