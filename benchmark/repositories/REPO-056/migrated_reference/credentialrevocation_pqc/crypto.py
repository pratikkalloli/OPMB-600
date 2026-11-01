"""ML-DSA reference for signed credential revocation feeds."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import mldsa
def canonical_feed(feed_id,sequence,issued_at,expires_at,revoked_ids):
 if not feed_id or sequence<1 or issued_at<0 or expires_at<=issued_at:raise ValueError('invalid revocation feed')
 return json.dumps({'feed_id':feed_id,'sequence':sequence,'issued_at':issued_at,'expires_at':expires_at,'revoked_ids':sorted(set(revoked_ids))},sort_keys=True,separators=(',',':')).encode()
def generate_publisher_keypair():return mldsa.MLDSA65PrivateKey.generate()
def sign_feed(record,private):return private.sign(record,context=b'credential-revocation-feed-v1')
def verify_feed(record,sig,public):
 try:public.verify(sig,record,context=b'credential-revocation-feed-v1');return True
 except (InvalidSignature,ValueError):return False
def export_publisher_key(public):return public.public_bytes_raw()
def load_publisher_key(raw):return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
