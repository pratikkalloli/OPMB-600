# Team B cryptographic verification

## Result

**PARTIALLY VERIFIED: functional reference operations exercised; official pytest suites not run.** The checks used the Codex-managed Python 3.12.14 runtime with `cryptography==50.0.2`. That provider version matches the Team B dependency pin, but the checks did not use the branch-local `.venv` because pip could not install its dependencies.

All 60 existing PQC test functions (four per application) were directly invoked and passed through a minimal compatibility context implementing only `pytest.raises`. This exercised ML-DSA-65 key generation, signing and verification; ML-KEM-768 key generation, encapsulation and decapsulation; and existing tamper, malformed input, context-binding, and authenticated-envelope rejection cases. The classical baseline functions were also directly invoked: 60/60 passed. Per-application results are recorded under `reports/evidence/REPO-033/` through `REPO-047/` in `team-b-direct-runtime-checks.json`.

These direct calls are supplemental functional checks, **not pytest suite runs**. Pytest is absent from `.venv`; no result here satisfies the task-level requirement for the pinned pytest environment. No formal verification, production-readiness, security certification, or broad security claim is made.

## Static implementation review

All 15 reference services import `cryptography.hazmat.primitives.asymmetric.mlkem` and `mldsa`, and use `MLKEM768PrivateKey`, `MLDSA65PrivateKey`, `encapsulate`, `decapsulate`, `sign`, and `verify`. They also use HKDF-SHA-256 and AES-GCM for envelope protection. The reviewed PQC modules contain no imports of classical RSA, EC, DH, X25519/X448, or padding APIs, and no such fallback was observed. This is a scoped source review, not proof that no fallback exists elsewhere.

The credential-pattern scan covered 747 Team B application and contribution files for private-key PEM headers, AWS access-key IDs, GitHub token prefixes, and Stripe live-secret prefixes; it found no matches. No approved dedicated secret scanner was installed, so this pattern scan is limited and cannot establish absence of secrets.

No production or private key material was used. Fixtures use synthetic records and messages. All task statuses remain pending until the pinned test and review requirements are satisfied.
