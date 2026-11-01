import pytest, sqlite3
from securemailbox_pqc.crypto import generate_sender,generate_recipient
from securemailbox_pqc.service import SecureMailbox
def test_send_receive_and_authentication(tmp_path):
 ask=generate_sender();ap=ask.public_key();bsk=generate_sender();bpk=bsk.public_key();rsk,rpk=generate_recipient();app=SecureMailbox(tmp_path/'m.db');app.register_user('alice',generate_recipient()[1],ap);app.register_user('bob',rpk,bpk);app.send('m1','alice','bob',1,b'hello',ask);assert app.receive('m1','bob',rsk)==b'hello'
def test_recipient_and_activity_checks(tmp_path):
 a=generate_sender();r,rp=generate_recipient();app=SecureMailbox(tmp_path/'m.db');app.register_user('a',generate_recipient()[1],a.public_key());app.register_user('b',rp,generate_sender().public_key());app.send('m','a','b',1,b'x',a)
 with pytest.raises(PermissionError):app.receive('m','a',generate_recipient()[0])
 assert app.deactivate_user('b')
 with pytest.raises(PermissionError):app.receive('m','b',r)
def test_message_fields_and_unique_id(tmp_path):
 a=generate_sender();r,rp=generate_recipient();app=SecureMailbox(tmp_path/'m.db');app.register_user('a',generate_recipient()[1],a.public_key());app.register_user('b',rp,generate_sender().public_key());app.send('m','a','b',1,b'x',a)
 with pytest.raises(sqlite3.IntegrityError):app.send('m','a','b',1,b'y',a)
