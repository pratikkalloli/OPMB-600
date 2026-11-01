# IrrigationZoneSchedule

Issues irrigation commands by field zone with water allocation and soil-moisture constraints.

Workflow: Issues irrigation commands by field zone with water allocation and soil-moisture constraints; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_irrigation_zone_schedule.py` and `python -m pytest tests/test_irrigation_zone_schedule_pqc.py` from this directory.
