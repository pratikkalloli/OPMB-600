import sqlite3
import pytest
from eventpass.crypto import canonical_pass, export_public_key, generate_signer, load_public_key, verify_pass
from eventpass.service import EventPass


def test_issue_offline_verify_expiry_and_revoke(tmp_path):
    private, public = generate_signer(); app = EventPass(tmp_path / "passes.db")
    app.issue("P-1", "EXPO-1", "guest-7", 11, 5000, private)
    assert app.verify_offline("P-1", public, now=1000)
    assert not app.verify_offline("P-1", public, now=6000)
    assert app.revoke("P-1") and not app.verify_offline("P-1", public, now=1000)


def test_duplicate_serial_and_bad_pass_fields_rejected(tmp_path):
    private, _ = generate_signer(); app = EventPass(tmp_path / "passes.db")
    app.issue("P-1", "EXPO-1", "guest-a", 8, 9000, private)
    assert app.duplicate_serial(8)
    with pytest.raises(sqlite3.IntegrityError): app.issue("P-2", "EXPO-1", "guest-b", 8, 9000, private)
    with pytest.raises(ValueError): canonical_pass("", "e", "h", 1, 100)


def test_public_key_format_roundtrip():
    _, public = generate_signer(); assert load_public_key(export_public_key(public)).public_numbers() == public.public_numbers()
