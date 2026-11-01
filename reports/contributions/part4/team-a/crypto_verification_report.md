# Cryptographic verification

Status: **passed by application tests** in Python 3.11.9, pytest 8.4.2, and `cryptography==50.0.2`.

The 15 separate PQC suites passed 150 tests with no failures, skips, errors, or warnings. They exercise FIPS 203 ML-KEM-768, FIPS 204 ML-DSA-65, distinct signing/transport keys, purpose-tagged serialization, strict version and algorithm checks, context-bound signatures, HKDF-SHA-256, AES-256-GCM, malformed-input rejection, and lifecycle behavior.

| Repository | PQC tests | Result |
|---|---:|---|
| REPO-018 | 10 passed, 0 failed, 0 skipped | passed |
| REPO-019 | 10 passed, 0 failed, 0 skipped | passed |
| REPO-020 | 10 passed, 0 failed, 0 skipped | passed |
| REPO-021 | 10 passed, 0 failed, 0 skipped | passed |
| REPO-022 | 10 passed, 0 failed, 0 skipped | passed |
| REPO-023 | 10 passed, 0 failed, 0 skipped | passed |
| REPO-024 | 10 passed, 0 failed, 0 skipped | passed |
| REPO-025 | 10 passed, 0 failed, 0 skipped | passed |
| REPO-026 | 10 passed, 0 failed, 0 skipped | passed |
| REPO-027 | 10 passed, 0 failed, 0 skipped | passed |
| REPO-028 | 10 passed, 0 failed, 0 skipped | passed |
| REPO-029 | 10 passed, 0 failed, 0 skipped | passed |
| REPO-030 | 10 passed, 0 failed, 0 skipped | passed |
| REPO-031 | 10 passed, 0 failed, 0 skipped | passed |
| REPO-032 | 10 passed, 0 failed, 0 skipped | passed |

Application tests verify domain policy and workflow behavior in addition to cryptographic properties. Passing tests are execution evidence, not independent NIST validation or production approval.
