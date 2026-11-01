"""Classical baseline for KeyRecovery: Threshold recovery cases tracking principal, key fingerprint, required approvals, and fulfillment decisions."""
from __future__ import annotations
import hashlib,json,os
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

_CONTEXT="key_recovery:v1".encode()
_CONFIG={"entity":"recovery_case","fields":["recovery_id","principal_id","key_fingerprint","approvals_required","opened_at","recovery_state"],"state":"recovery_state","states":["opened","approved","fulfilled","denied"],"transitions":{"opened":["approved","denied"],"approved":["fulfilled","denied"],"fulfilled":[],"denied":[]},"identifier":"recovery_id"}

def _aad(entity_id: str) -> bytes:
    if not entity_id: raise ValueError("entity ID required")
    return _CONTEXT+b":"+entity_id.encode()

def _signed_bytes(record) -> bytes:
    return _CONTEXT+b":decision:"+json.dumps(record,sort_keys=True,separators=(",",":"),allow_nan=False).encode()

def build_recovery_case(data: dict) -> dict:
    if not isinstance(data,dict): raise ValueError("recovery_case must be a mapping")
    missing=[field for field in _CONFIG["fields"] if field not in data]
    if missing: raise ValueError("missing required recovery_case fields")
    if not isinstance(data[_CONFIG["identifier"]],str) or not data[_CONFIG["identifier"]]: raise ValueError("invalid recovery_case identifier")
    if data[_CONFIG["state"]] not in _CONFIG["states"]: raise ValueError("invalid recovery_case lifecycle state")
    if not (isinstance(data["approvals_required"],int) and 2<=data["approvals_required"]<=5): raise ValueError("invalid recovery_case domain invariant")
    try: return json.loads(json.dumps(data,sort_keys=True,separators=(",",":"),allow_nan=False))
    except (TypeError,ValueError) as exc: raise ValueError("recovery_case fields must be JSON-safe") from exc

def generate_recovery_case_signing_keypair():
    private=rsa.generate_private_key(public_exponent=65537,key_size=3072)
    return private,private.public_key()

def sign_recovery_case_decision(record,private) -> bytes:
    return private.sign(_signed_bytes(record),padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())

def verify_recovery_case_decision(record,signature,public) -> bool:
    try:
        public.verify(signature,_signed_bytes(record),padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
        return True
    except (InvalidSignature,ValueError,TypeError): return False

def generate_recovery_case_recipient_keypair():
    private=rsa.generate_private_key(public_exponent=65537,key_size=3072)
    return private,private.public_key()

def seal_recovery_case_attachment(cleartext: bytes,recipient_public,entity_id: str) -> bytes:
    if not isinstance(cleartext,bytes) or not entity_id: raise ValueError("cleartext and recovery_case ID are required")
    data_key=os.urandom(32)
    wrapped_key=recipient_public.encrypt(data_key,padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=_CONTEXT))
    payload_nonce=os.urandom(12); ciphertext=AESGCM(data_key).encrypt(payload_nonce,cleartext,_aad(entity_id))
    return wrapped_key+payload_nonce+ciphertext

def open_recovery_case_attachment(envelope: bytes,recipient_private,entity_id: str) -> bytes:
    if len(envelope)<384+12+16 or not entity_id: raise ValueError("invalid recovery_case envelope")
    wrapped_key,payload_nonce,ciphertext=envelope[:384],envelope[384:396],envelope[396:]
    try:
        data_key=recipient_private.decrypt(wrapped_key,padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=_CONTEXT))
        if len(data_key)!=32: raise ValueError("invalid data key")
        return AESGCM(data_key).decrypt(payload_nonce,ciphertext,_aad(entity_id))
    except (InvalidTag,ValueError,TypeError) as exc: raise ValueError("recovery_case envelope authentication failed") from exc

def encode_recovery_case_recipient_public(public) -> bytes:
    return public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)

def load_recovery_case_recipient_public(data: bytes):
    key=serialization.load_pem_public_key(data)
    if not isinstance(key,rsa.RSAPublicKey): raise ValueError("expected RSA recipient key")
    return key

def rotate_recovery_case_attachment(envelope: bytes,old_private,new_public,entity_id: str) -> bytes:
    return seal_recovery_case_attachment(open_recovery_case_attachment(envelope,old_private,entity_id),new_public,entity_id)

def validate_recovery_case_transition(previous: bytes,proposed: bytes) -> bool:
    try: old=json.loads(previous); new=json.loads(proposed)
    except (TypeError,ValueError): return False
    ident=_CONFIG["identifier"]; state=_CONFIG["state"]
    if old.get(ident)!=new.get(ident) or old.get(state) not in _CONFIG["transitions"]: return False
    return new.get(state) in _CONFIG["transitions"][old[state]]
