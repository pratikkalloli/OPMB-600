"""PQC session establishment and authenticated cache snapshot transfer."""
from __future__ import annotations
import hashlib,json,os
from dataclasses import dataclass
from cryptography.exceptions import InvalidSignature,InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mldsa,mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

@dataclass(frozen=True)
class SnapshotEnvelope:
 snapshot_id:str; source:str; target:str; version:int; encapsulation:bytes; nonce:bytes; ciphertext:bytes; signature:bytes
def generate_node_keypair():
 p=mlkem.MLKEM768PrivateKey.generate(); return p,p.public_key()
def encapsulate_session(target_public,source:str,target:str)->tuple[bytes,bytes]:
 if not source or not target or source==target: raise ValueError("invalid cache node pair")
 shared,ct=target_public.encapsulate(); info=f"cache-session-v1:{source}:{target}".encode(); key=HKDF(algorithm=hashes.SHA256(),length=32,salt=hashlib.sha256(b"distributedcache").digest(),info=info).derive(shared); return ct,key
def decapsulate_session(private,encapsulation:bytes,source:str,target:str)->bytes:
 if not source or not target or source==target: raise ValueError("invalid cache node pair")
 shared=private.decapsulate(encapsulation); info=f"cache-session-v1:{source}:{target}".encode(); return HKDF(algorithm=hashes.SHA256(),length=32,salt=hashlib.sha256(b"distributedcache").digest(),info=info).derive(shared)
def generate_signer(): return mldsa.MLDSA65PrivateKey.generate()
def _metadata(sid,source,target,version,encapsulation,nonce,ciphertext): return json.dumps({'id':sid,'source':source,'target':target,'version':version,'kem':encapsulation.hex(),'nonce':nonce.hex(),'ciphertext_sha256':hashlib.sha256(ciphertext).hexdigest()},sort_keys=True,separators=(',',':')).encode()
def seal_snapshot(snapshot_id,source,target,version,plaintext,session_key,signing_private,encapsulation=b""):
 if not snapshot_id or version<1 or not plaintext or len(session_key)!=32: raise ValueError("invalid cache snapshot")
 nonce=os.urandom(12); aad=f"{snapshot_id}:{source}:{target}:{version}".encode(); ciphertext=AESGCM(session_key).encrypt(nonce,plaintext,aad); signature=signing_private.sign(_metadata(snapshot_id,source,target,version,encapsulation,nonce,ciphertext),context=b"distributedcache-snapshot-v1")
 return SnapshotEnvelope(snapshot_id,source,target,version,encapsulation,nonce,ciphertext,signature)
def open_snapshot(envelope,session_key,signing_public):
 try: signing_public.verify(envelope.signature,_metadata(envelope.snapshot_id,envelope.source,envelope.target,envelope.version,envelope.encapsulation,envelope.nonce,envelope.ciphertext),context=b"distributedcache-snapshot-v1")
 except (InvalidSignature,ValueError) as exc: raise ValueError("cache snapshot signature invalid") from exc
 try: return AESGCM(session_key).decrypt(envelope.nonce,envelope.ciphertext,f"{envelope.snapshot_id}:{envelope.source}:{envelope.target}:{envelope.version}".encode())
 except (InvalidTag,ValueError) as exc: raise ValueError("cache snapshot authentication failed") from exc
def export_node_key(public): return public.public_bytes_raw()
def load_node_key(raw:bytes): return mlkem.MLKEM768PublicKey.from_public_bytes(raw)
def export_signer_key(public): return public.public_bytes_raw()
def load_signer_key(raw:bytes): return mldsa.MLDSA65PublicKey.from_public_bytes(raw)
