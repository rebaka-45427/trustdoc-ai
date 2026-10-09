# Running TrustDoc AI

## Prerequisites
- Python 3.10+
- PostgreSQL (or SQLite for dev)
- Node.js (for frontend)

## 1. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## 2. Frontend Setup (If Available)
```bash
cd frontend
npm install
npm run dev
```

## 3. Testing
Access API docs at `http://localhost:8000/docs`.
Use the `/api/auth/register` to create a user.

## Deployment Instructions
**Backend**: Use Render or Railway. Connect the GitHub repo, set the Build command to `pip install -r requirements.txt` and Start command to `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Add the environment variables including `DATABASE_URL`.
**Frontend**: Deploy to Vercel. Connect the repo and add the API base URL.
