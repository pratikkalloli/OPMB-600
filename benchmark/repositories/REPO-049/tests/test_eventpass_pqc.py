import pytest
from eventpass_pqc.crypto import canonical_pass, export_public_key, generate_signer, load_public_key, sign_pass, verify_pass
from eventpass_pqc.service import EventPassPQC


def test_mldsa_offline_pass_verification_and_revocation(tmp_path):
    private = generate_signer(); app = EventPassPQC(tmp_path / "passes.db")
    app.issue("P-2", "EXPO-2", "guest-x", 22, 5000, private)
    assert app.verify_offline("P-2", private.public_key(), now=1000)
    assert not app.verify_offline("P-2", private.public_key(), now=6000)
    assert not app.verify_offline("P-2", private.public_key(), now=1000, revoked_snapshot={"P-2"})


def test_modified_pass_and_wrong_key_rejected():
    private = generate_signer(); other = generate_signer(); payload = canonical_pass("P", "E", "H", 2, 99); sig = sign_pass(payload, private)
    assert verify_pass(payload, sig, private.public_key())
    assert not verify_pass(payload + b"x", sig, private.public_key())
    assert not verify_pass(payload, sig, other.public_key())


def test_mldsa_public_key_serialization_and_invalid_key():
    private = generate_signer(); pub = load_public_key(export_public_key(private.public_key()))
    assert verify_pass(b"x", sign_pass(b"x", private), pub)
    with pytest.raises(ValueError): load_public_key(b"bad")
