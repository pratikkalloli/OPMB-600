# Team B cryptographic verification

## Result

**FUNCTIONAL CHECKS PASS; no security certification claimed.** The official PQC suites ran in the branch-local `.venv` using Python 3.12.14 and the pinned `cryptography==50.0.2` provider. All 15 suites passed (four tests each, 60 total). The classical suites also passed 60/60.

Each official pytest suite was invoked separately using its path from `applications.json`, with four tests passing and zero failures. PQC tests exercise ML-DSA-65 key generation, signing and verification; ML-KEM-768 key generation, encapsulation and decapsulation; and negative cases including tampered signatures/envelopes, malformed inputs, and context/recipient mismatch. Detailed official results are in `reports/evidence/REPO-033/` through `REPO-047/` in `test-results.json`.

Earlier direct invocations with a minimal `pytest.raises` compatibility context are retained as supplemental evidence in `team-b-direct-runtime-checks.json`; they are not counted as pytest runs. The official pytest suites subsequently ran in `.venv`. No formal verification, production-readiness, security certification, or broad security claim is made.

## Static implementation review

All 15 reference services import `cryptography.hazmat.primitives.asymmetric.mlkem` and `mldsa`, and use `MLKEM768PrivateKey`, `MLDSA65PrivateKey`, `encapsulate`, `decapsulate`, `sign`, and `verify`. They also use HKDF-SHA-256 and AES-GCM for envelope protection. The reviewed PQC modules contain no imports of classical RSA, EC, DH, X25519/X448, or padding APIs, and no such fallback was observed. This is a scoped source review, not proof that no fallback exists elsewhere.

The credential-pattern scan covered 747 Team B application and contribution files for private-key PEM headers, AWS access-key IDs, GitHub token prefixes, and Stripe live-secret prefixes; it found no matches. No approved dedicated secret scanner was installed, so this pattern scan is limited and cannot establish absence of secrets.

No production or private key material was used. Fixtures use synthetic records and messages. All task statuses remain pending until the pinned test and review requirements are satisfied.
