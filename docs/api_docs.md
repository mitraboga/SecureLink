# API Docs

Run the API and open:

- Swagger UI: `http://localhost:8010/docs`
- ReDoc: `http://localhost:8010/redoc`

Important endpoint groups:

- Auth: `/auth/register`, `/auth/login`, `/auth/me`
- Keys: `/keys/generate-rsa`, `/keys/exchange-dh`, `/keys/public/{user_id}`
- Messages: `/messages/send`, `/messages/inbox`, `/messages/{message_id}`
- Security: `/security/events`, `/security/summary`, `/security/simulate/replay`, `/security/simulate/tamper`, `/security/simulate/invalid-signature`, `/security/simulate/mitm`
