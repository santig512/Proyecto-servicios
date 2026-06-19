import asyncio
import os
import subprocess
import sys

import asyncpg

from app.core.config import settings

DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.postgres_host()}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)


async def wait_for_database(retries: int = 30, delay: float = 2.0) -> None:
    last_error = None
    for _ in range(retries):
        try:
            conn = await asyncpg.connect(DATABASE_URL)
            await conn.close()
            return
        except Exception as exc:
            last_error = exc
            await asyncio.sleep(delay)
    raise RuntimeError(f"Database not ready: {last_error}")


def run_migrations() -> None:
    subprocess.run([sys.executable, "-m", "alembic", "-c", "alembic.ini", "upgrade", "head"], check=True)


def main() -> None:
    asyncio.run(wait_for_database())
    run_migrations()
    os.execvp(
        "uvicorn",
        [
            "uvicorn",
            "app.main:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
        ],
    )


if __name__ == "__main__":
    main()
