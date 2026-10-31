import pytest
from keyledger_pqc.crypto import serialize_private_key,load_private_key,generate_signing_keypair,sign_audit_event,verify_audit_event
from keyledger_pqc.ledger import KeyLedger
from keyledger_pqc.crypto import generate_transport_keypair,wrap_recovery_secret,unwrap_recovery_secret,serialize_public_key,load_public_key,public_key_fingerprint
def test_kem_recovery_secret_wrong_context_rejected():
 private,public=generate_transport_keypair(); env=wrap_recovery_secret(b"seed",public,key_id="key-1"); assert unwrap_recovery_secret(env,private,key_id="key-1")==b"seed"
 with pytest.raises(ValueError): unwrap_recovery_secret(env,private,key_id="key-2")
def test_mldsa_audit_signature_rejects_modified_event():
 private,public=generate_signing_keypair(); sig=sign_audit_event(b"created",private); assert verify_audit_event(b"created",sig,public); assert not verify_audit_event(b"deleted",sig,public)
def test_mlkem_public_serialization_round_trip():
 _,public=generate_transport_keypair(); loaded=load_public_key(serialize_public_key(public)); assert public_key_fingerprint(public)==public_key_fingerprint(loaded)


def test_encrypted_mlkem_private_key_serialization(tmp_path):
 from keyledger_pqc.crypto import generate_transport_keypair
 private,_=generate_transport_keypair(); data=serialize_private_key(private,b"synthetic-passphrase")
 restored=load_private_key(data,b"synthetic-passphrase"); assert restored.public_key().public_bytes_raw()==private.public_key().public_bytes_raw()

def test_pqc_lifecycle_audit_and_rotation(tmp_path):
 audit,audit_public=generate_signing_keypair(); current,current_public=generate_transport_keypair(); ledger=KeyLedger(tmp_path/"ledger.db",audit,audit_public)
 old=ledger.register("edge-service","session key establishment",current_public); assert ledger.audit_valid(old)
 newer,new_public=generate_transport_keypair(); replacement=ledger.rotate(old,new_public); assert ledger.audit_valid(old) and ledger.audit_valid(replacement)
 assert any(row[3]=="ML-KEM-768" for row in ledger.inventory())
