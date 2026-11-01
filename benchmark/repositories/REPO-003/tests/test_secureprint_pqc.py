import pytest
from secureprint_pqc import crypto
from secureprint_pqc.service import PrintService

def test_kem_aead_roundtrip_and_tamper_rejection():
    private, public = crypto.generate_printer_keypair(); package = crypto.encrypt_job_content(b"release", public, "job1")
    assert crypto.decrypt_job_content(package, private, "job1") == b"release"
    changed = dict(package); changed["ciphertext"] = package["ciphertext"][:-1] + bytes([package["ciphertext"][-1] ^ 1])
    with pytest.raises(ValueError): crypto.decrypt_job_content(changed, private, "job1")

def test_mldsa_signature_and_invalid_signature():
    private, public = crypto.generate_audit_keypair(); sig = crypto.sign_job_metadata(b"manifest", private)
    assert crypto.verify_job_metadata(b"manifest", sig, public)
    assert not crypto.verify_job_metadata(b"other", sig, public)

def test_public_key_type_separation():
    _, public = crypto.generate_printer_keypair(); encoded = crypto.serialize_public_key(public)
    assert isinstance(crypto.load_public_key(encoded, "kem"), type(public))
    with pytest.raises(ValueError): crypto.load_public_key(encoded, "signature")

def test_package_serialization_roundtrip():
    _, public = crypto.generate_printer_keypair(); package = crypto.encrypt_job_content(b"doc", public, "id")
    restored = crypto.deserialize_job_package(crypto.serialize_job_package(package))
    assert crypto.decrypt_job_content(restored, _, "id") == b"doc"

def test_pqc_service_authorization_release_and_cancel():
    app = PrintService(); app.register_user("fictional-user"); app.register_printer("printer-a")
    app.submit_job("job-a", "fictional-user", "printer-a", b"sample")
    assert app.release_job("job-a", "printer-a") == b"sample"
    app.submit_job("job-b", "fictional-user", "printer-a", b"sample 2")
    assert app.cancel_job("job-b", "fictional-user")
    with pytest.raises(ValueError): app.submit_job("job-c", "revoked-user", "printer-a", b"x")
