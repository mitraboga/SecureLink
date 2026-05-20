# SecureLink

## Executive Summary
SecureLink is a secure messaging and attack-detection platform that demonstrates applied cryptography, message authentication, replay protection, digital signatures, and IDS-style monitoring.

## Problem Statement
Sensitive application messages can be intercepted, modified, replayed, or forged when systems lack strong encryption, authentication, integrity checks, and audit logging. SecureLink models a safer communication flow and shows attacks being blocked.

## Real-World Incident Inspiration
This project is inspired by the 2024 Snowflake customer data theft campaign attributed by Mandiant to UNC5537. The campaign showed how stolen credentials, missing MFA, weak access controls, and limited anomaly detection can lead to large-scale cloud data theft and extortion.

## CS50 Cybersecurity Concepts Applied
- Password security
- Authentication
- Cryptography
- Hashing
- Secure communication
- Web application security
- Network security
- Incident response
- Attack prevention
- Security monitoring

## CSEN2071 Concepts Applied
- Unit 1: Security concepts, attacks, services, mechanisms
- Unit 2: AES symmetric encryption
- Unit 3: RSA and Diffie-Hellman
- Unit 4: SHA, HMAC, digital signatures
- Unit 5: TLS, firewalls, IDS/IPS concepts

## Architecture
FastAPI exposes authentication, key, message, and security APIs. SQLAlchemy persists users, encrypted messages, and security events. The Streamlit dashboard reads the API to visualize alerts. Attack simulator scripts call API endpoints to demonstrate blocked attacks.

Architecture assets:

- `assets/architecture.svg`
- `assets/attack-flow.svg`
- `assets/dashboard-preview.svg`
- `assets/architecture.png`
- `assets/attack-flow.png`
- `assets/dashboard-preview.png`

## Features
- User registration and login with bcrypt password hashing
- JWT access tokens
- AES-256-GCM encrypted messages
- HMAC-SHA256 integrity protection
- RSA-PSS digital signatures
- Diffie-Hellman shared-key demonstration
- Replay detection using message IDs, nonces, and timestamps
- Attack simulation endpoints and scripts
- Security event dashboard
- Prometheus metrics endpoint
- Security headers
- Redis-backed IP rate limiting with in-memory fallback
- Caddy TLS reverse proxy
- Alembic database migrations
- Docker Compose monitoring with Prometheus and Grafana

## API Endpoints
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `POST /keys/generate-rsa`
- `POST /keys/exchange-dh`
- `GET /keys/public/{user_id}`
- `POST /messages/send`
- `GET /messages/inbox`
- `GET /messages/{message_id}`
- `GET /security/events`
- `GET /security/summary`
- `POST /security/simulate/replay`
- `POST /security/simulate/tamper`
- `POST /security/simulate/invalid-signature`
- `POST /security/simulate/mitm`
- `GET /health`
- `GET /ready`
- `GET /metrics`

## Local Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker Setup
```bash
docker compose up --build
```

Services:

- API: `http://localhost:8010`
- API docs: `http://localhost:8010/docs`
- Dashboard: `http://localhost:8501`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3010` with `admin` / `securelink`
- TLS reverse proxy: `https://localhost:8443` using Caddy's internal local certificate authority

## Demo Walkthrough
1. Register Alice and Bob.
2. Log in as Alice.
3. Send Bob a secure message.
4. Fetch Bob's inbox and verify the plaintext is returned only after integrity, signature, and replay checks pass.
5. Run replay and tamper simulations.
6. Open the Streamlit dashboard and show logged security events.

## Testing
```bash
pytest
```

CI is configured in `.github/workflows/ci.yml`.

Optional Dockerized PostgreSQL integration check:

```bash
docker compose up -d db redis
$env:SECURELINK_POSTGRES_TEST_URL="postgresql+psycopg2://securelink:securelink@localhost:15432/securelink"
pytest tests/test_postgres_integration.py
```

## Production Workflow
1. Copy `.env.example` to `.env` and replace development secrets.
2. Run `docker compose up --build`.
3. Register demo users through `/docs`.
4. Send a secure message.
5. Run attack simulator scripts or simulation endpoints.
6. Review events in Streamlit.
7. Review metrics in Prometheus and Grafana.
8. Run `pytest` before pushing changes.

The API container runs `alembic upgrade head` on startup before launching Uvicorn.

Full workflow shortcut:

```bash
python attack_simulator/full_demo.py --api http://localhost:8010
```

## Manual Swagger Demo
Open `http://localhost:8010/docs`.

1. Register Alice with `POST /auth/register`.
2. Register Bob with `POST /auth/register`.
3. Login Alice with `POST /auth/login`.
4. Click `Authorize` and paste `Bearer <alice_token>`.
5. Send Bob a message with `POST /messages/send` using Bob's `receiver_id`.
6. Login Bob and authorize Swagger with Bob's token.
7. Read Bob's inbox with `GET /messages/inbox`.
8. Trigger replay, tamper, invalid-signature, and MITM simulations.
9. Review `/security/events`, `/security/summary`, Streamlit, Prometheus, and Grafana.

Example message body:

```json
{
  "receiver_id": 2,
  "plaintext": "Hello Bob, this is a secure encrypted message."
}
```

## Security Limitations
This is an educational system. Private keys are stored encrypted with an application secret for demonstration, key rotation is minimal, TLS uses Caddy's internal local certificate authority in Docker, and DH-derived conversation keys are generated server-side for classroom clarity rather than through a full client-held end-to-end key ceremony.

## Future Improvements
- Hardware-backed key storage
- Redis clustering or managed Redis for multi-instance rate limiting
- Full client-held end-to-end key exchange
- Key rotation and revocation workflows
- Deployment manifests for a cloud target

## Presentation Assets
Generated presentation file:

- `docs/SecureLink_presentation.pptx`

Regenerate PNG assets and the slide deck:

```bash
python scripts/generate_presentation_assets.py
```

## Author
Add your name, edX username, and GitHub username before submission.
