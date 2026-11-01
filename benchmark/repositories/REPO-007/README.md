# PayRoute

Controlled synthetic payment routing application for OPMB-600. Synthetic payment instruction signing, recipient key delivery, and idempotent settlement records. Classical baseline: RSA-3072 OAEP/PSS. Migration target: ML-KEM-768 + ML-DSA-65. Candidate specifications only; no reference migration or test outcome is claimed.

Run `python -m pytest` after installing the pinned requirements.
