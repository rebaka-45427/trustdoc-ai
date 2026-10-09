@echo off
echo Starting TrustDoc AI Local Environment...

cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

echo Running Database Migrations...
alembic upgrade head

echo Starting FastAPI Backend...
start cmd /k "title TrustDoc API && uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo TrustDoc AI Backend is running at http://127.0.0.1:8000
echo API Docs available at http://127.0.0.1:8000/docs
pause
