import pytest
from careconsent_pqc.crypto import generate_authority,export_authority,load_authority
from careconsent_pqc.service import CareConsent
def test_grant_authorization_expiry_and_revocation(tmp_path):
 sk=generate_authority();pk=sk.public_key();app=CareConsent(tmp_path/'c.db');app.grant('c1','patient-a','study-7','analysis,followup',500,2,sk);assert app.authorize('c1','patient-a','study-7','analysis',pk,now=100);assert not app.authorize('c1','patient-a','study-7','analysis',pk,now=600);assert app.revoke('c1','withdrawn',now=200);assert not app.authorize('c1','patient-a','study-7','analysis',pk,now=250)
def test_subject_study_scope_and_expiry_binding(tmp_path):
 sk=generate_authority();pk=sk.public_key();app=CareConsent(tmp_path/'c.db');app.grant('c2','p','s','read',900,1,sk);assert not app.authorize('c2','other','s','read',pk,now=1);assert not app.authorize('c2','p','s','write',pk,now=1);assert app.revision('c2')==1
def test_bad_record_and_key_serialization(tmp_path):
 sk=generate_authority();app=CareConsent(tmp_path/'c.db')
 with pytest.raises(ValueError):app.grant('x','p','s','r',0,1,sk)
 app.grant('x','p','s','r',900,1,sk);assert app.revoke('x','withdrawn',now=1);assert not app.revoke('x','again',now=2);assert load_authority(export_authority(sk.public_key())) is not None
