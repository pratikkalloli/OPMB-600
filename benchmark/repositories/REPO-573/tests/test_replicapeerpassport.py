import sqlite3
from replicapeerpassport.crypto import export_public_key, generate_signer, load_public_key
from replicapeerpassport.service import ReplicaPeerPassport

def sample():
    return {'passport_id': 'test-id', 'cluster_id': 'cluster-a', 'region': 'ap-south-1', 'endpoint': 'https://peer.example', 'peer_digest': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'expires_at': 1800000000}

def test_issue_verify_and_deactivate(tmp_path):
    key=generate_signer(); store=ReplicaPeerPassport(tmp_path/'records.db'); claims=sample(); store.issue(claims,key)
    assert store.verify(claims['passport_id'],key.public_key())
    assert not store.verify(claims['passport_id'],key.public_key(),expected={'cluster_id':'other'})
    assert store.deactivate(claims['passport_id']) and not store.verify(claims['passport_id'],key.public_key())

def test_domain_validation(tmp_path):
    import pytest
    key=generate_signer(); store=ReplicaPeerPassport(tmp_path/'invalid.db')
    with pytest.raises(ValueError):
        invalid=sample(); invalid.pop(next(iter(invalid))); store.issue(invalid,key)



def test_wrong_signer_and_persisted_mutation_rejected(tmp_path):
    key=generate_signer(); wrong=generate_signer(); store=ReplicaPeerPassport(tmp_path/'tamper.db'); claims=sample(); store.issue(claims,key)
    assert not store.verify(claims[next(iter(claims))],wrong.public_key())
    with sqlite3.connect(store.path) as db: db.execute("UPDATE records SET payload=?",(b'[]',))
    assert not store.verify(claims[next(iter(claims))],key.public_key())

def test_public_key_serialization_roundtrip(tmp_path):
    key=generate_signer(); store=ReplicaPeerPassport(tmp_path/'serialized.db'); claims=sample(); store.issue(claims,key)
    assert store.verify(claims[next(iter(claims))],load_public_key(export_public_key(key)))

def test_record_identifier_is_bound_to_signed_claim(tmp_path):
    key=generate_signer(); store=ReplicaPeerPassport(tmp_path/'record-id.db'); claims=sample(); store.issue(claims,key)
    with sqlite3.connect(store.path) as db: db.execute("UPDATE records SET record_id=?",('different-row-id',))
    assert not store.verify('different-row-id',key.public_key())
