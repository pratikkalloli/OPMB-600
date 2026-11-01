# OPMB-0240 expected behavior

- The DataProvenance provenance checkpoint workflow succeeds for valid input.
- The migrated function `revoke_provenance_checkpoint_identity` uses Fail-closed key revocation and stale-version rejection.
- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.
