# InvoiceSeal cryptographic verification

Original suite: 6 passed, 0 failed, 0 skipped. PQC reference suite: 5 passed, 0 failed, 0 skipped. Compile check passed.

Coverage includes RSA-PSS and ML-DSA-65 acceptance, altered-payload and wrong-key rejection, ML-DSA public-key encoding round trip, malformed-key rejection, canonical invoice validation, algorithm-tagged version IDs, database payload-digest tampering rejection, and persisted invoice issue/revision/history behavior. ML-DSA uses an InvoiceSeal-specific context string. The lexical scanner found no targeted RSA/ECDSA/ECDH/X25519/X448 calls in migrated Python source.

These tests do not establish formal security or certification. The scanner does not inspect dependencies, runtime-loaded code, serialized data, or side channels. Exact commands, timestamps, versions, exit codes, and counts are in reports/evidence/REPO-048/test-results.json.
