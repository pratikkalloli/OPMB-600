# OPMB-0006: RSA-PSS manifest verification

Migrate signature verification to the corresponding PQC public-key representation and preserve invalid-signature semantics.

## Required changes

- Replace the targeted classical public-key operation using the migration target specified in `task.json`.
- Update caller interfaces and key serialization where the new algorithm requires it.
- Preserve SecureVault document integrity, authenticated failure behavior, and storage semantics.
