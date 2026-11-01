import sqlite3
from sharedfolderaccessgrant_pqc.crypto import export_public_key, generate_signer, load_public_key
from sharedfolderaccessgrant_pqc.service import SharedFolderAccessGrantPQC

def sample():
    return {'grant_id': 'test-id', 'workspace_id': 'demo', 'folder_id': 'demo', 'subject': 'alice', 'permission': 'read', 'expires_at': 1800000000}

def test_issue_verify_and_deactivate(tmp_path):
    key=generate_signer(); store=SharedFolderAccessGrantPQC(tmp_path/'records.db'); claims=sample(); store.issue(claims,key)
    assert store.verify(claims['grant_id'],key.public_key())
    assert not store.verify(claims['grant_id'],key.public_key(),expected={'workspace_id':'other'})
    assert store.deactivate(claims['grant_id']) and not store.verify(claims['grant_id'],key.public_key())

def test_domain_validation(tmp_path):
    import pytest
    key=generate_signer(); store=SharedFolderAccessGrantPQC(tmp_path/'invalid.db')
    with pytest.raises(ValueError):
        invalid=sample(); invalid.pop(next(iter(invalid))); store.issue(invalid,key)



def test_wrong_signer_and_persisted_mutation_rejected(tmp_path):
    key=generate_signer(); wrong=generate_signer(); store=SharedFolderAccessGrantPQC(tmp_path/'tamper.db'); claims=sample(); store.issue(claims,key)
    assert not store.verify(claims[next(iter(claims))],wrong.public_key())
    with sqlite3.connect(store.path) as db: db.execute("UPDATE records SET payload=?",(b'[]',))
    assert not store.verify(claims[next(iter(claims))],key.public_key())

def test_public_key_serialization_roundtrip(tmp_path):
    key=generate_signer(); store=SharedFolderAccessGrantPQC(tmp_path/'serialized.db'); claims=sample(); store.issue(claims,key)
    assert store.verify(claims[next(iter(claims))],load_public_key(export_public_key(key)))

def test_record_identifier_is_bound_to_signed_claim(tmp_path):
    key=generate_signer(); store=SharedFolderAccessGrantPQC(tmp_path/'record-id.db'); claims=sample(); store.issue(claims,key)
    with sqlite3.connect(store.path) as db: db.execute("UPDATE records SET record_id=?",('different-row-id',))
    assert not store.verify('different-row-id',key.public_key())

def test_malformed_public_key_rejected():
    import pytest
    with pytest.raises(ValueError): load_public_key(b'bad-key')
