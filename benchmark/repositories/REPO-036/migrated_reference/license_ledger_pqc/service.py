"""PQC reference for LicenseLedger: Product license records covering organization, seats, validity windows, suspension, and revocation."""
from __future__ import annotations
import hashlib,json,os
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mlkem, mldsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

_CONTEXT="license_ledger:v1".encode()
_CONFIG={"entity":"license_record","fields":["license_id","product_id","organization_id","seat_count","expires_at","status"],"state":"status","states":["trial","active","suspended","revoked"],"transitions":{"trial":["active","revoked"],"active":["suspended","revoked"],"suspended":["active","revoked"],"revoked":[]},"identifier":"license_id"}

def _aad(entity_id: str) -> bytes:
    if not entity_id: raise ValueError("entity ID required")
    return _CONTEXT+b":"+entity_id.encode()

def _signed_bytes(record) -> bytes:
    return _CONTEXT+b":decision:"+json.dumps(record,sort_keys=True,separators=(",",":"),allow_nan=False).encode()

def _derive(shared: bytes,entity_id: str) -> bytes:
    if not entity_id: raise ValueError("entity ID required")
    return HKDF(algorithm=hashes.SHA256(),length=32,salt=hashlib.sha256(_CONTEXT).digest(),info=_CONTEXT+b":"+entity_id.encode()).derive(shared)

def build_license_record(data: dict) -> dict:
    if not isinstance(data,dict): raise ValueError("license_record must be a mapping")
    missing=[field for field in _CONFIG["fields"] if field not in data]
    if missing: raise ValueError("missing required license_record fields")
    if not isinstance(data[_CONFIG["identifier"]],str) or not data[_CONFIG["identifier"]]: raise ValueError("invalid license_record identifier")
    if data[_CONFIG["state"]] not in _CONFIG["states"]: raise ValueError("invalid license_record lifecycle state")
    if not (isinstance(data["seat_count"],int) and data["seat_count"]>0 and data["expires_at"]>0): raise ValueError("invalid license_record domain invariant")
    try: return json.loads(json.dumps(data,sort_keys=True,separators=(",",":"),allow_nan=False))
    except (TypeError,ValueError) as exc: raise ValueError("license_record fields must be JSON-safe") from exc

def generate_license_record_signing_keypair():
    private=mldsa.MLDSA65PrivateKey.generate()
    return private,private.public_key()

def sign_license_record_decision(record,private) -> bytes:
    return private.sign(_signed_bytes(record))

def verify_license_record_decision(record,signature,public) -> bool:
    try:
        public.verify(signature,_signed_bytes(record))
        return True
    except (InvalidSignature,ValueError,TypeError): return False

def generate_license_record_recipient_keypair():
    private=mlkem.MLKEM768PrivateKey.generate()
    return private,private.public_key()

def seal_license_record_attachment(cleartext: bytes,recipient_public,entity_id: str) -> bytes:
    if not isinstance(cleartext,bytes) or not entity_id: raise ValueError("cleartext and license_record ID are required")
    data_key=os.urandom(32)
    shared,kem_ciphertext=recipient_public.encapsulate()
    wrapping_key=_derive(shared,entity_id)
    wrap_nonce=os.urandom(12); payload_nonce=os.urandom(12); aad=_aad(entity_id)
    wrapped_key=AESGCM(wrapping_key).encrypt(wrap_nonce,data_key,aad)
    ciphertext=AESGCM(data_key).encrypt(payload_nonce,cleartext,aad)
    return kem_ciphertext+wrap_nonce+payload_nonce+wrapped_key+ciphertext

def open_license_record_attachment(envelope: bytes,recipient_private,entity_id: str) -> bytes:
    if len(envelope)<1088+24+48+16 or not entity_id: raise ValueError("invalid license_record envelope")
    kem_ciphertext,wrap_nonce,payload_nonce=envelope[:1088],envelope[1088:1100],envelope[1100:1112]
    wrapped_key=envelope[1112:1160]; ciphertext=envelope[1160:]
    try:
        wrapping_key=_derive(recipient_private.decapsulate(kem_ciphertext),entity_id)
        data_key=AESGCM(wrapping_key).decrypt(wrap_nonce,wrapped_key,_aad(entity_id))
        if len(data_key)!=32: raise ValueError("invalid data key")
        return AESGCM(data_key).decrypt(payload_nonce,ciphertext,_aad(entity_id))
    except (InvalidTag,ValueError,TypeError) as exc: raise ValueError("license_record envelope authentication failed") from exc

def encode_license_record_recipient_public(public) -> bytes:
    return public.public_bytes_raw()

def load_license_record_recipient_public(data: bytes):
    try: return mlkem.MLKEM768PublicKey.from_public_bytes(data)
    except (ValueError,TypeError) as exc: raise ValueError("invalid ML-KEM recipient key") from exc

def rotate_license_record_attachment(envelope: bytes,old_private,new_public,entity_id: str) -> bytes:
    return seal_license_record_attachment(open_license_record_attachment(envelope,old_private,entity_id),new_public,entity_id)

def validate_license_record_transition(previous: bytes,proposed: bytes) -> bool:
    try: old=json.loads(previous); new=json.loads(proposed)
    except (TypeError,ValueError): return False
    ident=_CONFIG["identifier"]; state=_CONFIG["state"]
    if old.get(ident)!=new.get(ident) or old.get(state) not in _CONFIG["transitions"]: return False
    return new.get(state) in _CONFIG["transitions"][old[state]]
