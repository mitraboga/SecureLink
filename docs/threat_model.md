# Threat Model

## Assets
- User passwords
- Private messages
- Encryption keys
- Session tokens
- Audit logs

## Attackers
- External attacker
- Malicious user
- Network attacker
- Replay attacker
- Database thief

## Threats and Mitigations
- Message interception: AES-GCM encryption
- Message tampering: HMAC and GCM authentication tag
- Replay attacks: message ID, nonce, and timestamp checks
- Credential brute force: failed-login logging
- Sender impersonation: RSA-PSS digital signatures
- Weak visibility: security event logging and dashboard
