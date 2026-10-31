# OPMB-0008: RSA signing key generation

Replace the independent signing-key lifecycle with ML-DSA keys and define rotation and storage compatibility.

## Required changes

- Replace the targeted classical public-key operation using the migration target specified in `task.json`.
- Update caller interfaces and key serialization where the new algorithm requires it.
- Preserve SecureVault document integrity, authenticated failure behavior, and storage semantics.
