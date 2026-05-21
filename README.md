<div align="center">

# 🔐 SecureLink 🪪

### Secure Messaging, Applied Cryptography, Attack Simulation & Security Monitoring Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%2B-blue?logo=python">
  <img src="https://img.shields.io/badge/FastAPI-Security_API-009688?logo=fastapi">
  <img src="https://img.shields.io/badge/PostgreSQL-Persistent_Storage-336791?logo=postgresql">
  <img src="https://img.shields.io/badge/Redis-Rate_Limiting-DC382D?logo=redis">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker">
  <img src="https://img.shields.io/badge/Streamlit-Security_Dashboard-FF4B4B?logo=streamlit">
  <img src="https://img.shields.io/badge/Prometheus-Metrics-E6522C?logo=prometheus">
  <img src="https://img.shields.io/badge/Grafana-Observability-F46800?logo=grafana">
  <img src="https://img.shields.io/badge/Caddy-TLS_Reverse_Proxy-1F88C0">
  <img src="https://img.shields.io/badge/Security-AES--GCM%20%7C%20HMAC%20%7C%20RSA%20%7C%20DH-success">
  <img src="https://img.shields.io/badge/CS50-Cybersecurity-black">
</p>

<p align="center">
  <img src="assets/dashboard-preview.png" width="100%">
</p>

</div>

---

# 🚀 Executive Summary

**SecureLink** is a secure messaging and attack-detection platform that demonstrates applied cryptography, authentication, message integrity, replay protection, digital signatures, TLS termination, rate limiting, security telemetry, and IDS-style monitoring.

The system models a safer communication workflow where messages are encrypted, authenticated, signed, validated, monitored, and protected against common attack classes such as replay, tampering, invalid signatures, and simulated man-in-the-middle behavior.

This project was built as a **CS50 Cybersecurity final project** and extended into a production-style secure systems engineering portfolio project.

It demonstrates how cybersecurity concepts move from theory into a working application architecture.

---

# 🧩 Problem Statement

Modern applications exchange sensitive messages across networks, APIs, browsers, services, databases, and third-party infrastructure.

Without layered defenses, those messages can be:

- intercepted
- modified
- replayed
- forged
- exposed through weak authentication
- abused through missing rate limits
- left invisible due to poor monitoring

**SecureLink** addresses this by combining secure communication primitives with an observable attack-detection workflow.

The goal is not just to encrypt data.

The goal is to show how a real secure system requires:

- authentication
- authorization
- confidentiality
- integrity
- non-repudiation
- replay protection
- transport security
- auditability
- monitoring
- incident visibility

---

# 🌍 Real-World Incident Inspiration

SecureLink is partly inspired by the **2024 Snowflake customer data theft campaign** attributed by Mandiant to UNC5537.

That campaign showed how stolen credentials, weak access controls, missing MFA, and limited anomaly detection can lead to large-scale cloud data theft and extortion.

The lesson is powerful:

> Encryption matters, but identity, access control, monitoring, and incident response matter just as much.

SecureLink focuses on the defensive side of that lesson by implementing a layered security model for secure application messaging.

---

# 🧠 CS50 Cybersecurity Concepts Applied

This project directly connects to the major themes from **CS50 Cybersecurity**.

## 0. Securing Accounts

SecureLink implements authentication controls designed to reduce account compromise risk.

### Applied Concepts

- User registration
- Login workflows
- Password hashing with bcrypt
- JWT access tokens
- Authenticated API routes
- Current-user lookup through `/auth/me`

### Project Implementation

```text
POST /auth/register
POST /auth/login
GET  /auth/me
```

Passwords are never stored in plaintext. Instead, they are hashed before persistence, helping protect users even if database contents are exposed.

---

## 1. Securing Data

SecureLink protects message confidentiality and integrity using modern cryptographic primitives.

### Applied Concepts

- Symmetric encryption
- Message authentication
- Hashing
- Digital signatures
- Secure key exchange
- Integrity validation

### Project Implementation

| Security Goal | Implementation |
|---|---|
| Confidentiality | AES-256-GCM encrypted messages |
| Integrity | HMAC-SHA256 validation |
| Authenticity | RSA-PSS digital signatures |
| Key exchange demo | Diffie-Hellman shared-key workflow |
| Replay prevention | Message IDs, nonces, and timestamps |

The project demonstrates that secure data protection requires multiple layers.

Encryption protects content.

HMAC protects integrity.

Signatures help prove origin.

Replay protection prevents old messages from being reused maliciously.

---

## 2. Securing Systems

SecureLink includes infrastructure-level security controls beyond application logic.

### Applied Concepts

- TLS
- Reverse proxying
- Service readiness
- Containerized infrastructure
- Monitoring
- Observability
- Rate limiting

### Project Implementation

- Docker Compose service orchestration
- Caddy TLS reverse proxy
- PostgreSQL persistence
- Redis-backed IP rate limiting
- In-memory fallback rate limiting
- `/health` and `/ready` checks
- Prometheus `/metrics`
- Grafana monitoring stack

This makes SecureLink more than a script.

It behaves like a real deployed security service.

---

## 3. Securing Software

SecureLink demonstrates secure software design through attack simulation, validation, and defensive coding patterns.

### Applied Concepts

- Secure API design
- Input validation
- Attack simulation
- Tamper detection
- Replay detection
- Invalid-signature detection
- Security event logging

### Project Implementation

```text
POST /security/simulate/replay
POST /security/simulate/tamper
POST /security/simulate/invalid-signature
POST /security/simulate/mitm
```

The attack simulator allows the system to demonstrate not only normal behavior, but also how malicious behavior is detected and logged.

This is important because secure software should be testable against adversarial scenarios.

---

## 4. Preserving Privacy

SecureLink is designed around reducing unnecessary exposure of sensitive communication data.

### Applied Concepts

- Encrypted message storage
- Authenticated access
- Limited visibility
- Security event audit trail
- Privacy-aware design

### Project Implementation

Messages are stored encrypted, accessed only through authenticated workflows, and inspected through controlled API paths.

The dashboard visualizes security events without exposing unnecessary plaintext message contents.

The broader privacy lesson:

> Data privacy is not only about hiding information. It is about controlling who can access it, when they can access it, and how that access is monitored.

---

# 🎓 CSEN2071 Concepts Applied

SecureLink also maps directly to core cybersecurity and cryptography concepts from CSEN2071.

| Unit | Concept | SecureLink Application |
|---|---|---|
| Unit 1 | Security concepts, attacks, services, mechanisms | Attack simulation, CIA triad, security monitoring |
| Unit 2 | AES symmetric encryption | AES-256-GCM encrypted messages |
| Unit 3 | RSA and Diffie-Hellman | RSA-PSS signatures and DH shared-key demo |
| Unit 4 | SHA, HMAC, digital signatures | HMAC-SHA256 and signature validation |
| Unit 5 | TLS, firewalls, IDS/IPS concepts | Caddy TLS proxy, rate limiting, security dashboard |

---

# 🏗️ Architecture

<p align="center">
  <img src="assets/architecture.png" width="100%">
</p>

SecureLink uses a modular architecture built around secure APIs, persistent storage, attack simulation, and observability.

## System Flow

```text
Client / Swagger / Simulator
        ↓
Caddy TLS Reverse Proxy
        ↓
FastAPI Security API
        ↓
Authentication + Crypto + Validation Layer
        ↓
PostgreSQL + SQLAlchemy
        ↓
Security Events + Metrics
        ↓
Streamlit Dashboard + Prometheus + Grafana
```

## Core Components

| Component | Responsibility |
|---|---|
| FastAPI API | Authentication, messaging, keys, security simulation |
| SQLAlchemy | ORM for users, messages, events |
| PostgreSQL | Persistent storage |
| Redis | IP rate limiting |
| Caddy | TLS reverse proxy |
| Streamlit | Security event dashboard |
| Prometheus | Metrics collection |
| Grafana | Observability dashboards |
| Attack Simulator | Replay, tamper, invalid-signature, MITM demos |

---

# 🧨 Attack Flow

<p align="center">
  <img src="assets/attack-flow.png" width="100%">
</p>

SecureLink includes attack simulation workflows to demonstrate how the system detects suspicious behavior.

## Simulated Attacks

| Attack | What It Tests |
|---|---|
| Replay Attack | Reusing a previously valid message |
| Tampering | Modifying encrypted or signed message data |
| Invalid Signature | Forged or corrupted digital signatures |
| MITM Simulation | Unsafe communication assumptions and key exchange risks |

Each simulation produces a security event that can be reviewed through the API, dashboard, and monitoring stack.

---

# 🔐 Security Features

## Authentication

- User registration
- Login
- JWT-based session access
- Protected API routes
- Current-user identity endpoint

## Cryptography

- AES-256-GCM encrypted messages
- HMAC-SHA256 integrity protection
- RSA-PSS digital signatures
- Diffie-Hellman shared-key demonstration
- Secure random nonces
- Timestamp validation

## Attack Detection

- Replay detection
- Tamper detection
- Invalid-signature detection
- MITM simulation
- IDS-style security events

## Infrastructure Security

- TLS reverse proxy through Caddy
- Redis-backed rate limiting
- Security headers
- PostgreSQL persistence
- Alembic migrations
- Docker Compose service orchestration

## Observability

- Streamlit dashboard
- Prometheus metrics
- Grafana monitoring
- `/health`
- `/ready`
- `/metrics`

---

# 🌐 API Endpoints

## Authentication

```text
POST /auth/register
POST /auth/login
GET  /auth/me
```

## Key Management

```text
POST /keys/generate-rsa
POST /keys/exchange-dh
GET  /keys/public/{user_id}
```

## Secure Messaging

```text
POST /messages/send
GET  /messages/inbox
GET  /messages/{message_id}
```

## Security Monitoring

```text
GET  /security/events
GET  /security/summary
POST /security/simulate/replay
POST /security/simulate/tamper
POST /security/simulate/invalid-signature
POST /security/simulate/mitm
```

## Platform Health

```text
GET /health
GET /ready
GET /metrics
```

---

# ⚙️ Local Setup

Use Python 3.12.

## Create Virtual Environment

```bash
python -m venv .venv
```

## Activate Environment

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run API Locally

```bash
uvicorn app.main:app --reload
```

---

# 🐳 Docker Setup

```bash
docker compose up --build
```

## Services

| Service | URL |
|---|---|
| API | `http://localhost:8010` |
| API Docs | `http://localhost:8010/docs` |
| Dashboard | `http://localhost:8501` |
| Prometheus | `http://localhost:9090` |
| Grafana | `http://localhost:3010` |
| TLS Reverse Proxy | `https://localhost:8443` |

Grafana login:

```text
admin / securelink
```

TLS uses Caddy's internal local certificate authority in Docker.

---

# 🧭 Interfaces: Swagger UI vs Streamlit Dashboard

SecureLink uses two different browser-based interfaces for two different jobs.

Both connect to the same FastAPI backend, but they serve different purposes.

```text
Browser
  |
  |-- Swagger UI: http://localhost:8010/docs
  |       API testing console
  |       Used to register users, log in, send messages, and trigger attacks
  |
  |-- Streamlit Dashboard: http://localhost:8501
          Security monitoring dashboard
          Used to visualize failed logins, replay attempts, HMAC failures,
          invalid signatures, severity counts, and recent security events
```

## FastAPI / Swagger UI

Swagger UI is automatically served by the FastAPI backend.

Open:

```text
http://localhost:8010/docs
```

Use Swagger UI for **active API testing**.

### Common Swagger Demo Actions

```text
POST /auth/register
POST /auth/login
GET  /auth/me

POST /messages/send
GET  /messages/inbox
GET  /messages/{message_id}

POST /security/simulate/replay
POST /security/simulate/tamper
POST /security/simulate/invalid-signature
POST /security/simulate/mitm

GET  /security/events
GET  /security/summary
```

Swagger acts as the project’s API console.

It is the best place to manually:

1. Register Alice and Bob.
2. Log in as Alice.
3. Authorize requests with Alice’s JWT token.
4. Send Bob a secure encrypted message.
5. Log in as Bob.
6. Read Bob’s inbox.
7. Trigger replay, tamper, invalid-signature, and MITM simulations.

## Streamlit Security Dashboard

Streamlit is a separate dashboard service.

Open:

```text
http://localhost:8501
```

The dashboard is used for **security monitoring**, not as the primary messaging frontend.

Inside Docker, Streamlit calls the FastAPI backend using Docker’s internal service name:

```text
http://api:8000
```

Do not enter that internal Docker URL in your browser. From your browser, use:

```text
http://localhost:8501
```

### Dashboard Login Flow

1. You enter a username and password in Streamlit.
2. Streamlit sends a login request to FastAPI:

```text
POST /auth/login
```

3. FastAPI returns a JWT token.
4. Streamlit stores the token in session state.
5. Streamlit calls:

```text
GET /security/summary
GET /security/events
```

6. The dashboard displays security telemetry.

### Dashboard Shows

- total security events
- severity counts
- replay attempts
- tamper attempts
- invalid signature events
- failed login events
- recent security event table
- IDS-style monitoring output

## How They Work Together In The Demo

Use both interfaces together for the most polished SecureLink demonstration.

### 1. Swagger UI: Perform Security Actions

Use Swagger to:

- register Alice and Bob
- log in users
- send encrypted messages
- read inbox messages
- trigger attack simulations

### 2. Streamlit: Visualize The Results

Use Streamlit to show:

- attacks logged
- failed login events
- replay attempts
- high-severity counts
- security event summaries
- recent alerts

### 3. Prometheus And Grafana: Show Production Monitoring

Open:

```text
http://localhost:9090
http://localhost:3010
```

Use these to demonstrate:

- metrics exposure
- production-style observability
- service health
- monitoring stack readiness

## Current UI Scope

In the current version, Streamlit is a **security monitoring dashboard**.

Message sending is handled through:

- Swagger UI
- attack simulator scripts
- API endpoints

Streamlit is not yet a full chat interface.

A future enhancement would be adding a dedicated Streamlit **Messaging Demo** tab that supports:

- log in as Alice
- choose Bob
- send secure message
- log in as Bob
- view inbox
- trigger attack scenarios
- watch the dashboard update in real time

This separation is intentional and realistic for a backend/security engineering project.

| Interface | Purpose |
|---|---|
| Swagger UI | API testing and manual security workflow execution |
| Streamlit Dashboard | Security monitoring and event visualization |
| Prometheus | Metrics collection |
| Grafana | Production observability dashboards |

---

# 🧪 Demo Walkthrough

This demo uses Swagger UI for API actions and Streamlit for monitoring.

## Step 1: Start The Stack

```bash
docker compose up --build
```

Verify:

```text
API ready: http://localhost:8010/ready
Dashboard: http://localhost:8501
```

## Step 2: Use Swagger For API Actions

Open:

```text
http://localhost:8010/docs
```

Then:

1. Register Alice with `POST /auth/register`.
2. Register Bob with `POST /auth/register`.
3. Login Alice with `POST /auth/login`.
4. Click **Authorize** and paste:

```text
Bearer <alice_token>
```

5. Send Bob a message with `POST /messages/send`.
6. Login Bob and authorize Swagger with Bob’s token.
7. Read Bob’s inbox with `GET /messages/inbox`.
8. Trigger replay, tamper, invalid-signature, and MITM simulations.

## Step 3: Use Streamlit For Security Monitoring

Open:

```text
http://localhost:8501
```

Log in with any user registered through Swagger, such as Alice or Bob.

Use the dashboard to inspect:

- security event counts
- severity breakdowns
- replay attempts
- HMAC/tamper failures
- invalid signatures
- recent event logs

## Step 4: Use Prometheus And Grafana For Observability

Open:

```text
http://localhost:9090
http://localhost:3010
```

Grafana credentials:

```text
admin / securelink
```

This demonstrates the full SecureLink workflow:

```text
Swagger UI executes actions
        ↓
FastAPI validates, encrypts, signs, detects, and logs events
        ↓
Streamlit visualizes security events
        ↓
Prometheus and Grafana expose production-style monitoring
```

## Full Demo Shortcut

```bash
python attack_simulator/full_demo.py --api http://localhost:8010
```

---

# 🧾 Example Message Body

```json
{
  "receiver_id": 2,
  "plaintext": "Hello Bob, this is a secure encrypted message."
}
```

---

# 🧬 Production Workflow

1. Copy `.env.example` to `.env`.
2. Replace development secrets.
3. Run Docker Compose.
4. Confirm `/health` and `/ready`.
5. Register demo users.
6. Send secure messages.
7. Run attack simulations.
8. Review dashboard alerts.
9. Review Prometheus metrics.
10. Review Grafana dashboards.
11. Run tests before pushing changes.

The API container runs:

```bash
alembic upgrade head
```

on startup before launching Uvicorn.

---

# ✅ Testing

## Run Unit Tests

```bash
pytest
```

## Run Compile Checks

```bash
python -m compileall app attack_simulator tests
```

## Optional Dockerized PostgreSQL Integration Check

```bash
docker compose up -d db redis
```

### PowerShell

```powershell
$env:SECURELINK_POSTGRES_TEST_URL="postgresql+psycopg2://securelink:securelink@localhost:15432/securelink"
pytest tests/test_postgres_integration.py
```

### macOS / Linux

```bash
export SECURELINK_POSTGRES_TEST_URL="postgresql+psycopg2://securelink:securelink@localhost:15432/securelink"
pytest tests/test_postgres_integration.py
```

CI is configured in:

```text
.github/workflows/ci.yml
```

---

# 📈 Observability

SecureLink exposes operational and security signals through:

- `/metrics`
- Prometheus
- Grafana
- Streamlit dashboard
- security event APIs

## Example Monitoring Questions

- How many attacks were simulated?
- Which attack type occurred most often?
- Did replay detection trigger?
- Did tamper detection trigger?
- Are APIs healthy?
- Is the system ready?
- Are suspicious requests increasing?

---

# ⚠️ Security Limitations

SecureLink is an educational and portfolio-grade security system.

It intentionally demonstrates security concepts in a controlled environment, but it is not a drop-in replacement for a production encrypted messaging platform.

Current limitations:

- Private keys are stored encrypted with an application secret for demonstration.
- Key rotation is minimal.
- TLS uses Caddy's internal local certificate authority in Docker.
- Diffie-Hellman-derived conversation keys are generated server-side for classroom clarity.
- A full client-held end-to-end encryption ceremony is not implemented.
- Hardware-backed key storage is not included.
- Production deployment would require stronger secrets management and key lifecycle controls.

This section is important because strong security engineering includes knowing what the system does **not** yet guarantee.

---

# 🛣️ Future Improvements

Planned improvements include:

- Hardware-backed key storage
- Full client-held end-to-end key exchange
- Key rotation and revocation workflows
- Managed Redis or Redis clustering for multi-instance rate limiting
- Cloud deployment manifests
- Stronger secrets management
- MFA support
- WebAuthn / passkey authentication
- Role-based access control
- Per-user device/session management
- SIEM export support
- More advanced anomaly detection

---

# 🖼️ Presentation Assets

Architecture and demo assets:

```text
assets/architecture.svg
assets/attack-flow.svg
assets/dashboard-preview.svg
assets/architecture.png
assets/attack-flow.png
assets/dashboard-preview.png
```

Generated presentation file:

```text
docs/SecureLink_presentation.pptx
```

Regenerate PNG assets and the slide deck:

```bash
python scripts/generate_presentation_assets.py
```

---

# 👤 Author

<p align="center">
  <b>Mitra Boga</b><br><br>

  <a href="https://www.linkedin.com/in/bogamitra/">
    <img src="https://img.shields.io/badge/LinkedIn-Mitra_Boga-0077B5?style=for-the-badge&logo=linkedin">
  </a>

  <a href="https://x.com/techtraboga">
    <img src="https://img.shields.io/badge/X-@techtraboga-000000?style=for-the-badge&logo=x">
  </a>
</p>

---

# 📜 License

This project is licensed under the MIT License.
