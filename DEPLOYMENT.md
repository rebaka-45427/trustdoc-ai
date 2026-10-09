# Deployment Guide

TrustDoc AI is designed for modern cloud deployment.

## Backend (FastAPI / Render / Railway)
1. Fork or clone this repository to your GitHub account.
2. Link the repository to your PaaS provider (Render, Railway, Fly.io).
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Configure Environment Variables:
   - `DATABASE_URL`: Your managed PostgreSQL connection string.
   - `JWT_SECRET`: A secure random string.
   - `HMAC_SECRET`: A secure random string for QR verification generation.
   - `PUBLIC_BASE_URL`: The domain where your public frontend will live (e.g., `https://trustdoc-ai.example.com`).
   - `ENVIRONMENT`: `production`

## Frontend (React / Vercel)
*(Note: Frontend is pending implementation. Once built, use these steps)*
1. Link the frontend directory to Vercel.
2. Set the framework preset to Vite/React.
3. Add `VITE_API_BASE_URL` pointing to your deployed backend domain.
4. Deploy.

## Database
- Use a managed PostgreSQL instance (Supabase, Neon, AWS RDS, Render Postgres).
- Run `alembic upgrade head` as a release command or manually via SSH/console to apply migrations.
