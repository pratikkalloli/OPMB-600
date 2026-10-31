"""SecureVault service using standardized post-quantum primitives."""
from __future__ import annotations
import hashlib,json,logging,os,uuid
from pathlib import Path
from dataclasses import dataclass
from .crypto import (decrypt_blob,encrypt_blob,generate_signing_keypair,sign_manifest,unwrap_data_key,verify_manifest,wrap_data_key,VaultCryptoError)
from .store import SealedObject,VaultStore
logger=logging.getLogger(__name__)
@dataclass(frozen=True)
class VaultConfig:
    max_document_bytes:int=5_000_000
    def __post_init__(self)->None:
        if self.max_document_bytes<=0: raise ValueError("max_document_bytes must be positive")
class SecureVaultPQC:
    """Reference service with ML-KEM key establishment and ML-DSA signatures."""
    def __init__(self,database:str|Path,recipient_public,recipient_private,signing_private=None,config:VaultConfig=VaultConfig())->None:
        self.store=VaultStore(database); self.recipient_public=recipient_public; self.recipient_private=recipient_private; self.config=config; self.signing_private=signing_private or generate_signing_keypair()[0]
    @staticmethod
    def _manifest(item:SealedObject)->bytes:
        return json.dumps({"id":item.object_id,"filename":item.filename,"sha256":hashlib.sha256(item.ciphertext).hexdigest()},sort_keys=True,separators=(",",":")).encode()
    def import_document(self,filename:str,content:bytes)->str:
        if not filename or Path(filename).name!=filename or filename in {".",".."}: raise ValueError("filename must be a plain basename")
        if not isinstance(content,bytes) or not content: raise ValueError("document must contain bytes")
        if len(content)>self.config.max_document_bytes: raise ValueError("document exceeds configured size limit")
        object_id=uuid.uuid4().hex; data_key=os.urandom(32); nonce,ciphertext=encrypt_blob(content,data_key,object_id=object_id)
        wrapped=wrap_data_key(data_key,self.recipient_public,object_id=object_id); unsigned=SealedObject(object_id,filename,nonce,ciphertext,wrapped,b"")
        item=SealedObject(object_id,filename,nonce,ciphertext,wrapped,sign_manifest(self._manifest(unsigned),self.signing_private))
        self.store.put(item); logger.info("document_imported",extra={"object_id":object_id,"size":len(content)}); return object_id
    def retrieve_document(self,object_id:str)->tuple[str,bytes]:
        item=self.store.get(object_id)
        if item is None: raise KeyError("document not found")
        if not verify_manifest(self._manifest(item),item.signature,self.signing_private.public_key()): raise VaultCryptoError("document manifest signature invalid")
        data_key=unwrap_data_key(item.wrapped_key,self.recipient_private,object_id=object_id)
        return item.filename,decrypt_blob(item.nonce,item.ciphertext,data_key,object_id=object_id)
    def remove_document(self,object_id:str)->bool: return self.store.delete(object_id)
