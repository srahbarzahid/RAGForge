# RAGForge

RAGForge is a private document intelligence portal. Its planned workflow is sign in, create a knowledge base, upload PDF/DOCX/TXT files, process and index them, then ask questions with source citations. The architecture and module order are defined in [`Docs/00_README_PROJECT_MASTER_PLAN.md`](Docs/00_README_PROJECT_MASTER_PLAN.md) and [`Docs/07_MODULE_BY_MODULE_EXECUTION_PLAN.md`](Docs/07_MODULE_BY_MODULE_EXECUTION_PLAN.md).

## Current state

Module 0 and Module 1 are implemented. Module 1 has Supabase email/password Auth pages, live JWT verification, and PostgreSQL connections through FastAPI SQLAlchemy and a server-only Next.js Prisma Client. Confirmation email and SMTP setup are deferred. Application tables, uploads, retrieval, chat, and infrastructure integrations are scheduled for later modules. See [`Docs/implementation/001-module-1.md`](Docs/implementation/001-module-1.md) for setup and verification.

## Stack and boundaries

- Frontend: Next.js App Router, React, JavaScript, Tailwind CSS, shadcn/ui, and server-only Prisma.
- API: Python, FastAPI. Supabase Auth and PostgreSQL connection code is in Module 1; application tables arrive in Module 2.
- Planned supporting services: Qdrant vectors, private object storage, Redis, Celery, Kafka, LangGraph, and LLM providers in the order specified by the module execution plan.
- Frontend browser code must contain only public Supabase configuration. Private credentials belong on the server.

## Run locally

Requirements: Python 3.12+, Node.js 20.9+, npm. On Windows PowerShell, use `npm.cmd` and `npx.cmd` if script execution blocks `npm.ps1`.

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install -r backend/requirements-dev.txt
cd backend
.venv/Scripts/python.exe -m uvicorn app.main:app --reload
```

In a second terminal:

```powershell
cd frontend
npm.cmd ci
npm.cmd run dev
```

Open <http://localhost:3000> and <http://localhost:8000/health>. The API docs are at <http://localhost:8000/docs>.

To run checks, execute `python -m ruff check .`, `python -m ruff format --check .`, and `python -m pytest` from `backend`, then `npm.cmd run lint`, `npm.cmd run format:check`, and `npm.cmd run build` from `frontend`. On systems with GNU Make, equivalent targets are in the root `Makefile`.

## Configuration

Copy `.env.example` to `.env` and set up `frontend/.env.local` to connect a Supabase project. Set `DATABASE_URL` in both ignored files so FastAPI and server-only Prisma can connect. Keep actual credentials out of Git; only `NEXT_PUBLIC_*` settings reach the browser. The Module 1 setup steps are in [`Docs/implementation/001-module-1.md`](Docs/implementation/001-module-1.md).
