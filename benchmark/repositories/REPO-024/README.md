# DataProvenance

Controlled synthetic application for OPMB-600. Signed data provenance and verifiable checkpoints. Classical baseline: RSA-3072 PSS and RSA-OAEP/AES-256-GCM. The independent reference package uses FIPS 204 ML-DSA-65 and FIPS 203 ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM.

**Scope distinction:** tracks general dataset/object lineage through chained digest checkpoints; it does not attest software builds or release artifacts.

Original source is in `src/dataprovenance/`; the migration reference is in `migrated_reference/dataprovenance_pqc/`. Both implement the domain-specific `provenance checkpoint` model and workflow, strict field validation, a persistent SQLite signed-record ledger, a runnable CLI, key serialization, and key lifecycle.

From this directory, run the original CLI with `PYTHONPATH=src python -m dataprovenance [record.json]` on POSIX or `$env:PYTHONPATH='src'; python -m dataprovenance [record.json]` in PowerShell. For the separate reference CLI, set `PYTHONPATH=migrated_reference` (PowerShell: `$env:PYTHONPATH='migrated_reference'`) and run `python -m dataprovenance_pqc [record.json]`. Omit the file to read JSON from standard input. Run the two test suites with `python -m pytest tests/test_dataprovenance.py -q` and `python -m pytest tests/test_dataprovenance_pqc.py -q`. This synthetic benchmark is not a production system.
