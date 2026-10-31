# OPMB-0003: AES-GCM document encryption key establishment

Integrate a KEM-derived data key into document encryption while preserving object-ID AAD binding and nonce handling.

## Required changes

- Replace the targeted classical public-key operation using the migration target specified in `task.json`.
- Update caller interfaces and key serialization where the new algorithm requires it.
- Preserve SecureVault document integrity, authenticated failure behavior, and storage semantics.
