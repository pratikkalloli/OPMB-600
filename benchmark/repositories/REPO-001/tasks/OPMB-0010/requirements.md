# OPMB-0010: PEM public-key loading API

Update the key-loading contract and type validation for PQC keys without silent classical fallback.

## Required changes

- Replace the targeted classical public-key operation using the migration target specified in `task.json`.
- Update caller interfaces and key serialization where the new algorithm requires it.
- Preserve SecureVault document integrity, authenticated failure behavior, and storage semantics.
