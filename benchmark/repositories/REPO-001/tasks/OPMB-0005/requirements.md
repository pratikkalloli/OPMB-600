# OPMB-0005: RSA-PSS manifest signing

Replace manifest signing with ML-DSA and update context, signature, and key handling across callers.

## Required changes

- Replace the targeted classical public-key operation using the migration target specified in `task.json`.
- Update caller interfaces and key serialization where the new algorithm requires it.
- Preserve SecureVault document integrity, authenticated failure behavior, and storage semantics.
