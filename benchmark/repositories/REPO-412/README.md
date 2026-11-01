# DroneSurveyMission

Authorizes a farm survey flight with field boundary, sensor payload, and image retention policy.

Workflow: Authorizes a farm survey flight with field boundary, sensor payload, and image retention policy; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_drone_survey_mission.py` and `python -m pytest tests/test_drone_survey_mission_pqc.py` from this directory.
