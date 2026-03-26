Architecture Overview
======================

This document describes the **target architecture** for ENAE VET as agreed in ticket `SCRUM-5` (see Jira SCRUM board).

## 1. High-level view

- **Web client (React/TypeScript)** consumes a backend API.
- **Backend API (FastAPI)** hosts all business logic and exposes REST endpoints (GraphQL optional later).
- **Relational database (PostgreSQL)** stores transactional data.
- **AuthN/AuthZ** manage users and roles.
- **Integrations** (email/WhatsApp, calendar, payments) are added as separate services or adapters.

## 2. Components and responsibilities

### 2.1 Frontend

- Renders views and user flows.
- Performs basic validation and session handling.
- Calls backend endpoints and surfaces validation / domain errors from the API.

### 2.2 Backend (API)

- Owns business rules and invariants (single source of truth).
- Validates input and enforces authorization.
- Coordinates persistence through the data access layer (SQLAlchemy).
- Exposes structured logs and, optionally, tracing/metrics.

### 2.3 Database

- PostgreSQL with a normalized relational model.
- Versioned migrations managed by Alembic.
- Future tables include (non-exhaustive, to be specified in later tickets):
  - Clients
  - Pets
  - Appointments
  - Services
  - Users and roles

## 3. Principles

- **Separation of concerns**: UI, API, and persistence are clearly separated.
- **Evolutionary architecture**: significant changes captured as ADRs in `docs/adr/`.
- **Security by default**: role-based access, least privilege, secrets in environment variables only.

## 4. Environments

- **Local**: development, usually via Docker and hot‑reload.
- **Staging**: pre‑production, integrated with external services where possible.
- **Production**: hardened configuration, observability, and backups.

Implementation details (schemas, endpoints, and workflows) will be added in subsequent tickets; this document only establishes the baseline target architecture.

