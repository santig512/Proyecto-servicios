from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth as auth_router
from app.api import users as users_router
from app.api import services as services_router
from app.api import quotations as quotations_router
from app.api import invoices as invoices_router
from app.api import payments as payments_router
from app.api import chat as chat_router
from app.api import notifications as notifications_router
from app.api import admin_users as admin_users_router
from app.api import reviews as reviews_router
from app.websocket import endpoint as websocket_endpoint
from app.api import uploads as uploads_router
from app.middleware.ratelimit import SimpleRateLimiter, rate_limit_middleware_factory
from app.middleware.security_headers import security_headers_middleware
from app.monitoring import metrics_endpoint
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="Proyecto Servicios API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register security middlewares
limiter = SimpleRateLimiter(limit=120, window_seconds=60)
app.middleware('http')(rate_limit_middleware_factory(limiter))
app.middleware('http')(security_headers_middleware)

app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users_router.router, prefix="/api/v1/users", tags=["users"])
app.include_router(services_router.router, prefix="/api/v1/services", tags=["services"])
app.include_router(quotations_router.router, prefix="/api/v1/quotations", tags=["quotations"])
app.include_router(invoices_router.router, prefix="/api/v1/invoices", tags=["invoices"])
app.include_router(payments_router.router, prefix="/api/v1/payments", tags=["payments"])
app.include_router(chat_router.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(notifications_router.router, prefix="/api/v1/notifications", tags=["notifications"])
app.include_router(admin_users_router.router, prefix="/api/v1/admin/users", tags=["admin-users"])
app.include_router(reviews_router.router, prefix="/api/v1/reviews", tags=["reviews"])

# include websocket routes
app.include_router(websocket_endpoint.router)
app.include_router(uploads_router.router, prefix="/api/v1/uploads", tags=["uploads"])

# metrics
@app.get('/metrics')
async def _metrics():
    return metrics_endpoint()

# serve uploaded files
UPLOAD_PATH = Path(__file__).resolve().parents[1] / 'uploads'
app.mount("/uploads", StaticFiles(directory=UPLOAD_PATH), name="uploads")


@app.get("/health")
async def health():
    return {"status": "ok"}
