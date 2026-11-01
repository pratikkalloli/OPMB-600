# BuildRelay

Controlled synthetic ci cd security application for OPMB-600. CI worker identity, encrypted secret handoff, and signed build attestations. Classical baseline: RSA-3072 OAEP/PSS. Migration target: ML-KEM-768 + ML-DSA-65. Candidate specifications only; no reference migration or test outcome is claimed.

Run `python -m pytest` after installing the pinned requirements.
