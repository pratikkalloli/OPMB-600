from encryptednotebook_pqc.crypto import generate_signer,generate_owner_keypair
from encryptednotebook_pqc.service import EncryptedNotebook
def test_version_history_restore_and_rotation(tmp_path):
 sig=generate_signer();k1,p1=generate_owner_keypair();nb=EncryptedNotebook(tmp_path/'n.db');nb.create_notebook('alice',p1,sig.public_key());nb.write_note('n1','alice',1,b'first',sig);nb.write_note('n1','alice',2,b'second',sig);assert nb.read_version('n1','alice',1,k1)==b'first';assert nb.restore_version('n1','alice',2,k1)==b'second';k2,p2=generate_owner_keypair();assert nb.rotate_key('alice',p2)==2;nb.write_note('n1','alice',3,b'third',sig);assert nb.read_version('n1','alice',3,k2)==b'third';assert nb.versions('n1','alice')==[1,2,3]
def test_access_version_order_and_missing_note(tmp_path):
 sig=generate_signer();k,p=generate_owner_keypair();nb=EncryptedNotebook(tmp_path/'n.db');nb.create_notebook('a',p,sig.public_key());wrong=generate_signer()
 try:nb.write_note('x','a',1,b'bad',wrong);assert False
 except PermissionError:pass
 try:nb.read_version('x','a',1,k);assert False
 except KeyError:pass
 try:nb.write_note('x','a',2,b'bad',sig);assert False
 except ValueError:pass
