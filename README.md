ENAE VET
========

Baseline documentation and project skeleton for the ENAE VET system. This ticket (`SCRUM-5` on the Jira SCRUM board) focuses **only** on architecture, tech stack, workflow, and documentation structure. **No product features or veterinary business rules are implemented here.**

## 1. Target architecture (high‑level)

- **Web client (frontend)**: React/TypeScript UI for reception/admin users and, later, veterinarians.
- **Backend API (FastAPI)**: Single source of truth for business logic, validation, and authorization.
- **Relational database (PostgreSQL)**: Transactional persistence (clients, pets, appointments, services, users/roles, etc. – to be modeled in future tickets).
- **Authentication & authorization**: Role-based access control, implemented in future tickets.
- **Integrations (future)**: Email/WhatsApp notifications, calendar, payments (if required).

### Separation of layers

- **Frontend**: Presentation, basic form validation, session handling, API consumption, and error display.
- **Backend**: Business rules, validation, authorization, persistence orchestration, observability (structured logs, tracing where needed).
- **Database**: Normalized relational model with versioned migrations.

### Environments

- **Local**: Developer machines (this repo + Docker).
- **Staging**: Pre‑production, integration testing.
- **Production**: Live environment.

### Principles

- **Single source of truth in backend**: All business rules live in the API, not duplicated in the client.
- **Evolutionary architecture**: Changes are captured via Architecture Decision Records (ADRs) under `docs/adr/`.
- **Security by default**: Least privilege, secrets via environment variables, no secrets in the repo.

For more detail, see `docs/architecture/overview.md`.

## 2. Baseline tech stack

### Backend

- **Language**: Python 3.12+
- **Framework**: FastAPI
- **Validation / schemas**: Pydantic
- **ORM & migrations**: SQLAlchemy + Alembic
- **Database**: PostgreSQL
- **Testing**: pytest (+ `pytest-cov`)
- **Linting / formatting**: Ruff *or* Black + isort (final choice to be captured in an ADR)

### Frontend (planned)

- **Language**: TypeScript
- **Framework**: React (Next.js optional for SSR/SEO)
- **Styling**: TailwindCSS
- **Testing**: Playwright (e2e) + Vitest/Jest (unit)

### Infra / DevOps

- **Containers**: Docker + docker compose
- **CI**: GitHub Actions (build, lint, tests)
- **Secrets**: Environment variables (never committed)

### Documentation

- **Format**: Markdown in‑repo
- **ADRs**: `docs/adr/` for architecture decisions

## 3. Workflow (SCRUM + Jira)

- **Board**: Jira SCRUM board for the ENAE VET project (`SCRUM` project key).
- **States**:
  - **To Do** → **In Progress** → **Code Review** → **QA / Validation** → **Done**.
- **Definition of Ready**:
  - Clear objective and context.
  - Verifiable acceptance criteria.
  - Dependencies and risks visible.
  - Priority (and estimation, if used) defined.
- **Branching**:
  - One branch per ticket, e.g. `feature/SCRUM-5-readme-and-docs`.
  - PRs target `main`.
- **Definition of Done (project)**:
  - Changes merged into `main`.
  - Validation completed (tests/QA).
  - Documentation updated when relevant.

## 4. Documentation index

Core documentation entry points for ENAE VET:

- `README.md` (this file): high‑level overview, stack, workflow, and quickstart.
- **Domain (SCRUM-14 / VET-14)** — clínica / esterilización / agenda:
  - [`docs/domain/glossary-and-preparation.md`](docs/domain/glossary-and-preparation.md) — glosario y reglas preparatorias.
  - [`docs/domain/event-storming-sterilization-booking.md`](docs/domain/event-storming-sterilization-booking.md) — Event Storming (Mermaid) del flujo de reserva.
  - [`docs/domain/business-rules.md`](docs/domain/business-rules.md) — reglas operativas (Tetris, 240 min/día, derivaciones).
- `docs/architecture/overview.md`: system architecture details.
- `docs/architecture/c4/`: C4 diagrams (Context / Container / Component), to be added.
- `docs/adr/`: Architecture Decision Records.
- `docs/api/`: API contracts, endpoints, and examples.
- `docs/db/schema.md`: database schema and data rules.
- `docs/runbook/`: operational documentation (deployments, troubleshooting).
- `docs/security/`: security posture, roles, permissions, and secrets handling.

## 5. Out of scope for SCRUM-5

- Modifying **Cursor** business rules or internal automation.
- Implementing ENAE VET product features (scheduling, records, billing, etc.).
- Defining veterinary clinical workflows or medical decision logic.

Those items will be implemented in separate tickets.

## 6. Project layout (initial)

After this ticket, the repo contains a minimal but testable backend skeleton:

- `pyproject.toml` – Python project metadata and dependencies.
- `src/enae_vet/app.py` – FastAPI application with a basic health endpoint.
- `tests/test_health.py` – Smoke test for the health endpoint.
- `docs/…` – Documentation structure described above.

## 7. Getting started (local, backend only)

1. **Prerequisites**
   - Python 3.12+
   - `pip` (or a virtual environment / tool such as `uv`, `poetry`, or `pipenv`)

2. **Install dependencies**

   ```bash
   # From the repo root, using a virtual environment is recommended
   pip install -e ".[dev]"
   ```

3. **Run tests**

   ```bash
   pytest
   ```

4. **Run the API locally (development)**

   ```bash
   uvicorn enae_vet.app:app --reload
   ```

## 8. Simple chatbot run (SCRUM-6)

The initial chatbot for `SCRUM-6` is intentionally minimal:
- LangChain in Python.
- No memory.
- No RAG.
- No tools.

Set your OpenAI key and run the Flask service:

```bash
set OPENAI_API_KEY=your_key_here
python -m enae_vet.chatbot.server
```

Then open `http://localhost:5000` and send a message through the basic chat form.

> Note: Docker, full DB setup, and CI workflows will be added in future tickets, following this baseline architecture and workflow.

