# Architecture

SecureLink uses a FastAPI backend, SQLAlchemy persistence, a Streamlit dashboard, and small attack simulator scripts.

```text
Client / Simulator / Dashboard
        |
        v
FastAPI API
        |
        +--> Auth service: bcrypt + JWT
        +--> Message service: AES-GCM + HMAC + RSA signatures
        +--> Detection service: replay and tamper checks
        |
        v
PostgreSQL or SQLite
```

The Docker setup runs PostgreSQL, the API, and the dashboard.

Production hardening adds Redis-backed rate limiting, Prometheus/Grafana monitoring, and a Caddy TLS reverse proxy on `https://localhost:8443`.
