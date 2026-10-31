import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from securevault.crypto import (VaultCryptoError, decrypt_blob, encrypt_blob, generate_recipient_keypair, generate_signing_keypair, load_public_key, serialize_public_key, sign_manifest, verify_manifest, wrap_data_key, unwrap_data_key)
from securevault.service import SecureVault, VaultConfig

def test_import_and_retrieve_round_trip(tmp_path):
    recipient,public=generate_recipient_keypair(); signer,_=generate_signing_keypair()
    vault=SecureVault(tmp_path/"vault.db",public,recipient,signer)
    object_id=vault.import_document("report.txt",b"synthetic benchmark document")
    assert vault.retrieve_document(object_id)==("report.txt",b"synthetic benchmark document")

def test_tampered_ciphertext_is_rejected():
    nonce,ciphertext=encrypt_blob(b"payload",b"k"*32,object_id="obj")
    with pytest.raises(VaultCryptoError): decrypt_blob(nonce,ciphertext[:-1]+bytes([ciphertext[-1]^1]),b"k"*32,object_id="obj")

def test_aad_prevents_object_id_swap():
    nonce,ciphertext=encrypt_blob(b"payload",b"k"*32,object_id="one")
    with pytest.raises(VaultCryptoError): decrypt_blob(nonce,ciphertext,b"k"*32,object_id="two")

def test_wrapped_key_round_trip_and_bad_size():
    private,public=generate_recipient_keypair(); wrapped=wrap_data_key(b"d"*32,public)
    assert unwrap_data_key(wrapped,private)==b"d"*32
    with pytest.raises(VaultCryptoError): wrap_data_key(b"short",public)

def test_manifest_signatures_reject_tampering():
    private,public=generate_signing_keypair(); sig=sign_manifest(b"manifest",private)
    assert verify_manifest(b"manifest",sig,public)
    assert not verify_manifest(b"other",sig,public)

def test_public_key_serialization_round_trip():
    _,public=generate_recipient_keypair()
    loaded=load_public_key(serialize_public_key(public))
    assert loaded.public_numbers()==public.public_numbers()

def test_filename_and_size_validation(tmp_path):
    private,public=generate_recipient_keypair(); vault=SecureVault(tmp_path/"vault.db",public,private,config=VaultConfig(3))
    with pytest.raises(ValueError): vault.import_document("../secret",b"x")
    with pytest.raises(ValueError): vault.import_document("large",b"four")

def test_delete_is_idempotent(tmp_path):
    private,public=generate_recipient_keypair(); vault=SecureVault(tmp_path/"vault.db",public,private)
    key=vault.import_document("a.txt",b"a")
    assert vault.remove_document(key)
    assert not vault.remove_document(key)


def test_wrapped_key_rejects_wrong_recipient():
    _,public=generate_recipient_keypair(); wrong,_=generate_recipient_keypair()
    wrapped=wrap_data_key(b"d"*32,public)
    with pytest.raises(VaultCryptoError): unwrap_data_key(wrapped,wrong)

def test_manifest_rejects_wrong_public_key():
    private,_=generate_signing_keypair(); _,wrong=generate_signing_keypair()
    signature=sign_manifest(b"manifest",private)
    assert not verify_manifest(b"manifest",signature,wrong)
