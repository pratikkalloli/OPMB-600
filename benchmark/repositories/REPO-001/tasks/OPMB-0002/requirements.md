# OPMB-0002: RSA-OAEP key unwrapping

Redesign recipient key opening for a KEM-derived wrapping key while retaining uniform failure behavior.

## Required changes

- Replace the targeted classical public-key operation using the migration target specified in `task.json`.
- Update caller interfaces and key serialization where the new algorithm requires it.
- Preserve SecureVault document integrity, authenticated failure behavior, and storage semantics.
