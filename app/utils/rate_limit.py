import time
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable

from fastapi import status
from redis import Redis
from redis.exceptions import RedisError
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.config import get_settings

_requests: dict[str, deque[float]] = defaultdict(deque)
_redis_client: Redis | None = None


def _client_key(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


async def rate_limit_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    if request.url.path in {"/health", "/ready", "/metrics"}:
        return await call_next(request)

    settings = get_settings()
    key = _client_key(request)
    if settings.redis_url:
        try:
            response = _redis_rate_limit(key)
            if response:
                return response
            return await call_next(request)
        except RedisError:
            pass

    now = time.monotonic()
    window_start = now - settings.rate_limit_window_seconds
    hits = _requests[key]

    while hits and hits[0] < window_start:
        hits.popleft()

    if len(hits) >= settings.rate_limit_requests:
        return JSONResponse(
            {"detail": "Rate limit exceeded"},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            headers={"Retry-After": str(settings.rate_limit_window_seconds)},
        )

    hits.append(now)
    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(settings.rate_limit_requests)
    response.headers["X-RateLimit-Remaining"] = str(max(settings.rate_limit_requests - len(hits), 0))
    return response


def _redis() -> Redis:
    global _redis_client
    settings = get_settings()
    if _redis_client is None:
        _redis_client = Redis.from_url(settings.redis_url or "", decode_responses=True)
    return _redis_client


def _redis_rate_limit(key: str) -> JSONResponse | None:
    settings = get_settings()
    redis_key = f"securelink:ratelimit:{key}"
    count = _redis().incr(redis_key)
    if count == 1:
        _redis().expire(redis_key, settings.rate_limit_window_seconds)
    if count > settings.rate_limit_requests:
        return JSONResponse(
            {"detail": "Rate limit exceeded"},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            headers={"Retry-After": str(settings.rate_limit_window_seconds)},
        )
    return None
