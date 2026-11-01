# Expected behavior

- Preserve the ParcelBoundaryRecord workflow and its domain-specific policy.
- Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.
- Keep signing and transport key purposes separate.

The exact source target is src/parcel_boundary_record/workflow.py, src/parcel_boundary_record/crypto.py; the original test is `tests/test_parcel_boundary_record.py::test_task_2032_public_key_encoding_round_trips_and_binds_purpose` and PQC migration test is `tests/test_parcel_boundary_record_pqc.py::test_task_2032_public_key_encoding_round_trips_and_binds_purpose`.
