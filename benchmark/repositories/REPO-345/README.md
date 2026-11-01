# CustomsInspectionPacket

Assembles shipment inspection evidence and records release or hold authority.

Workflow: Assembles shipment inspection evidence and records release or hold authority; intake, validate, approve, record transition, and preserve a verifiable audit artifact.

All identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.

Run `python -m pytest tests/test_customs_inspection_packet.py` and `python -m pytest tests/test_customs_inspection_packet_pqc.py` from this directory.
