import pytest
from distributedcache.crypto import derive_session_key,generate_node_keypair,generate_signer
from distributedcache.service import CacheCluster


def test_x25519_session_and_encrypted_snapshot_roundtrip(tmp_path):
    src,src_pub=generate_node_keypair(); dst,dst_pub=generate_node_keypair(); assert derive_session_key(src,dst_pub,"src","dst")==derive_session_key(dst,src_pub,"src","dst")
    signer,signer_pub=generate_signer(); cluster=CacheCluster(tmp_path/"cache.db"); cluster.register_node("src",src_pub,signer_pub); cluster.register_node("dst",dst_pub,signer_pub)
    cluster.store_snapshot("snap-1","src","dst",1,b"synthetic cache",src,signer)
    assert cluster.read_snapshot("snap-1",dst)==b"synthetic cache"


def test_revoked_node_and_unknown_snapshot_rejected(tmp_path):
    src,sp=generate_node_keypair(); dst,dp=generate_node_keypair(); signer,pub=generate_signer(); c=CacheCluster(tmp_path/"nodes.db"); c.register_node("s",sp,pub); c.register_node("d",dp,pub); c.store_snapshot("s1","s","d",1,b"v",src,signer)
    assert c.revoke_node("d")
    with pytest.raises(PermissionError): c.read_snapshot("s1",dst)
    with pytest.raises(KeyError): c.read_snapshot("missing",dst)


def test_bad_node_pair_rejected():
    private,public=generate_node_keypair()
    with pytest.raises(ValueError): derive_session_key(private,public,"same","same")
