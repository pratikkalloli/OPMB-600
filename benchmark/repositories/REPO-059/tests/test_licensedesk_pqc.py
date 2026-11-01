import pytest
from licensedesk_pqc.crypto import generate_authority,export_authority,load_authority
from licensedesk_pqc.service import LicenseDesk
def test_issue_offline_validate_and_revoke(tmp_path):
 sk=generate_authority();pk=sk.public_key();d=LicenseDesk(tmp_path/'l.db');d.issue('l1','editor','install-a',['export','review'],10,100,sk);assert d.verify_offline('l1','editor','install-a','export',pk,now=50);assert not d.verify_offline('l1','editor','install-a','export',pk,now=100);assert d.revoke('l1','customer request',now=60);assert 'l1' in d.revocation_snapshot();assert not d.verify_offline('l1','editor','install-a','export',pk,now=70)
def test_wrong_installation_product_or_feature(tmp_path):
 sk=generate_authority();pk=sk.public_key();d=LicenseDesk(tmp_path/'l.db');d.issue('l','editor','device-1',['review'],1,100,sk);assert not d.verify_offline('l','editor','device-2','review',pk,now=5);assert not d.verify_offline('l','other','device-1','review',pk,now=5);assert not d.verify_offline('l','editor','device-1','export',pk,now=5)
def test_invalid_license_and_key_serialization(tmp_path):
 sk=generate_authority();d=LicenseDesk(tmp_path/'l.db')
 with pytest.raises(ValueError):d.issue('x','p','i',['f'],10,10,sk)
 assert load_authority(export_authority(sk.public_key())) is not None
