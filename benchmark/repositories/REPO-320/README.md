# WaterPumpEnergyLedger

Reconciles pump runtime and energy readings against a water delivery schedule.

Workflow: Reconciles pump runtime and energy readings against a water delivery schedule; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_water_pump_energy_ledger.py` and `python -m pytest tests/test_water_pump_energy_ledger_pqc.py` from this directory.
