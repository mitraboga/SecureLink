from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import auth_routes, key_routes, message_routes, security_routes
from app.database import engine, init_db
from app.utils.metrics import metrics_middleware, metrics_response
from app.utils.rate_limit import rate_limit_middleware
from app.utils.security_headers import security_headers_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="SecureLink",
    description="Encrypted messaging and attack-detection platform",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    with engine.connect():
        return {"status": "ready"}


@app.get("/metrics")
def metrics():
    return metrics_response()


app.middleware("http")(metrics_middleware)
app.middleware("http")(rate_limit_middleware)
app.middleware("http")(security_headers_middleware)
app.include_router(auth_routes.router)
app.include_router(key_routes.router)
app.include_router(message_routes.router)
app.include_router(security_routes.router)
