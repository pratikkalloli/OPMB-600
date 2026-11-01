"""Persistent cache nodes and encrypted snapshot exchange."""
import sqlite3
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from .crypto import derive_session_key,export_node_key,load_node_key,open_snapshot,seal_snapshot


class CacheCluster:
    def __init__(self,path:str|Path):
        self.path=str(path)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS nodes(node_id TEXT PRIMARY KEY,exchange_key BLOB NOT NULL,verify_key BLOB NOT NULL,status TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS snapshots(snapshot_id TEXT PRIMARY KEY,source TEXT NOT NULL,target TEXT NOT NULL,version INTEGER NOT NULL,nonce BLOB NOT NULL,ciphertext BLOB NOT NULL,signature BLOB NOT NULL)")
    def register_node(self,node_id,exchange_public,verify_public):
        if not node_id: raise ValueError("node ID required")
        with sqlite3.connect(self.path) as db: db.execute("INSERT INTO nodes VALUES(?,?,?,'active')",(node_id,export_node_key(exchange_public),verify_public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)))
    def revoke_node(self,node_id):
        with sqlite3.connect(self.path) as db: return db.execute("UPDATE nodes SET status='revoked' WHERE node_id=? AND status='active'",(node_id,)).rowcount==1
    def store_snapshot(self,snapshot_id,source,target,version,payload,source_private,signing_private):
        with sqlite3.connect(self.path) as db:
            rows=db.execute("SELECT node_id,exchange_key,status FROM nodes WHERE node_id IN (?,?)",(source,target)).fetchall()
        nodes={r[0]:r[1:] for r in rows}
        if source not in nodes or target not in nodes or nodes[source][1]!='active' or nodes[target][1]!='active': raise PermissionError("both cache nodes must be registered and active")
        key=derive_session_key(source_private,load_node_key(nodes[target][0]),source,target); env=seal_snapshot(snapshot_id,source,target,version,payload,key,signing_private)
        with sqlite3.connect(self.path) as db: db.execute("INSERT INTO snapshots VALUES(?,?,?,?,?,?,?)",(snapshot_id,source,target,version,env.nonce,env.ciphertext,env.signature))
    def read_snapshot(self,snapshot_id,target_private):
        with sqlite3.connect(self.path) as db:
            row=db.execute("SELECT source,target,version,nonce,ciphertext,signature FROM snapshots WHERE snapshot_id=?",(snapshot_id,)).fetchone()
            if row is None: raise KeyError("snapshot not found")
            source,target,version,nonce,ciphertext,signature=row; nodes={r[0]:r[1:] for r in db.execute("SELECT node_id,exchange_key,verify_key,status FROM nodes WHERE node_id IN (?,?)",(source,target)).fetchall()}
        if source not in nodes or target not in nodes or nodes[source][2]!='active' or nodes[target][2]!='active': raise PermissionError("snapshot node revoked")
        signer=serialization.load_pem_public_key(nodes[source][1]); key=derive_session_key(target_private,load_node_key(nodes[source][0]),source,target)
        from .crypto import SnapshotEnvelope
        return open_snapshot(SnapshotEnvelope(snapshot_id,source,target,version,nonce,ciphertext,signature),key,signer)
