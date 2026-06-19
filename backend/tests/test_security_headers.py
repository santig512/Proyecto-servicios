from starlette.testclient import TestClient
from app.main import app


def test_security_headers_present():
    client = TestClient(app)
    r = client.get('/health')
    assert r.status_code == 200
    assert 'X-Frame-Options' in r.headers
    assert 'X-Content-Type-Options' in r.headers
    assert 'Content-Security-Policy' in r.headers
