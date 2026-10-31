# Application catalogue

| Repository | Application | Domain | Purpose | Main modules | Classical cryptography | Tasks | Original tests |
|---|---|---|---|---|---|---:|---|
| REPO-001 | SecureVault | Secure file storage | Local SQLite document vault with authenticated encryption and signed integrity metadata | securevault.crypto, securevault.store, securevault.service | RSA-3072 OAEP/PSS, AES-256-GCM | 10 | 11 passed |
| REPO-002 | KeyLedger | Key management | SQLite inventory for ownership, purpose, expiry, rotation, revocation, and signed lifecycle audit events | keyledger.crypto, keyledger.ledger | RSA-3072 OAEP/PSS | 10 | 7 passed |

The remaining catalogue entries will be added when their application source and tests exist.
