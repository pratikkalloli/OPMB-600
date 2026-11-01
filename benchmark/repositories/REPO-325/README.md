# EnergyMarketBidEnvelope

Submits a time-bounded market bid with quantity limits and authorized trader identity.

Workflow: Submits a time-bounded market bid with quantity limits and authorized trader identity; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_energy_market_bid_envelope.py` and `python -m pytest tests/test_energy_market_bid_envelope_pqc.py` from this directory.
