"""ECDSA baseline for signed credential revocation feeds."""
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import ec
def canonical_feed(feed_id,sequence,issued_at,expires_at,revoked_ids):
 if not feed_id or sequence<1 or issued_at<0 or expires_at<=issued_at:raise ValueError('invalid revocation feed')
 return json.dumps({'feed_id':feed_id,'sequence':sequence,'issued_at':issued_at,'expires_at':expires_at,'revoked_ids':sorted(set(revoked_ids))},sort_keys=True,separators=(',',':')).encode()
def generate_publisher_keypair():
 p=ec.generate_private_key(ec.SECP256R1());return p,p.public_key()
def sign_feed(record,private):return private.sign(record,ec.ECDSA(hashes.SHA256()))
def verify_feed(record,sig,public):
 try:public.verify(sig,record,ec.ECDSA(hashes.SHA256()));return True
 except (InvalidSignature,ValueError):return False
def export_publisher_key(public):return public.public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)
def load_publisher_key(raw):
 p=serialization.load_der_public_key(raw)
 if not isinstance(p,ec.EllipticCurvePublicKey):raise ValueError('expected EC feed key')
 return p
