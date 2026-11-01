# Expected behavior

- Preserve the MerchantOnboard workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/merchant_onboard/workflow.py, src/merchant_onboard/crypto.py; the original test is `tests/test_merchant_onboard.py::test_task_2152_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_merchant_onboard_pqc.py::test_task_2152_public_key_encoding_round_trips_and_binds_purpose`.
