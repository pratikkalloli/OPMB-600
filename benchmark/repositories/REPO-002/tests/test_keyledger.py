import pytest
from keyledger.crypto import *
from keyledger.ledger import KeyLedger
def test_key_lifecycle_and_signed_audit(tmp_path):
 audit,audit_pub=generate_signing_keypair(); transport,public=generate_transport_keypair(); ledger=KeyLedger(tmp_path/"keys.db",audit,audit_pub)
 key_id=ledger.register("service-a","data wrapping",public); assert ledger.audit_valid(key_id)
 replacement,replacement_pub=generate_transport_keypair(); new_id=ledger.rotate(key_id,replacement_pub); assert ledger.audit_valid(new_id)
 assert ledger.revoke(new_id); assert not ledger.revoke(new_id)
def test_audit_signature_rejects_mutation():
 private,public=generate_signing_keypair(); sig=sign_audit_event(b"created",private); assert verify_audit_event(b"created",sig,public); assert not verify_audit_event(b"revoked",sig,public)
def test_encrypted_private_key_storage_round_trip():
 private,_=generate_signing_keypair(); encoded=serialize_private_key(private,b"benchmark-only-passphrase"); restored=load_private_key(encoded,b"benchmark-only-passphrase"); assert restored.key_size==3072
def test_key_transport_recovery():
 private,public=generate_transport_keypair(); wrapped=wrap_recovery_secret(b"synthetic recovery value",public); assert unwrap_recovery_secret(wrapped,private)==b"synthetic recovery value"
def test_public_serialization_and_fingerprint():
 _,public=generate_transport_keypair(); restored=load_public_key(serialize_public_key(public)); assert public_key_fingerprint(public)==public_key_fingerprint(restored)


def test_rsa_oaep_recovery_limit_and_rejection():
 private,public=generate_transport_keypair(); secret=b"s"*318
 assert unwrap_recovery_secret(wrap_recovery_secret(secret,public),private)==secret
 with pytest.raises(ValueError): wrap_recovery_secret(b"s"*319,public)

def test_expired_key_metadata_rejected(tmp_path):
 import time
 audit,audit_public=generate_signing_keypair(); _,public=generate_transport_keypair(); ledger=KeyLedger(tmp_path/"expired.db",audit,audit_public)
 with pytest.raises(ValueError): ledger.register("service","transport",public,expires=int(time.time())-1)
