import pytest
from app.auth.utils import hash_password, verify_password, create_access_token, decode_token
from datetime import timedelta

def test_password_hash_and_verify():
    pw = 'secret1234'
    h = hash_password(pw)
    assert h != pw
    assert verify_password(pw, h)

def test_token_create_and_decode():
    token = create_access_token('42', expires_delta=timedelta(minutes=1))
    payload = decode_token(token)
    assert payload is not None
    assert payload.get('sub') == '42'

def test_decode_invalid_token():
    assert decode_token('not-a-token') is None
