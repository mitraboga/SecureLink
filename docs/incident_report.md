# Incident Report: Snowflake Customer Data Theft Campaign

SecureLink is inspired by the 2024 Snowflake customer data theft campaign attributed by Mandiant to UNC5537.

## Incident Summary
In June 2024, Mandiant reported that UNC5537 was systematically compromising Snowflake customer instances using stolen customer credentials, then stealing data and attempting extortion. Mandiant stated that it had not found evidence that the activity came from a breach of Snowflake's enterprise environment. Instead, the incidents Mandiant investigated were traced to compromised customer credentials.

Mandiant also reported that affected accounts often lacked MFA, exposed credentials remained valid for long periods, and network allow lists were not consistently used.

## Why This Fits SecureLink
This incident fits the current project because SecureLink demonstrates the same defensive themes:

- Encrypt sensitive messages before storage.
- Authenticate users before access.
- Detect repeated failed logins and suspicious access patterns.
- Apply Redis-backed rate limiting.
- Verify message integrity before decryption.
- Detect replayed or tampered messages.
- Log suspicious activity for incident response.
- Surface security events through a dashboard and monitoring stack.

## SecureLink Connection
SecureLink models how systems can reduce the impact of credential and data-access failures by combining:

- bcrypt password hashing
- JWT authentication
- DH-derived conversation keys
- AES-GCM encryption
- HMAC verification
- RSA digital signatures
- replay detection
- login anomaly detection
- Redis-backed rate limiting
- audit logging
- Prometheus/Grafana monitoring

## CVE Note
This incident does not center on a single CVE. For the CS50 slide deck, list the incident as:

```text
Snowflake customer data theft campaign / UNC5537
Incident month/year: June 2024
CVE: N/A
```
