from starlette.requests import Request
from starlette.responses import Response


async def security_headers_middleware(request: Request, call_next):
    response: Response = await call_next(request)
    # Basic security headers
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Permissions-Policy'] = 'geolocation=()'
    # Content-Security-Policy minimal
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline'"
    return response
