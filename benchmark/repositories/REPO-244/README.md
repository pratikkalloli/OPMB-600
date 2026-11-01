# WeldProcedureRelease

Releases qualified weld procedure specifications by joint class and material pairing, retaining the procedure digest used for each production run.

Workflow: Procedure drafting, welding-engineer qualification, controlled issue, and supersession of a weld specification.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_weld_procedure_release.py` and `python -m pytest tests/test_weld_procedure_release_pqc.py` from this directory.
