# ToolWearForecastCase

Records measured cutting-tool wear and the maintenance disposition used to prevent an expired tool from returning to a workcell.

Workflow: Records measured cutting-tool wear and the maintenance disposition used to prevent an expired tool from returning to a workcell; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_tool_wear_forecast_case.py` and `python -m pytest tests/test_tool_wear_forecast_case_pqc.py` from this directory.
