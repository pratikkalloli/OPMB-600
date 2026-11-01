"""ML-DSA reference for research consent authorization records."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import mldsa
def canonical_consent(consent_id,subject,study,scope,expires_at,revision):
 if not all((consent_id,subject,study,scope)) or expires_at<=0 or revision<1:raise ValueError('invalid consent record')
 return json.dumps({'consent_id':consent_id,'subject':subject,'study':study,'scope':scope,'expires_at':expires_at,'revision':revision},sort_keys=True,separators=(',',':')).encode()
def generate_authority():return mldsa.MLDSA65PrivateKey.generate()
def sign_consent(record,private):return private.sign(record,context=b'careconsent-grant-v1')
def verify_consent(record,signature,public):
 try:public.verify(signature,record,context=b'careconsent-grant-v1');return True
 except (InvalidSignature,ValueError):return False
def export_authority(public):return public.public_bytes_raw()
def load_authority(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
