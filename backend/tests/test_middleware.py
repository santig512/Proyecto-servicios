from app.middleware.ratelimit import SimpleRateLimiter


def test_rate_limiter_allows_and_blocks():
    limiter = SimpleRateLimiter(limit=2, window_seconds=1)
    key = 'test:key'
    assert limiter.is_allowed(key) is True
    assert limiter.is_allowed(key) is True
    # third should be blocked
    assert limiter.is_allowed(key) is False

    # after window passes, should allow again
    import time
    time.sleep(1.1)
    assert limiter.is_allowed(key) is True
