import pytest
from clearingdesk_pqc.crypto import generate_approver,generate_desk_keypair,seal_transfer,open_transfer,export_approver,load_approver
from clearingdesk_pqc.service import ClearingDesk
def test_two_person_payment_settlement(tmp_path):
 a=generate_approver(); b=generate_approver(); app=ClearingDesk(tmp_path/'pay.db'); app.create_instruction('T1',1250,'usd','merchant-4'); app.approve_instruction('T1','alice',a)
 with pytest.raises(PermissionError): app.settle_instruction('T1',{'alice':a.public_key(),'bob':b.public_key()})
 app.approve_instruction('T1','bob',b); assert app.settle_instruction('T1',{'alice':a.public_key(),'bob':b.public_key()}); assert app.status('T1')=='settled'
def test_duplicate_approver_cannot_satisfy_quorum(tmp_path):
 a=generate_approver(); app=ClearingDesk(tmp_path/'pay.db'); app.create_instruction('T2',20,'EUR','m'); app.approve_instruction('T2','alice',a)
 with pytest.raises(PermissionError): app.settle_instruction('T2',{'alice':a.public_key()})
def test_transfer_and_key_serialization():
 sk,pk=generate_desk_keypair(); envelope=seal_transfer(b'batch',pk); assert open_transfer(envelope,sk)==b'batch'; a=generate_approver(); assert load_approver(export_approver(a.public_key())) is not None

def test_same_signing_key_cannot_be_aliased_as_two_approvers(tmp_path):
 a=generate_approver(); ap=a.public_key(); app=ClearingDesk(tmp_path/'pay.db'); app.create_instruction('T3',99,'USD','merchant'); app.approve_instruction('T3','alice',a); app.approve_instruction('T3','mallory',a)
 with pytest.raises(PermissionError): app.settle_instruction('T3',{'alice':ap,'mallory':ap})
