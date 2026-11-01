# OPMB-0275 expected behavior

- The DesktopUpdateProof update release workflow succeeds for valid input.
- The migrated function `canonicalize_update_release` uses Stable canonical JSON for signature input.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
