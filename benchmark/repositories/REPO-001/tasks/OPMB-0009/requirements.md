# OPMB-0009: SPKI public-key persistence API

Revise public-key serialization and configuration interfaces for the selected standardized PQC key format.

## Required changes

- Replace the targeted classical public-key operation using the migration target specified in `task.json`.
- Update caller interfaces and key serialization where the new algorithm requires it.
- Preserve SecureVault document integrity, authenticated failure behavior, and storage semantics.
