import pytest
from tenderproof.crypto import generate_bidder_signer,generate_evaluator_keypair
from tenderproof.service import TenderProof
def test_confidential_bid_and_audit(tmp_path):
 sk,pk=generate_bidder_signer();ek,ep=generate_evaluator_keypair();t=TenderProof(tmp_path/'t.db');t.create_tender('T',100,ep);t.register_bidder('T','vendor',pk);t.submit_bid('T','vendor','B1',25000,b'proposal',90,sk);assert t.open_bid('B1','reviewer',ek,now=101)==b'proposal';assert t.audit_history('B1')==[('reviewer',101)]
def test_deadline_wrong_signer_and_missing_bid(tmp_path):
 sk,pk=generate_bidder_signer();other,_=generate_bidder_signer();ek,ep=generate_evaluator_keypair();t=TenderProof(tmp_path/'t.db');t.create_tender('T',10,ep);t.register_bidder('T','v',pk)
 with pytest.raises(ValueError):t.submit_bid('T','v','late',1,b'p',11,sk)
 with pytest.raises(PermissionError):t.submit_bid('T','v','wrong',1,b'p',9,other)
 with pytest.raises(KeyError):t.open_bid('missing','r',ek,now=12)
