import pytest
from distributedcache_pqc.crypto import decapsulate_session,encapsulate_session,generate_node_keypair,generate_signer
from distributedcache_pqc.service import CacheClusterPQC


def test_mlkem_session_keys_match_and_snapshot_roundtrip(tmp_path):
    src,src_pub=generate_node_keypair(); dst,dst_pub=generate_node_keypair(); ct,key=encapsulate_session(dst_pub,"src","dst"); assert key==decapsulate_session(dst,ct,"src","dst")
    signer=generate_signer(); cluster=CacheClusterPQC(tmp_path/"cache.db"); cluster.register_node("src",src_pub,signer.public_key()); cluster.register_node("dst",dst_pub,signer.public_key())
    cluster.store_snapshot("snap-1","src","dst",1,b"synthetic cache",src,signer); assert cluster.read_snapshot("snap-1",dst)==b"synthetic cache"


def test_wrong_context_and_revoked_node_rejected(tmp_path):
    src,sp=generate_node_keypair(); dst,dp=generate_node_keypair(); signer=generate_signer(); cluster=CacheClusterPQC(tmp_path/"nodes.db"); cluster.register_node("s",sp,signer.public_key()); cluster.register_node("d",dp,signer.public_key()); cluster.store_snapshot("s1","s","d",1,b"v",src,signer)
    assert cluster.revoke_node("d")
    with pytest.raises(PermissionError): cluster.read_snapshot("s1",dst)
    ct,key=encapsulate_session(dp,"s","d")
    assert decapsulate_session(dst,ct,"s","other") != key


def test_snapshot_signature_tamper_rejected():
    from distributedcache_pqc.crypto import seal_snapshot,open_snapshot
    signer=generate_signer(); envelope=seal_snapshot("x","a","b",1,b"data",b"k"*32,signer,b"enc")
    with pytest.raises(ValueError): open_snapshot(envelope,b"k"*32,generate_signer().public_key())
