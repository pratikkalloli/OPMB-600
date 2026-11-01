# Expected behavior

Migrate MachineInterlockPermit recover an artifact and reject malformed or altered envelopes from X25519 ECDH with HKDF-SHA-256 and AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Safety-case review, interlock epoch issuance, operator acknowledgment, and restart authorization. semantics.

Valid interlock permit operations remain interoperable with the documented PQC format. Invalid state, bad interlock_epoch, altered content, wrong keys, and unsupported versions are rejected.
