"""Classical cryptographic operations in the synthetic BackupRelay benchmark."""
from __future__ import annotations

def operation_01(private_key, public_key, payload: bytes, context: bytes = b"opmb-v1") -> bytes | bool:
    """Baseline rsa key-pair provisioning operation; synthetic data only."""
    if not isinstance(payload, bytes) or not payload:
        raise ValueError("payload must be non-empty bytes")
    import base64, json
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    if private_key is not None:
        signature = private_key.sign(context + b"\x00" + payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return json.dumps({"payload": base64.b64encode(payload).decode(), "signature": base64.b64encode(signature).decode()}, sort_keys=True).encode()
    try:
        envelope = json.loads(payload)
        signed_payload = base64.b64decode(envelope["payload"], validate=True)
        signature = base64.b64decode(envelope["signature"], validate=True)
        public_key.verify(signature, context + b"\x00" + signed_payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except Exception:
        return False

def operation_02(private_key, public_key, payload: bytes, context: bytes = b"opmb-v1") -> bytes | bool:
    """Baseline public-key serialization operation; synthetic data only."""
    if not isinstance(payload, bytes) or not payload:
        raise ValueError("payload must be non-empty bytes")
    import base64, json
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    if private_key is not None:
        signature = private_key.sign(context + b"\x00" + payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return json.dumps({"payload": base64.b64encode(payload).decode(), "signature": base64.b64encode(signature).decode()}, sort_keys=True).encode()
    try:
        envelope = json.loads(payload)
        signed_payload = base64.b64decode(envelope["payload"], validate=True)
        signature = base64.b64decode(envelope["signature"], validate=True)
        public_key.verify(signature, context + b"\x00" + signed_payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except Exception:
        return False

def operation_03(private_key, public_key, payload: bytes, context: bytes = b"opmb-v1") -> bytes | bool:
    """Baseline detached record signing operation; synthetic data only."""
    if not isinstance(payload, bytes) or not payload:
        raise ValueError("payload must be non-empty bytes")
    import base64, json
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    if private_key is not None:
        signature = private_key.sign(context + b"\x00" + payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return json.dumps({"payload": base64.b64encode(payload).decode(), "signature": base64.b64encode(signature).decode()}, sort_keys=True).encode()
    try:
        envelope = json.loads(payload)
        signed_payload = base64.b64decode(envelope["payload"], validate=True)
        signature = base64.b64decode(envelope["signature"], validate=True)
        public_key.verify(signature, context + b"\x00" + signed_payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except Exception:
        return False

def operation_04(private_key, public_key, payload: bytes, context: bytes = b"opmb-v1") -> bytes | bool:
    """Baseline signature verification policy operation; synthetic data only."""
    if not isinstance(payload, bytes) or not payload:
        raise ValueError("payload must be non-empty bytes")
    import base64, json
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    if private_key is not None:
        signature = private_key.sign(context + b"\x00" + payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return json.dumps({"payload": base64.b64encode(payload).decode(), "signature": base64.b64encode(signature).decode()}, sort_keys=True).encode()
    try:
        envelope = json.loads(payload)
        signed_payload = base64.b64decode(envelope["payload"], validate=True)
        signature = base64.b64decode(envelope["signature"], validate=True)
        public_key.verify(signature, context + b"\x00" + signed_payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except Exception:
        return False

def operation_05(private_key, public_key, payload: bytes, context: bytes = b"opmb-v1") -> bytes | bool:
    """Baseline recipient key establishment operation; synthetic data only."""
    if not isinstance(payload, bytes) or not payload:
        raise ValueError("payload must be non-empty bytes")
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    if private_key is not None:
        return private_key.public_key().encrypt(payload, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=context))
    return public_key.decrypt(payload, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=context))

def operation_06(private_key, public_key, payload: bytes, context: bytes = b"opmb-v1") -> bytes | bool:
    """Baseline envelope encoding operation; synthetic data only."""
    if not isinstance(payload, bytes) or not payload:
        raise ValueError("payload must be non-empty bytes")
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    if private_key is not None:
        return private_key.public_key().encrypt(payload, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=context))
    return public_key.decrypt(payload, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=context))

def operation_07(private_key, public_key, payload: bytes, context: bytes = b"opmb-v1") -> bytes | bool:
    """Baseline tamper and context binding operation; synthetic data only."""
    if not isinstance(payload, bytes) or not payload:
        raise ValueError("payload must be non-empty bytes")
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    if private_key is not None:
        return private_key.public_key().encrypt(payload, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=context))
    return public_key.decrypt(payload, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=context))

def operation_08(private_key, public_key, payload: bytes, context: bytes = b"opmb-v1") -> bytes | bool:
    """Baseline key rotation and revocation operation; synthetic data only."""
    if not isinstance(payload, bytes) or not payload:
        raise ValueError("payload must be non-empty bytes")
    import base64, json
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    if private_key is not None:
        signature = private_key.sign(context + b"\x00" + payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return json.dumps({"payload": base64.b64encode(payload).decode(), "signature": base64.b64encode(signature).decode()}, sort_keys=True).encode()
    try:
        envelope = json.loads(payload)
        signed_payload = base64.b64decode(envelope["payload"], validate=True)
        signature = base64.b64decode(envelope["signature"], validate=True)
        public_key.verify(signature, context + b"\x00" + signed_payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except Exception:
        return False

def operation_09(private_key, public_key, payload: bytes, context: bytes = b"opmb-v1") -> bytes | bool:
    """Baseline dependency and api migration operation; synthetic data only."""
    if not isinstance(payload, bytes) or not payload:
        raise ValueError("payload must be non-empty bytes")
    import base64, json
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    if private_key is not None:
        signature = private_key.sign(context + b"\x00" + payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return json.dumps({"payload": base64.b64encode(payload).decode(), "signature": base64.b64encode(signature).decode()}, sort_keys=True).encode()
    try:
        envelope = json.loads(payload)
        signed_payload = base64.b64decode(envelope["payload"], validate=True)
        signature = base64.b64decode(envelope["signature"], validate=True)
        public_key.verify(signature, context + b"\x00" + signed_payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except Exception:
        return False

def operation_10(private_key, public_key, payload: bytes, context: bytes = b"opmb-v1") -> bytes | bool:
    """Baseline cross-component migration and regression operation; synthetic data only."""
    if not isinstance(payload, bytes) or not payload:
        raise ValueError("payload must be non-empty bytes")
    import base64, json
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    if private_key is not None:
        signature = private_key.sign(context + b"\x00" + payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return json.dumps({"payload": base64.b64encode(payload).decode(), "signature": base64.b64encode(signature).decode()}, sort_keys=True).encode()
    try:
        envelope = json.loads(payload)
        signed_payload = base64.b64decode(envelope["payload"], validate=True)
        signature = base64.b64decode(envelope["signature"], validate=True)
        public_key.verify(signature, context + b"\x00" + signed_payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except Exception:
        return False
