# TaskPilot — Task Manager API

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

Note about login endpoints and Swagger UI
- This project exposes two login endpoints intentionally:
	- `POST /login` expects JSON body {"username":"...","password":"..."} and is used by tests and API clients.
	- `POST /login-form` accepts form-encoded username/password (used by the Swagger UI OAuth2 "password" flow / Authorize dialog).
	When using the interactive docs at `/docs`, the Authorize dialog will POST form data to `/login-form`. For command-line or programmatic login use `/login` with a JSON payload.


