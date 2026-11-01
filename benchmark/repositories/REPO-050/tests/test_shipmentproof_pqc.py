import pytest
from shipmentproof_pqc.crypto import canonical_handoff,export_public_key,generate_signer,load_public_key,sign_handoff,verify_handoff
from shipmentproof_pqc.ledger import ShipmentLedgerPQC


def test_mldsa_hash_linked_handoffs_and_wrong_key(tmp_path):
    private=generate_signer(); other=generate_signer(); ledger=ShipmentLedgerPQC(tmp_path/"pqc.db"); ledger.register_shipment("SIM-1","warehouse")
    ledger.transfer_custody("SIM-1","warehouse","driver","gate",private,at=50)
    ledger.transfer_custody("SIM-1","driver","recipient","front desk",other,at=60)
    assert ledger.verify_chain("SIM-1",{"warehouse":private.public_key(),"driver":other.public_key()})
    assert not ledger.verify_chain("SIM-1",{"warehouse":private.public_key(),"driver":private.public_key()})


def test_modified_handoff_signature_rejected():
    private=generate_signer(); payload=canonical_handoff("x",1,"a","b","dock",50,"0"*64); signature=sign_handoff(payload,private)
    assert verify_handoff(payload,signature,private.public_key()); assert not verify_handoff(payload+b"!",signature,private.public_key())


def test_mldsa_key_encoding_and_bad_fields():
    private=generate_signer(); public=load_public_key(export_public_key(private.public_key())); assert verify_handoff(b"x",sign_handoff(b"x",private),public)
    with pytest.raises(ValueError): canonical_handoff("",1,"a","b","dock",1,"")
