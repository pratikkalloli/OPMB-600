from credentialrevocation.crypto import generate_publisher_keypair
from credentialrevocation.service import CredentialRevocation
def test_publish_apply_fresh_feed_and_revoke(tmp_path):
 sk,pk=generate_publisher_keypair();c=CredentialRevocation(tmp_path/'c.db');c.register_credential('cred-1');c.rotate_publisher_key(sk,pk);c.revoke_credential('cred-1',10,'compromised');c.publish_feed('feed',1,20,100,sk);assert c.apply_feed('verifier','feed',1,30);assert c.is_revoked('cred-1');assert c.is_revoked('cred-1','verifier');assert c.revocation_history()==[('cred-1',10,'compromised')]
def test_stale_expired_and_rollback_feed_rejected(tmp_path):
 sk,pk=generate_publisher_keypair();c=CredentialRevocation(tmp_path/'c.db');c.rotate_publisher_key(sk,pk);c.publish_feed('fresh',1,20,40,sk);c.publish_feed('live',1,1,99,sk);assert not c.apply_feed('v','fresh',1,50);assert c.apply_feed('v','live',1,20);c.publish_feed('live',2,21,100,sk);assert c.apply_feed('v','live',2,30);assert not c.apply_feed('v','live',1,31);c.publish_feed('older',1,10,80,sk);c.publish_feed('newer',1,40,120,sk);assert c.apply_feed('other','newer',1,50);assert not c.apply_feed('other','older',1,51)

def test_key_rotation_keeps_old_feed_verifiable(tmp_path):
 sk,pk=generate_publisher_keypair();c=CredentialRevocation(tmp_path/'c.db');old=c.rotate_publisher_key(sk,pk);c.publish_feed('f',1,1,99,sk);sk2,pk2=generate_publisher_keypair();assert c.rotate_publisher_key(sk2,pk2)==old+1;assert c.apply_feed('v','f',1,5)
