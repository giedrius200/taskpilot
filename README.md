# TaskPilot — Task Manager API (sample project for your CV)

[![CI](https://github.com/your-username/your-repo-name/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/your-repo-name/actions/workflows/ci.yml)

TaskPilot is a small FastAPI service showing modern Python backend skills: REST APIs, JWT auth, relational persistence, background tasks, and tests.

Features
- FastAPI HTTP endpoints with JWT authentication
- SQLite persistence via SQLModel (built on SQLAlchemy)
- Background task example (notification simulation)
- Unit tests using pytest and httpx AsyncClient
- Dockerfile for easy deployment

Quick start
1. Create a virtual env and activate it
2. Install dependencies: pip install -r requirements.txt
3. Run tests: pytest -q
4. Start API: uvicorn src.app:app --reload

Environment variables
- TASKPILOT_SECRET_KEY: recommended to set a secure secret for JWT signing (defaults to a placeholder)
- DATABASE_URL: optional; defaults to sqlite:///./test.db. Example: export DATABASE_URL="sqlite:///./taskpilot.db"

Docker
Build and run the Docker image:

    docker build -t taskpilot:latest .
    docker run -p 8000:8000 -e TASKPILOT_SECRET_KEY="your-secret" taskpilot:latest

What to highlight on your CV
- Implemented a REST API with FastAPI and pydantic/SQLModel for schema and ORM
- Added JWT authentication and password hashing (passlib + python-jose)
- Wrote unit tests covering auth and basic CRUD
