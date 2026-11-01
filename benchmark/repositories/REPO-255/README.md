# PackagingArtworkRelease

Controls the approved artwork revision and market destination before a packaging line can print labels.

Workflow: Controls the approved artwork revision and market destination before a packaging line can print labels; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_packaging_artwork_release.py` and `python -m pytest tests/test_packaging_artwork_release_pqc.py` from this directory.

## Domain workflow

Both the original and PQC services implement `release_packaging_artwork`. It enforces the application's stated business rule and records the decision with the signed record's workflow event.
