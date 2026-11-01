import base64, json
import pytest
from cryptography.hazmat.primitives.asymmetric import mldsa, mlkem
from trustbridge_pqc import crypto

SIGN = [crypto.operation_01, crypto.operation_02, crypto.operation_03, crypto.operation_04, crypto.operation_08, crypto.operation_09, crypto.operation_10]
ENC = [crypto.operation_05, crypto.operation_06, crypto.operation_07]

def test_all_signature_tasks_use_mldsa_context_and_reject_tamper():
    private, public = crypto.generate_signing_keypair(); _, wrong_public = crypto.generate_signing_keypair()
    assert isinstance(private, mldsa.MLDSA65PrivateKey)
    for operation in SIGN:
        envelope = operation(private, None, b"synthetic-record", b"trust-v1")
        assert operation(None, public, envelope, b"trust-v1") is True
        assert operation(None, wrong_public, envelope, b"trust-v1") is False
        assert operation(None, public, envelope, b"wrong-context") is False
        obj = json.loads(envelope); obj["payload"] = base64.b64encode(b"changed").decode()
        assert operation(None, public, json.dumps(obj).encode(), b"trust-v1") is False

def test_all_confidentiality_tasks_use_mlkem_and_aead():
    private, public = crypto.generate_kem_keypair(); wrong_private, _ = crypto.generate_kem_keypair()
    assert isinstance(private, mlkem.MLKEM768PrivateKey)
    for operation in ENC:
        envelope = operation(public, None, b"synthetic-key", b"care-v1")
        assert operation(None, private, envelope, b"care-v1") == b"synthetic-key"
        with pytest.raises(ValueError): operation(None, private, envelope, b"other")
        with pytest.raises(ValueError): operation(None, wrong_private, envelope, b"care-v1")
        obj = json.loads(envelope); obj["alg"] = "RSA-OAEP"
        with pytest.raises(ValueError): operation(None, private, json.dumps(obj).encode(), b"care-v1")

def test_key_encoding_type_separation_and_malformed_rejection():
    _, sign_public = crypto.generate_signing_keypair(); _, kem_public = crypto.generate_kem_keypair()
    assert isinstance(crypto.load_public_key(crypto.serialize_public_key(sign_public), "signature"), mldsa.MLDSA65PublicKey)
    assert isinstance(crypto.load_public_key(crypto.serialize_public_key(kem_public), "kem"), mlkem.MLKEM768PublicKey)
    with pytest.raises(ValueError): crypto.load_public_key(crypto.serialize_public_key(sign_public), "kem")
    with pytest.raises(ValueError): crypto.load_public_key(b"truncated", "signature")

def test_invalid_and_empty_inputs_fail_closed():
    sign_private, sign_public = crypto.generate_signing_keypair(); kem_private, _ = crypto.generate_kem_keypair()
    for operation in [*SIGN, *ENC]:
        with pytest.raises(ValueError): operation(sign_private, sign_public, b"")
    assert crypto.operation_01(None, sign_public, b'{"v":2,"alg":"RSA","payload":"eA==","signature":"eA=="}') is False
    with pytest.raises(ValueError): crypto.operation_05(None, kem_private, b"not-json")

def test_provision_rotate_revoke_lifecycle_and_stale_key_rejection():
    registry = crypto.KeyRegistry()
    first = registry.provision("service-a")
    assert first["version"] == 1
    active = registry.get_active("service-a", 1)
    assert isinstance(active["signing_private"], mldsa.MLDSA65PrivateKey)
    assert isinstance(active["kem_private"], mlkem.MLKEM768PrivateKey)
    second = registry.rotate("service-a")
    assert second["version"] == 2
    with pytest.raises(ValueError): registry.get_active("service-a", 1)
    registry.revoke("service-a")
    with pytest.raises(ValueError): registry.get_active("service-a", 2)
