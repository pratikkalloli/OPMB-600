import pytest
from inventoryhandoff_pqc.crypto import generate_actor
from inventoryhandoff_pqc.service import InventoryHandoff
def test_item_transfer_chain_and_history(tmp_path):
 a=generate_actor();b=generate_actor();h=InventoryHandoff(tmp_path/'i.db');h.register_actor('a',a.public_key());h.register_actor('b',b.public_key());h.register_item('item-1','batch-4','a');assert h.transfer_item('item-1','a','b',1,10,a);assert h.verify_chain('item-1');assert h.custody_history('item-1')==[(1,10,'a','b')]
def test_wrong_sender_sequence_and_unknown_item(tmp_path):
 a=generate_actor();b=generate_actor();h=InventoryHandoff(tmp_path/'i.db');h.register_actor('a',a.public_key());h.register_actor('b',b.public_key());h.register_item('i','batch','a')
 with pytest.raises(PermissionError):h.transfer_item('i','a','b',1,1,b)
 with pytest.raises(ValueError):h.transfer_item('i','a','b',2,1,a)
 with pytest.raises(KeyError):h.transfer_item('missing','a','b',1,1,a)
