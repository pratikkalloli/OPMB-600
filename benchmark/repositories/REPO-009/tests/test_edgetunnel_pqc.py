"""Required migrated behavior tests; implement with the selected standardized provider."""
import pytest

@pytest.mark.skip(reason="PQC reference implementation is pending; candidate task only")
def test_pqc_migration_contract():
    pytest.fail("Implement PQC round-trip, tamper, downgrade, and key lifecycle cases")
