# Demo Script

## Demo 1: Normal Secure Message
Register Alice and Bob. Alice logs in and sends Bob a message. Bob logs in and opens the inbox. The API returns plaintext only after HMAC and signature verification.

## Demo 2: Tampering Attack
Run the tamper simulation as Bob. The API modifies ciphertext in a controlled test, verification fails, and a security event is logged.

## Demo 3: Replay Attack
Run the replay simulation as Alice after sending a message. The API attempts to reuse the old message ID and nonce. Replay detection blocks the request.

## Demo 4: Invalid Signature
Run the invalid-signature simulation as Bob. The API modifies the signature in a controlled test, signature verification fails, and a security event is logged.

## Demo 5: Dashboard
Open Streamlit at `http://localhost:8501`, log in, and show the event counts and recent events.

## Full Demo Shortcut
After the API is running, execute:

```bash
python attack_simulator/full_demo.py --api http://localhost:8010
```

## CS50 Video Flow
1. Show the required title slide with name, edX username, GitHub username, recording date, incident month/year, and CVE status.
2. Explain the Snowflake / UNC5537 incident and why credential abuse and monitoring matter.
3. Show the SecureLink architecture.
4. Open Swagger at `http://localhost:8010/docs`.
5. Register Alice and Bob.
6. Login Alice, authorize Swagger, and send Bob an encrypted message.
7. Login Bob, authorize Swagger, and show Bob's decrypted inbox.
8. Run replay, tamper, invalid-signature, and MITM simulations.
9. Open the Streamlit dashboard at `http://localhost:8501`.
10. Briefly show Prometheus at `http://localhost:9090` and Grafana at `http://localhost:3010`.
11. Close with security recommendations and limitations.
