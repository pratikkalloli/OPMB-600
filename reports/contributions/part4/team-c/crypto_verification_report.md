# Team C cryptographic verification checkpoint

InvoiceSeal: 6 original tests and 5 ML-DSA reference tests passed. EventPass: 3 original tests and 3 ML-DSA reference tests passed. No skips or failures.

Coverage includes signature acceptance, modified payload rejection, wrong-key rejection, PQC public-key serialization, malformed-key rejection, invoice revision identity and digest tampering, and event pass expiration, revocation snapshots, duplicate serials, and offline verification. Both references use an application-specific ML-DSA context string. The reference scanner reported no RSA/ECDSA/ECDH/X25519/X448 source matches for these two apps.

Evidence is under reports/evidence/REPO-048 and reports/evidence/REPO-049. Unit tests and lexical scans are not formal security proofs, dependency scans, side-channel evaluations, or independent certification.
