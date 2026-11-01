"""Persistent node registry and ML-KEM-protected cache snapshots."""
import sqlite3
from pathlib import Path
from .crypto import decapsulate_session,encapsulate_session,export_node_key,export_signer_key,load_node_key,load_signer_key,open_snapshot,seal_snapshot,SnapshotEnvelope


class CacheClusterPQC:
    def __init__(self,path:str|Path):
        self.path=str(path)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS nodes(node_id TEXT PRIMARY KEY,exchange_key BLOB NOT NULL,verify_key BLOB NOT NULL,status TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS snapshots(snapshot_id TEXT PRIMARY KEY,source TEXT NOT NULL,target TEXT NOT NULL,version INTEGER NOT NULL,encapsulation BLOB NOT NULL,nonce BLOB NOT NULL,ciphertext BLOB NOT NULL,signature BLOB NOT NULL)")
    def register_node(self,node_id,exchange_public,verify_public):
        if not node_id: raise ValueError("node ID required")
        with sqlite3.connect(self.path) as db: db.execute("INSERT INTO nodes VALUES(?,?,?,'active')",(node_id,export_node_key(exchange_public),export_signer_key(verify_public)))
    def revoke_node(self,node_id):
        with sqlite3.connect(self.path) as db: return db.execute("UPDATE nodes SET status='revoked' WHERE node_id=? AND status='active'",(node_id,)).rowcount==1
    def store_snapshot(self,snapshot_id,source,target,version,payload,source_private,signing_private):
        with sqlite3.connect(self.path) as db: rows=db.execute("SELECT node_id,exchange_key,status FROM nodes WHERE node_id IN (?,?)",(source,target)).fetchall()
        nodes={r[0]:r[1:] for r in rows}
        if source not in nodes or target not in nodes or nodes[source][1]!='active' or nodes[target][1]!='active': raise PermissionError("both cache nodes must be registered and active")
        encapsulation,key=encapsulate_session(load_node_key(nodes[target][0]),source,target); env=seal_snapshot(snapshot_id,source,target,version,payload,key,signing_private,encapsulation)
        with sqlite3.connect(self.path) as db: db.execute("INSERT INTO snapshots VALUES(?,?,?,?,?,?,?,?)",(snapshot_id,source,target,version,encapsulation,env.nonce,env.ciphertext,env.signature))
    def read_snapshot(self,snapshot_id,target_private):
        with sqlite3.connect(self.path) as db:
            row=db.execute("SELECT source,target,version,encapsulation,nonce,ciphertext,signature FROM snapshots WHERE snapshot_id=?",(snapshot_id,)).fetchone()
            if row is None: raise KeyError("snapshot not found")
            source,target,version,encapsulation,nonce,ciphertext,signature=row; nodes={r[0]:r[1:] for r in db.execute("SELECT node_id,exchange_key,verify_key,status FROM nodes WHERE node_id IN (?,?)",(source,target)).fetchall()}
        if source not in nodes or target not in nodes or nodes[source][2]!='active' or nodes[target][2]!='active': raise PermissionError("snapshot node revoked")
        key=decapsulate_session(target_private,encapsulation,source,target); signer=load_signer_key(nodes[source][1])
        return open_snapshot(SnapshotEnvelope(snapshot_id,source,target,version,encapsulation,nonce,ciphertext,signature),key,signer)
