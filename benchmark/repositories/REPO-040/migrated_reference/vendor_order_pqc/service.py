"""PQC reference for VendorOrder: Buyer and supplier purchase orders with currency, integer totals, and fulfillment transitions."""
from __future__ import annotations
import hashlib,json,os
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mlkem, mldsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

_CONTEXT="vendor_order:v1".encode()
_CONFIG={"entity":"purchase_order","fields":["order_id","buyer_id","supplier_id","currency","total_cents","created_at","status"],"state":"status","states":["draft","submitted","accepted","fulfilled","cancelled"],"transitions":{"draft":["submitted","cancelled"],"submitted":["accepted","cancelled"],"accepted":["fulfilled","cancelled"],"fulfilled":[],"cancelled":[]},"identifier":"order_id"}

def _aad(entity_id: str) -> bytes:
    if not entity_id: raise ValueError("entity ID required")
    return _CONTEXT+b":"+entity_id.encode()

def _signed_bytes(record) -> bytes:
    return _CONTEXT+b":decision:"+json.dumps(record,sort_keys=True,separators=(",",":"),allow_nan=False).encode()

def _derive(shared: bytes,entity_id: str) -> bytes:
    if not entity_id: raise ValueError("entity ID required")
    return HKDF(algorithm=hashes.SHA256(),length=32,salt=hashlib.sha256(_CONTEXT).digest(),info=_CONTEXT+b":"+entity_id.encode()).derive(shared)

def build_purchase_order(data: dict) -> dict:
    if not isinstance(data,dict): raise ValueError("purchase_order must be a mapping")
    missing=[field for field in _CONFIG["fields"] if field not in data]
    if missing: raise ValueError("missing required purchase_order fields")
    if not isinstance(data[_CONFIG["identifier"]],str) or not data[_CONFIG["identifier"]]: raise ValueError("invalid purchase_order identifier")
    if data[_CONFIG["state"]] not in _CONFIG["states"]: raise ValueError("invalid purchase_order lifecycle state")
    if not (isinstance(data["total_cents"],int) and data["total_cents"]>0 and len(data["currency"])==3 and data["currency"].isalpha() and data["currency"].isupper()): raise ValueError("invalid purchase_order domain invariant")
    try: return json.loads(json.dumps(data,sort_keys=True,separators=(",",":"),allow_nan=False))
    except (TypeError,ValueError) as exc: raise ValueError("purchase_order fields must be JSON-safe") from exc

def generate_purchase_order_signing_keypair():
    private=mldsa.MLDSA65PrivateKey.generate()
    return private,private.public_key()

def sign_purchase_order_decision(record,private) -> bytes:
    return private.sign(_signed_bytes(record))

def verify_purchase_order_decision(record,signature,public) -> bool:
    try:
        public.verify(signature,_signed_bytes(record))
        return True
    except (InvalidSignature,ValueError,TypeError): return False

def generate_purchase_order_recipient_keypair():
    private=mlkem.MLKEM768PrivateKey.generate()
    return private,private.public_key()

def seal_purchase_order_attachment(cleartext: bytes,recipient_public,entity_id: str) -> bytes:
    if not isinstance(cleartext,bytes) or not entity_id: raise ValueError("cleartext and purchase_order ID are required")
    data_key=os.urandom(32)
    shared,kem_ciphertext=recipient_public.encapsulate()
    wrapping_key=_derive(shared,entity_id)
    wrap_nonce=os.urandom(12); payload_nonce=os.urandom(12); aad=_aad(entity_id)
    wrapped_key=AESGCM(wrapping_key).encrypt(wrap_nonce,data_key,aad)
    ciphertext=AESGCM(data_key).encrypt(payload_nonce,cleartext,aad)
    return kem_ciphertext+wrap_nonce+payload_nonce+wrapped_key+ciphertext

def open_purchase_order_attachment(envelope: bytes,recipient_private,entity_id: str) -> bytes:
    if len(envelope)<1088+24+48+16 or not entity_id: raise ValueError("invalid purchase_order envelope")
    kem_ciphertext,wrap_nonce,payload_nonce=envelope[:1088],envelope[1088:1100],envelope[1100:1112]
    wrapped_key=envelope[1112:1160]; ciphertext=envelope[1160:]
    try:
        wrapping_key=_derive(recipient_private.decapsulate(kem_ciphertext),entity_id)
        data_key=AESGCM(wrapping_key).decrypt(wrap_nonce,wrapped_key,_aad(entity_id))
        if len(data_key)!=32: raise ValueError("invalid data key")
        return AESGCM(data_key).decrypt(payload_nonce,ciphertext,_aad(entity_id))
    except (InvalidTag,ValueError,TypeError) as exc: raise ValueError("purchase_order envelope authentication failed") from exc

def encode_purchase_order_recipient_public(public) -> bytes:
    return public.public_bytes_raw()

def load_purchase_order_recipient_public(data: bytes):
    try: return mlkem.MLKEM768PublicKey.from_public_bytes(data)
    except (ValueError,TypeError) as exc: raise ValueError("invalid ML-KEM recipient key") from exc

def rotate_purchase_order_attachment(envelope: bytes,old_private,new_public,entity_id: str) -> bytes:
    return seal_purchase_order_attachment(open_purchase_order_attachment(envelope,old_private,entity_id),new_public,entity_id)

def validate_purchase_order_transition(previous: bytes,proposed: bytes) -> bool:
    try: old=json.loads(previous); new=json.loads(proposed)
    except (TypeError,ValueError): return False
    ident=_CONFIG["identifier"]; state=_CONFIG["state"]
    if old.get(ident)!=new.get(ident) or old.get(state) not in _CONFIG["transitions"]: return False
    return new.get(state) in _CONFIG["transitions"][old[state]]
