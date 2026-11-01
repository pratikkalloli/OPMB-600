# Part 3 known issues

> Historical checkpoint notes below describe the state before the 2026-11-01 remediation. The task CSV, SecureVault task JSON mismatch, and missing Python dependencies have since been resolved; see `part3_audit_report.md` for verification. Remaining benchmark limitations include pending tests/references for REPO-003?017 and the missing 43 applications / 430 tasks.

- Preflight differs from the prompt: only two prior applications and 20 tasks were present. Safe new allocation starts at REPO-003 / OPMB-0021.
- Only REPO-003 is implemented here; 14 applications and 140 Part 3 tasks remain incomplete.
- Runtime tests and cryptographic execution checks are pending because the active Python lacks cryptography, pytest, and pip; the other Windows Python launch targets were inaccessible.
- JSON Schema validation is pending because jsonschema is unavailable. Task-link, repository, duplicate, syntax, and lexical-scan checks did run.
- Lexical scanning is not a proof of cryptographic correctness and does not inspect dependencies or dynamic code.
- SecurePrint has in-memory records and process-ephemeral keys; it is a research simulation.
- No changes were committed or pushed.
