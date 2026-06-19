# Backend - Proyecto Servicios

Requisitos: Python 3.11, PostgreSQL, Redis

Instalación local:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
# Si corres fuera de Docker, asegúrate de que PostgreSQL esté disponible en localhost
# Si usas Docker Compose, el backend recibirá la configuración del contenedor
alembic -c alembic.ini upgrade head
python -m app.scripts.seed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Celery:

```bash
celery -A app.core.celery_app.celery worker --loglevel=info -Q notifications
```

API base: `http://localhost:8000`
