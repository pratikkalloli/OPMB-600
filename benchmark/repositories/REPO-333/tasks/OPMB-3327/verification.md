# Verification

From `benchmark/repositories/REPO-333`, run `python -m pytest tests/test_aircraft_component_life_card.py` and `python -m pytest tests/test_aircraft_component_life_card_pqc.py`. Exercise `load_public_key`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/REPO-333/`.
