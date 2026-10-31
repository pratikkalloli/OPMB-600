import pytest
from cryptography.hazmat.primitives.asymmetric import mldsa,mlkem
from securevault_pqc.crypto import (VaultCryptoError,decrypt_blob,encrypt_blob,generate_recipient_keypair,generate_signing_keypair,load_public_key,serialize_public_key,sign_manifest,unwrap_data_key,verify_manifest,wrap_data_key,rotate_object_key)
from securevault_pqc.service import SecureVaultPQC

def test_fips203_wrap_round_trip_and_authentication():
    private,public=generate_recipient_keypair(); wrapped=wrap_data_key(b"d"*32,public,object_id="obj")
    assert unwrap_data_key(wrapped,private,object_id="obj")==b"d"*32
    with pytest.raises(VaultCryptoError): unwrap_data_key(wrapped,private,object_id="wrong")

def test_fips204_signature_and_tamper_rejection():
    private,public=generate_signing_keypair(); signature=sign_manifest(b"manifest",private)
    assert verify_manifest(b"manifest",signature,public)
    assert not verify_manifest(b"tampered",signature,public)

def test_data_aead_rejects_tampering():
    nonce,cipher=encrypt_blob(b"secret",b"k"*32,object_id="item")
    with pytest.raises(VaultCryptoError): decrypt_blob(nonce,cipher[:-1]+bytes([cipher[-1]^1]),b"k"*32,object_id="item")

def test_key_serialization_and_rotation():
    old_private,old_public=generate_recipient_keypair(); new_private,new_public=generate_recipient_keypair()
    assert isinstance(load_public_key(serialize_public_key(old_public)),mlkem.MLKEM768PublicKey)
    wrapped=wrap_data_key(b"z"*32,old_public,object_id="x")
    rotated=rotate_object_key(wrapped,old_private,new_public,object_id="x")
    assert unwrap_data_key(rotated,new_private,object_id="x")==b"z"*32

def test_migrated_service_document_round_trip(tmp_path):
    private,public=generate_recipient_keypair(); signer,_=generate_signing_keypair(); vault=SecureVaultPQC(tmp_path/"pqc.db",public,private,signer)
    item=vault.import_document("record.txt",b"controlled sample")
    assert vault.retrieve_document(item)==("record.txt",b"controlled sample")


def test_fips203_rejects_wrong_recipient():
    _,recipient=generate_recipient_keypair(); wrong,_=generate_recipient_keypair()
    wrapped=wrap_data_key(b"d"*32,recipient,object_id="obj")
    with pytest.raises(VaultCryptoError): unwrap_data_key(wrapped,wrong,object_id="obj")

def test_fips204_rejects_wrong_public_key():
    private,_=generate_signing_keypair(); _,wrong=generate_signing_keypair()
    signature=sign_manifest(b"manifest",private)
    assert not verify_manifest(b"manifest",signature,wrong)

def test_malformed_mlkem_public_key_is_rejected():
    with pytest.raises(VaultCryptoError): load_public_key(b"not a public key")


def test_stored_nonce_is_covered_by_signed_manifest(tmp_path):
    import sqlite3
    private,public=generate_recipient_keypair(); signer,_=generate_signing_keypair(); database=tmp_path/"vault.db"
    vault=SecureVaultPQC(database,public,private,signer); object_id=vault.import_document("proof.txt",b"content")
    with sqlite3.connect(database) as db: db.execute("UPDATE objects SET nonce=? WHERE object_id=?",(b"n"*12,object_id))
    with pytest.raises(VaultCryptoError,match="manifest signature"):
        vault.retrieve_document(object_id)
