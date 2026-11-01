"""ML-DSA reference for short-lived API capabilities."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import mldsa
def canonical_capability(token_id,principal,resource,action,expires_at):
 if not all((token_id,principal,resource,action)) or expires_at<=0:raise ValueError('invalid capability')
 return json.dumps({'jti':token_id,'sub':principal,'resource':resource,'action':action,'exp':expires_at},sort_keys=True,separators=(',',':')).encode()
def generate_issuer():return mldsa.MLDSA65PrivateKey.generate()
def sign_capability(payload,private):return private.sign(payload,context=b'capabilitygate-token-v1')
def verify_capability(payload,sig,public):
 try:public.verify(sig,payload,context=b'capabilitygate-token-v1');return True
 except (InvalidSignature,ValueError):return False
def export_issuer(public):return public.public_bytes_raw()
def load_issuer(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
