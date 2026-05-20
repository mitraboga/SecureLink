# Production-Ready Build Checklist

SecureLink is now built as a production-style course project through week 4.

## Week 1: Backend and Crypto Core
- FastAPI application
- AES-256-GCM encryption and decryption
- HMAC-SHA256 generation and verification
- SHA-256 helper
- RSA-PSS signing and verification
- Diffie-Hellman shared-key demonstration
- Unit tests for AES, HMAC, and signatures

## Week 2: Auth and Messages
- User registration
- bcrypt password hashing
- JWT login flow
- Authenticated `/auth/me`
- Encrypted message sending
- Inbox retrieval with verification before plaintext is returned
- SQLAlchemy database models
- SQLite local default and PostgreSQL Docker target

## Week 3: Attacks and Detection
- Replay simulation
- Tamper simulation
- Invalid-signature simulation
- MITM simulation explanation endpoint
- Brute-force login simulator script
- Login anomaly thresholding with `BRUTE_FORCE_LOGIN_DETECTED`
- Security event logging
- Streamlit dashboard for event visibility

## Week 4: Production Polish
- Dockerfile
- Docker Compose with PostgreSQL, API, dashboard, Prometheus, and Grafana
- Health and readiness endpoints
- Prometheus `/metrics`
- Security headers middleware
- Redis-backed IP rate limiting with in-memory fallback
- Caddy TLS reverse proxy
- GitHub Actions CI
- README, architecture docs, threat model, incident report, API docs, and demo script
- Architecture, attack-flow, and dashboard preview assets
- PNG exports for presentation assets
- Generated PowerPoint deck at `docs/SecureLink_presentation.pptx`

## Remaining Security Limitations
- Rate limiting is Redis-backed in Docker and falls back to in-memory mode when Redis is unavailable.
- Database migrations are configured with Alembic; future schema changes should be added as new revisions.
- Private-key handling is educational and should be backed by a KMS/HSM in real systems.
- TLS is terminated by Caddy with an internal local certificate authority; public deployment should use a real domain certificate.
- Conversation keys are DH-derived and persisted encrypted server-side; a real end-to-end messenger should keep private key material client-side.
