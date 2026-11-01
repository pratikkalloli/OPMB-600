# WebhookShield

Controlled synthetic application for OPMB-600. Signed webhook delivery and replay protection. Classical baseline: RSA-3072 PSS and RSA-OAEP/AES-256-GCM. The independent reference package uses FIPS 204 ML-DSA-65 and FIPS 203 ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM.

**Scope distinction:** focuses on HTTP event delivery identifiers, nonce replay detection, and signed request bodies; it is not a network tunnel or general peer session protocol.

Original source is in `src/webhookshield/`; the migration reference is in `migrated_reference/webhookshield_pqc/`. Both implement the domain-specific `delivery` model and workflow, strict field validation, a persistent SQLite signed-record ledger, a runnable CLI, key serialization, and key lifecycle.

From this directory, run the original CLI with `PYTHONPATH=src python -m webhookshield [record.json]` on POSIX or `$env:PYTHONPATH='src'; python -m webhookshield [record.json]` in PowerShell. For the separate reference CLI, set `PYTHONPATH=migrated_reference` (PowerShell: `$env:PYTHONPATH='migrated_reference'`) and run `python -m webhookshield_pqc [record.json]`. Omit the file to read JSON from standard input. Run the two test suites with `python -m pytest tests/test_webhookshield.py -q` and `python -m pytest tests/test_webhookshield_pqc.py -q`. This synthetic benchmark is not a production system.
