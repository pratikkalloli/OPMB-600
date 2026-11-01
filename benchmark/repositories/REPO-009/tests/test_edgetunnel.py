from cryptography.hazmat.primitives.asymmetric import rsa
from edgetunnel.crypto import operation_01, operation_02, operation_03, operation_04, operation_05, operation_06, operation_07, operation_08, operation_09, operation_10

def test_signature_envelopes_roundtrip_and_context_binding():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    for operation in (operation_01, operation_02, operation_03, operation_04, operation_08, operation_09, operation_10):
        envelope = operation(private, None, b"record")
        assert operation(None, private.public_key(), envelope, b"opmb-v1") is True
        assert operation(None, private.public_key(), envelope, b"wrong-context") is False

def test_oaep_operations_roundtrip_and_context_binding():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    for operation in (operation_05, operation_06, operation_07):
        ciphertext = operation(private, None, b"synthetic-data-key", b"context")
        assert operation(None, private, ciphertext, b"context") == b"synthetic-data-key"
        try:
            operation(None, private, ciphertext, b"other")
        except Exception:
            pass
        else:
            raise AssertionError("context mismatch must fail")

def test_every_operation_rejects_empty_input():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    for operation in (operation_01, operation_02, operation_03, operation_04, operation_05, operation_06, operation_07, operation_08, operation_09, operation_10):
        try:
            operation(private, private.public_key(), b"")
        except ValueError:
            pass
        else:
            raise AssertionError("empty payload must fail")
