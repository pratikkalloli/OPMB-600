# OPMB-0001: RSA-OAEP key wrapping

Replace RSA-wrapped per-document data keys with a protocol using ML-KEM to establish a wrapping secret, a KDF, and authenticated symmetric wrapping.

## Required changes

- Replace the targeted classical public-key operation using the migration target specified in `task.json`.
- Update caller interfaces and key serialization where the new algorithm requires it.
- Preserve SecureVault document integrity, authenticated failure behavior, and storage semantics.
