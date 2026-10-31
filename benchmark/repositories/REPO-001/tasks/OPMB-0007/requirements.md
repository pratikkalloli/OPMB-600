# OPMB-0007: RSA recipient key generation

Replace recipient RSA key lifecycle with ML-KEM keypair generation and document serialized key changes.

## Required changes

- Replace the targeted classical public-key operation using the migration target specified in `task.json`.
- Update caller interfaces and key serialization where the new algorithm requires it.
- Preserve SecureVault document integrity, authenticated failure behavior, and storage semantics.
