"""FIPS 204 custody signature and event-chain operations."""
import hashlib,json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import mldsa


def canonical_handoff(shipment:str,sequence:int,sender:str,recipient:str,location:str,at:int,previous:str)->bytes:
    if not all((shipment,sender,recipient,location)) or sequence<1 or at<=0: raise ValueError("invalid handoff fields")
    return json.dumps({"shipment":shipment,"sequence":sequence,"sender":sender,"recipient":recipient,"location":location,"at":at,"previous":previous,"format":1},sort_keys=True,separators=(",",":")).encode()


def generate_signer(): return mldsa.MLDSA65PrivateKey.generate()
def sign_handoff(payload:bytes,private)->bytes: return private.sign(payload,context=b"shipmentproof-handoff-v1")
def verify_handoff(payload:bytes,signature:bytes,public)->bool:
    try: public.verify(signature,payload,context=b"shipmentproof-handoff-v1"); return True
    except (InvalidSignature,ValueError): return False
def export_public_key(public)->bytes: return public.public_bytes_raw()
def load_public_key(value:bytes): return mldsa.MLDSA65PublicKey.from_public_bytes(value)
def event_digest(payload:bytes,signature:bytes)->str: return hashlib.sha256(payload+signature).hexdigest()
