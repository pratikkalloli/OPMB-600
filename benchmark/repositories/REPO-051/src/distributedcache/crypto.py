"""X25519 session establishment, snapshot AEAD and ECDSA identity proof."""
from __future__ import annotations
import hashlib,json,os
from dataclasses import dataclass
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import ec,x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat

@dataclass(frozen=True)
class SnapshotEnvelope:
    snapshot_id:str; source:str; target:str; version:int; nonce:bytes; ciphertext:bytes; signature:bytes

def generate_node_keypair():
 p=x25519.X25519PrivateKey.generate(); return p,p.public_key()
def derive_session_key(private,peer_public,source:str,target:str)->bytes:
 if not source or not target or source==target: raise ValueError("invalid cache node pair")
 secret=private.exchange(peer_public); info=f"cache-session-v1:{source}:{target}".encode()
 return HKDF(algorithm=hashes.SHA256(),length=32,salt=hashlib.sha256(b"distributedcache").digest(),info=info).derive(secret)
def generate_signer():
 p=ec.generate_private_key(ec.SECP256R1()); return p,p.public_key()
def _metadata(snapshot_id,source,target,version,nonce,ciphertext):
 return json.dumps({'id':snapshot_id,'source':source,'target':target,'version':version,'nonce':nonce.hex(),'ciphertext_sha256':hashlib.sha256(ciphertext).hexdigest()},sort_keys=True,separators=(',',':')).encode()
def seal_snapshot(snapshot_id:str,source:str,target:str,version:int,plaintext:bytes,session_key:bytes,signing_private)->SnapshotEnvelope:
 if not snapshot_id or version<1 or not plaintext or len(session_key)!=32: raise ValueError("invalid cache snapshot")
 nonce=os.urandom(12); aad=f"{snapshot_id}:{source}:{target}:{version}".encode(); ciphertext=AESGCM(session_key).encrypt(nonce,plaintext,aad)
 signature=signing_private.sign(_metadata(snapshot_id,source,target,version,nonce,ciphertext),ec.ECDSA(hashes.SHA256()))
 return SnapshotEnvelope(snapshot_id,source,target,version,nonce,ciphertext,signature)
def open_snapshot(envelope:SnapshotEnvelope,session_key:bytes,signing_public)->bytes:
 try: signing_public.verify(envelope.signature,_metadata(envelope.snapshot_id,envelope.source,envelope.target,envelope.version,envelope.nonce,envelope.ciphertext),ec.ECDSA(hashes.SHA256()))
 except (InvalidSignature,ValueError) as exc: raise ValueError("cache snapshot signature invalid") from exc
 aad=f"{envelope.snapshot_id}:{envelope.source}:{envelope.target}:{envelope.version}".encode()
 try: return AESGCM(session_key).decrypt(envelope.nonce,envelope.ciphertext,aad)
 except (InvalidTag,ValueError) as exc: raise ValueError("cache snapshot authentication failed") from exc
def export_node_key(public): return public.public_bytes(Encoding.Raw,PublicFormat.Raw)
def load_node_key(raw:bytes): return x25519.X25519PublicKey.from_public_bytes(raw)
