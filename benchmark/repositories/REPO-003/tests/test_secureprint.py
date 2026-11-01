import pytest
from secureprint import crypto
from secureprint.service import PrintService

def test_submit_and_authorized_release():
    app = PrintService(); app.register_user("alice"); app.register_printer("p1")
    app.submit_job("j1", "alice", "p1", b"synthetic document")
    assert app.release_job("j1", "p1") == b"synthetic document"
    assert app.jobs["j1"]["status"] == "released"

def test_wrong_printer_and_cancel_policy():
    app = PrintService(); app.register_user("alice"); app.register_printer("p1"); app.register_printer("p2")
    app.submit_job("j1", "alice", "p1", b"data")
    with pytest.raises(ValueError): app.release_job("j1", "p2")
    with pytest.raises(ValueError): app.cancel_job("j1", "mallory")
    assert app.cancel_job("j1", "alice") is True

def test_ciphertext_tamper_and_wrong_key_rejected():
    private, public = crypto.generate_printer_keypair(); other, _ = crypto.generate_printer_keypair()
    package = crypto.encrypt_job_content(b"secret", public, "j")
    changed = dict(package); changed["ciphertext"] = changed["ciphertext"][:-1] + bytes([changed["ciphertext"][-1] ^ 1])
    with pytest.raises(ValueError): crypto.decrypt_job_content(changed, private, "j")
    with pytest.raises(ValueError): crypto.decrypt_job_content(package, other, "j")

def test_signature_rejects_changed_metadata():
    private, public = crypto.generate_audit_keypair(); sig = crypto.sign_job_metadata(b"a", private)
    assert crypto.verify_job_metadata(b"a", sig, public)
    assert not crypto.verify_job_metadata(b"b", sig, public)

def test_package_serialization_rejects_corruption():
    _, public = crypto.generate_printer_keypair(); package = crypto.encrypt_job_content(b"x", public, "j")
    encoded = crypto.serialize_job_package(package)
    assert crypto.deserialize_job_package(encoded) == package
    with pytest.raises(ValueError): crypto.deserialize_job_package(b"not json")

def test_duplicate_and_missing_printer_rejected():
    app = PrintService(); app.register_user("a")
    with pytest.raises(ValueError): app.submit_job("j", "a", "missing", b"x")
    app.register_printer("p")
    with pytest.raises(ValueError): app.register_printer("p")
