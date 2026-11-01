import pytest
from clearingdesk.crypto import generate_approver,generate_desk_keypair,seal_transfer,open_transfer,export_approver,load_approver
from clearingdesk.service import ClearingDesk
def test_two_person_payment_settlement(tmp_path):
 a,ap=generate_approver(); b,bp=generate_approver(); app=ClearingDesk(tmp_path/'pay.db'); app.create_instruction('T1',1250,'usd','merchant-4'); app.approve_instruction('T1','alice',a)
 with pytest.raises(PermissionError): app.settle_instruction('T1',{'alice':ap,'bob':bp})
 app.approve_instruction('T1','bob',b); assert app.settle_instruction('T1',{'alice':ap,'bob':bp}); assert app.status('T1')=='settled'
def test_duplicate_approver_cannot_satisfy_quorum(tmp_path):
 a,ap=generate_approver(); app=ClearingDesk(tmp_path/'pay.db'); app.create_instruction('T2',20,'EUR','m'); app.approve_instruction('T2','alice',a)
 with pytest.raises(PermissionError): app.settle_instruction('T2',{'alice':ap})
def test_transfer_and_key_serialization():
 sk,pk=generate_desk_keypair(); envelope=seal_transfer(b'batch',pk); assert open_transfer(envelope,sk)==b'batch'; a,ap=generate_approver(); assert load_approver(export_approver(ap)) is not None

def test_same_signing_key_cannot_be_aliased_as_two_approvers(tmp_path):
 a,ap=generate_approver(); app=ClearingDesk(tmp_path/'pay.db'); app.create_instruction('T3',99,'USD','merchant'); app.approve_instruction('T3','alice',a); app.approve_instruction('T3','mallory',a)
 with pytest.raises(PermissionError): app.settle_instruction('T3',{'alice':ap,'mallory':ap})
