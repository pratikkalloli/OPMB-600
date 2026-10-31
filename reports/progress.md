# OPMB-600 progress

## Checkpoint: first application pilot

- Repository was initially empty; branch: `feature/opmb-600-benchmark`.
- Foundation includes schemas, docs, experiment templates, and validation commands.
- Added REPO-001 SecureVault: SQLite document store with per-object AES-GCM, RSA-OAEP data-key wrapping, and RSA-PSS manifest integrity.
- Added ten task directories/specifications linked to executable cryptographic functions.
- Added a separate reference implementation using ML-KEM-768 plus HKDF and AES-GCM for key wrapping, and ML-DSA-65 for manifest signatures.
- Pinned environment tests: original 8 passed; reference 8 passed. Test output and dependency versions are recorded in `reports/evidence/REPO-001/test-results.json`.
- Task statuses: 10 candidates, 0 accepted; execution evidence exists, independent review and full corpus acceptance do not.

## Remaining work

Batch 1 has five of six pilot applications and fifty tasks remaining. The other 54 applications/540 tasks, balanced global family distribution, final splits, scanner/leakage checks, broad migration verification, and full acceptance remain incomplete. Run `python -m validation.run_all --allow-incomplete` for batch checks; the default command fails until the 60/600/600 acceptance target is met.
