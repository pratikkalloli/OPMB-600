# Expected behavior

Migrate MachineInterlockPermit apply only an allowed domain lifecycle transition from ECDSA P-256/SHA-256 to ML-DSA-65, retaining Safety-case review, interlock epoch issuance, operator acknowledgment, and restart authorization. semantics.

Valid interlock permit operations remain interoperable with the documented PQC format. Invalid state, bad interlock_epoch, altered content, wrong keys, and unsupported versions are rejected.
