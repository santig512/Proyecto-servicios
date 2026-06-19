Local development

Backend (venv):

1. Create a virtualenv and install deps

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
```

2. Create `.env` in `backend/` (sample already provided).
3. Run migrations (requires a running Postgres)

```bash
cd backend
alembic -c alembic.ini upgrade head
```

4. Run the backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend (dev):

```bash
cd frontend
npm install
npm run dev
```

Docker (recommended):

```bash
# From repository root
docker-compose up --build
```

Notes & troubleshooting

- If Docker Compose fails, run containers one-by-one and inspect logs:

```bash
docker-compose up db
# wait until postgres ready
docker-compose up backend
```

- The backend contains `app/scripts/startup.py` that waits for Postgres and runs alembic migrations automatically when using Docker.
- The frontend proxies `/api` to `http://localhost:8000` in local dev (`vite.config.js`).

S3 / Uploads

- To enable S3 uploads set the `S3_BUCKET` environment variable in `backend/.env` and provide AWS credentials via environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, optionally `AWS_REGION`).

Production CI

- The release workflow (`.github/workflows/release.yml`) builds and pushes images to GitHub Container Registry (`ghcr.io`). Ensure repository has appropriate permissions and secrets are configured. The workflow uses `GITHUB_TOKEN` by default for GHCR auth.

CI

- A basic GitHub Actions pipeline is provided in `.github/workflows/ci.yml`.

Next steps (recommended)

- Expand unit tests for services and repositories.
- Add production secrets (do NOT store in `.env` in repo).
- Integrate a real payment provider (Stripe) and secure webhook signing.
- Optionally add S3 storage for uploads.
