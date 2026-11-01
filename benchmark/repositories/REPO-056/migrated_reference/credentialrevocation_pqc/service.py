"""Credential revocation log and signed, freshness-checked verifier feeds."""
import sqlite3,json
from pathlib import Path
from .crypto import canonical_feed,sign_feed,verify_feed,export_publisher_key,load_publisher_key
class CredentialRevocation:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS credentials(credential_id TEXT PRIMARY KEY,status TEXT NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS revocations(credential_id TEXT PRIMARY KEY,revoked_at INTEGER NOT NULL,reason TEXT NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS publisher_keys(key_version INTEGER PRIMARY KEY,verify_key BLOB NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS feeds(feed_id TEXT NOT NULL,sequence INTEGER NOT NULL,issued_at INTEGER NOT NULL,expires_at INTEGER NOT NULL,record BLOB NOT NULL,signature BLOB NOT NULL,key_version INTEGER NOT NULL,PRIMARY KEY(feed_id,sequence))")
   db.execute("CREATE TABLE IF NOT EXISTS verifier_revocations(verifier_id TEXT NOT NULL,credential_id TEXT NOT NULL,PRIMARY KEY(verifier_id,credential_id))")
   db.execute("CREATE TABLE IF NOT EXISTS verifier_state(verifier_id TEXT PRIMARY KEY,feed_id TEXT NOT NULL,sequence INTEGER NOT NULL,updated_at INTEGER NOT NULL)")
 def register_credential(self,credential_id):
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO credentials VALUES(?,'active')",(credential_id,))
 def revoke_credential(self,credential_id,revoked_at,reason):
  if not reason:raise ValueError('reason required')
  with sqlite3.connect(self.path) as db:
   c=db.execute("UPDATE credentials SET status='revoked' WHERE credential_id=? AND status='active'",(credential_id,))
   if c.rowcount!=1:return False
   db.execute("INSERT INTO revocations VALUES(?,?,?)",(credential_id,revoked_at,reason));return True
 def rotate_publisher_key(self,private,public):
  with sqlite3.connect(self.path) as db:
   v=(db.execute("SELECT MAX(key_version) FROM publisher_keys").fetchone()[0] or 0)+1;db.execute("INSERT INTO publisher_keys VALUES(?,?)",(v,export_publisher_key(public)));return v
 def publish_feed(self,feed_id,sequence,issued_at,expires_at,private):
  with sqlite3.connect(self.path) as db:
   key=db.execute("SELECT key_version FROM publisher_keys ORDER BY key_version DESC LIMIT 1").fetchone()
   if key is None:raise ValueError('publisher key not configured')
   revoked=[r[0] for r in db.execute("SELECT credential_id FROM revocations ORDER BY credential_id").fetchall()];record=canonical_feed(feed_id,sequence,issued_at,expires_at,revoked);sig=sign_feed(record,private);pub=db.execute("SELECT verify_key FROM publisher_keys WHERE key_version=?",(key[0],)).fetchone()[0]
   if not verify_feed(record,sig,load_publisher_key(pub)):raise PermissionError('feed signer does not match active publisher key')
   db.execute("INSERT INTO feeds VALUES(?,?,?,?,?,?,?)",(feed_id,sequence,issued_at,expires_at,record,sig,key[0]));return record,sig,key[0]
 def apply_feed(self,verifier_id,feed_id,sequence,now):
  with sqlite3.connect(self.path) as db:
   f=db.execute("SELECT issued_at,expires_at,record,signature,key_version FROM feeds WHERE feed_id=? AND sequence=?",(feed_id,sequence)).fetchone();state=db.execute("SELECT feed_id,sequence FROM verifier_state WHERE verifier_id=?",(verifier_id,)).fetchone();k=db.execute("SELECT verify_key FROM publisher_keys WHERE key_version=?",(f[4],)).fetchone() if f else None
   if f is None or k is None:return False
   if not (f[0]<=now<f[1]) or (state and state[0]==feed_id and sequence<=state[1]):return False
   if state:
    prior=db.execute("SELECT issued_at FROM feeds WHERE feed_id=? AND sequence=?",(state[0],state[1])).fetchone()
    if prior and f[0]<=prior[0]:return False
   body=json.loads(f[2])
   if canonical_feed(feed_id,sequence,f[0],f[1],body.get('revoked_ids',[]))!=f[2] or not verify_feed(f[2],f[3],load_publisher_key(k[0])):return False
   db.execute("INSERT INTO verifier_state VALUES(?,?,?,?) ON CONFLICT(verifier_id) DO UPDATE SET feed_id=excluded.feed_id,sequence=excluded.sequence,updated_at=excluded.updated_at",(verifier_id,feed_id,sequence,now));db.execute("DELETE FROM verifier_revocations WHERE verifier_id=?",(verifier_id,));db.executemany("INSERT INTO verifier_revocations VALUES(?,?)",[(verifier_id,x) for x in body['revoked_ids']]);return True
 def is_revoked(self,credential_id,verifier_id=None):
  table="revocations" if verifier_id is None else "verifier_revocations"
  with sqlite3.connect(self.path) as db:
   if verifier_id is None:return db.execute("SELECT 1 FROM revocations WHERE credential_id=?",(credential_id,)).fetchone() is not None
   return db.execute("SELECT 1 FROM verifier_revocations WHERE verifier_id=? AND credential_id=?",(verifier_id,credential_id)).fetchone() is not None
 def revocation_history(self):
  with sqlite3.connect(self.path) as db:return db.execute("SELECT credential_id,revoked_at,reason FROM revocations ORDER BY revoked_at,credential_id").fetchall()
