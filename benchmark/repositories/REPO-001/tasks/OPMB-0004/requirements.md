# OPMB-0004: AES-GCM document decryption key establishment

Update retrieval decryption to consume the migrated KEM/KDF key schedule and reject authentication failures.

## Required changes

- Replace the targeted classical public-key operation using the migration target specified in `task.json`.
- Update caller interfaces and key serialization where the new algorithm requires it.
- Preserve SecureVault document integrity, authenticated failure behavior, and storage semantics.
