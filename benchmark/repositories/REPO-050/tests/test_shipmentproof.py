import sqlite3
import pytest
from shipmentproof.crypto import generate_signer
from shipmentproof.ledger import ShipmentLedger


def test_custody_sequence_and_authorization(tmp_path):
    depot,depot_pub=generate_signer(); carrier,carrier_pub=generate_signer(); ledger=ShipmentLedger(tmp_path/"shipments.db"); ledger.register_shipment("BOX-9","depot")
    assert ledger.transfer_custody("BOX-9","depot","carrier","dock",depot,at=100)==1
    with pytest.raises(PermissionError): ledger.transfer_custody("BOX-9","depot","store","door",depot,at=101)
    assert ledger.transfer_custody("BOX-9","carrier","store","door",carrier,at=102)==2
    assert ledger.verify_chain("BOX-9",{"depot":depot_pub,"carrier":carrier_pub}) and len(ledger.history("BOX-9"))==2


def test_handoff_payload_tampering_breaks_chain(tmp_path):
    private,public=generate_signer(); db=tmp_path/"tamper.db"; ledger=ShipmentLedger(db); ledger.register_shipment("B","A"); ledger.transfer_custody("B","A","C","dock",private,at=100)
    with sqlite3.connect(db) as conn: conn.execute("UPDATE handoffs SET location='other' WHERE shipment='B'")
    assert not ledger.verify_chain("B",{"A":public})


def test_empty_shipment_rejected(tmp_path):
    ledger=ShipmentLedger(tmp_path/"empty.db")
    with pytest.raises(ValueError): ledger.register_shipment("", "holder")
