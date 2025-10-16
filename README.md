# TaskPilot — Task Manager API

Small FastAPI sample project demonstrating a REST API with JWT auth, persistence via SQLModel, background tasks and tests. Suitable as a CV/sample project.

Badges
- (optional) Add CI / coverage badges after you create the GitHub repo and CI workflow.

Quick highlights
- FastAPI endpoints with JWT authentication
- SQLite persistence via SQLModel (SQLAlchemy)
- Background task example (notification simulation)
- Unit tests using pytest + httpx AsyncClient
- Dockerfile for containerized runs

Requirements
- Python 3.10+
- See `requirements.txt` for exact packages

Local setup (developer)
1. In the project root create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run tests:

```powershell
pytest -q
```

4. Start the API server:

```powershell
uvicorn src.app:app --reload --port 8000
```

Configuration
- TASKPILOT_SECRET_KEY — secret for JWT (set in environment)
- DATABASE_URL — optional SQLAlchemy URL (defaults to sqlite:///./test.db)

Docker
Build and run with Docker:

```powershell
docker build -t taskpilot:latest .
docker run -p 8000:8000 -e TASKPILOT_SECRET_KEY="your-secret" taskpilot:latest
```

How the app works (short)
- Authentication: JWT tokens issued on login; passwords hashed with bcrypt (passlib).
- Persistence: SQLModel models in `src/models.py` persisted to SQLite by default.
- API: REST endpoints for tasks and auth are implemented in `src/app.py` and `src/auth.py`.
- Background tasks: a sample background job simulates notifications.

Showing the app to someone — simple demo steps
1. Local demo (fastest): run the server locally (see Local setup) and open http://localhost:8000/docs to show the interactive OpenAPI docs. Use the UI to call endpoints and authenticate.
2. Container demo: build the Docker image and run it; share your machine IP and port (or use ngrok) to let others access it.
3. Deploy (recommended for remote sharing): push the repo to GitHub and deploy to a platform (Render, Fly, Heroku, or GitHub Actions + cloud). See the "Deploying" section below.

Endpoints to highlight during a demo
- POST /auth/register — create a user (email + password)
- POST /auth/login — return an access JWT
- GET /tasks — (auth) list tasks
- POST /tasks — (auth) create task
- DELETE /tasks/{id} — (auth) delete task

Create a GitHub repo and push (commands)
If you have the GitHub CLI (`gh`) authenticated, this single command creates a public repo and pushes your code:

```powershell
gh repo create taskpilot --public --source=. --remote=origin --push
```

Manual sequence (if `gh` is not available):

```powershell
git init
git branch -M main
git add .
git commit -m "Initial commit"
# create a repo on GitHub via the website, then add the remote shown on that page
git remote add origin https://github.com/<your-username>/taskpilot.git
git push -u origin main
```

Notes on secrets
- Never commit real secrets (TASKPILOT_SECRET_KEY) to the repository. Use environment variables or GitHub Secrets for CI/deploy.

Running tests and CI
- Tests live in `tests/`. Running `pytest -q` runs the suite locally.
- A GitHub Actions workflow is included to run the test suite on pushes and pull requests.

Troubleshooting
- If tests fail locally, ensure you installed `requirements.txt` in the active virtual environment.
- If port 8000 is busy, change the `--port` for uvicorn or stop the conflicting process.

Contact / Next steps
- I can: add a CI workflow, help you deploy to Render/Fly/Heroku, or add README badges. Say which one you'd like.
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
