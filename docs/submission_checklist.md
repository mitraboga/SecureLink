# CS50 Cybersecurity Submission Checklist

## Required Video Details
- Length: 7-10 minutes.
- Format: video or screencast presentation report.
- Narration: spoken English voiceover is required.
- Visibility: upload to YouTube as Unlisted.
- First slide must include:
  - name
  - edX username
  - GitHub username
  - recording date
  - incident month/year: June 2024
  - CVE: N/A

## Incident
Use:

```text
Snowflake customer data theft campaign / UNC5537
Incident month/year: June 2024
CVE: N/A
```

## Demo URLs
- Swagger UI: `http://localhost:8010/docs`
- TLS proxy: `https://localhost:8443`
- Streamlit dashboard: `http://localhost:8501`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3010`

## Pre-Recording Commands
```bash
docker compose up --build
pytest
```

Optional live PostgreSQL test:

```powershell
$env:SECURELINK_POSTGRES_TEST_URL="postgresql+psycopg2://securelink:securelink@localhost:15432/securelink"
pytest tests/test_postgres_integration.py
```

## Demo Checklist
- Register Alice.
- Register Bob.
- Login Alice.
- Authorize Swagger with Alice's JWT.
- Send encrypted message to Bob.
- Login Bob.
- Authorize Swagger with Bob's JWT.
- Read Bob's inbox.
- Run replay simulation.
- Run tamper simulation.
- Run invalid-signature simulation.
- Run MITM simulation.
- Show security events.
- Show dashboard and monitoring.

## Accurate Limitation Statement
SecureLink is a production-style educational system. It demonstrates encryption, authentication, attack detection, rate limiting, migrations, monitoring, and TLS, but a real public deployment would still need managed secrets, hardened cloud networking, client-side private key ownership, key rotation, and production certificate management.
