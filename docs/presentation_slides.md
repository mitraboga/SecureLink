# SecureLink Presentation Slides

Generated deck: `docs/SecureLink_presentation.pptx`

## Slide 1: Title
SecureLink: A Production-Grade Encrypted Messaging and Attack Detection Platform

Include name, edX username, GitHub username, recording date, incident month/year, and CVE status.

Recommended incident line:

```text
Incident: Snowflake customer data theft campaign / UNC5537
Incident month/year: June 2024
CVE: N/A
```

## Slide 2: Snowflake / UNC5537 Summary
Explain that attackers used stolen customer credentials to access Snowflake customer environments, steal data, and extort victims.

## Slide 3: What Failed
Discuss stolen credentials, missing MFA, credential rotation gaps, weak network restrictions, monitoring needs, and incident response.

## Slide 4: Cryptography Concepts
AES-GCM, SHA-256, HMAC, RSA digital signatures, Diffie-Hellman, and JWT authentication.

## Slide 5: Architecture
Use `assets/architecture.svg`.

## Slide 6: Secure Message Flow
Login, verify JWT, encrypt with AES-GCM, authenticate with HMAC, sign metadata, store ciphertext, verify before decrypting.

## Slide 7: Attack Simulations
Use `assets/attack-flow.svg` and show replay, tampering, invalid signature, MITM, and brute force scenarios.

## Slide 8: Monitoring Dashboard
Use `assets/dashboard-preview.svg` and the live Streamlit dashboard.

## Slide 9: Recommendations
Use TLS, strict authentication, rate limiting, audit logging, key rotation, and monitoring.

## Slide 10: Conclusion
SecureLink demonstrates how layered cryptographic controls and security monitoring reduce the impact of compromised data-transfer workflows.
