import pytest,sqlite3
from capabilitygate.crypto import generate_issuer,export_issuer,load_issuer
from capabilitygate.service import CapabilityGate
def test_issue_authorize_expiry_and_revoke(tmp_path):
 sk,pk=generate_issuer();g=CapabilityGate(tmp_path/'g.db');g.issue('t1','user-1','/reports','read',100,sk);assert g.authorize('t1','user-1','/reports','read',pk,now=50);assert not g.authorize('t1','user-1','/reports','read',pk,now=100);assert g.revoke('t1');assert not g.authorize('t1','user-1','/reports','read',pk,now=60)
def test_scope_principal_and_wrong_issuer(tmp_path):
 sk,pk=generate_issuer();_,wrong=generate_issuer();g=CapabilityGate(tmp_path/'g.db');g.issue('t','u','/x','write',90,sk);assert not g.authorize('t','u','/x','read',pk,now=1);assert not g.authorize('t','other','/x','write',pk,now=1);assert not g.authorize('t','u','/x','write',wrong,now=1)
def test_token_id_unique_and_key_roundtrip(tmp_path):
 sk,pk=generate_issuer();g=CapabilityGate(tmp_path/'g.db');g.issue('t','u','/x','read',10,sk)
 with pytest.raises(sqlite3.IntegrityError):g.issue('t','u','/x','read',20,sk)
 assert load_issuer(export_issuer(pk)) is not None
