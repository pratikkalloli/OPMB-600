# Cryptographic verification summary

The recorded full inventory contains 2,240 actual pytest cases across 360 original/PQC suites (2,240 passed, 0 failed, 0 skipped). Batches 01 and 02 were rerun after domain-workflow changes: 320 tests passed across 40 suites. Their cases include each added workflow decision and at least one policy rejection in the separate original and PQC implementations.

The other 160 applications' historical passing tests do not demonstrate domain-specific behavior. Per-application evidence is under `reports/evidence/REPO-XXX/`; current workflow status is in `domain_specificity_audit.json`.

These are software functional-test results only. They do not establish formal verification, FIPS certification, independent security review, or production readiness. A dedicated cryptographic scanner has not been run.
