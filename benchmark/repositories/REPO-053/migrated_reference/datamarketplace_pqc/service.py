"""Provider and dataset publication with encrypted access audit."""
import sqlite3
from pathlib import Path
from .crypto import canonical_manifest,sign_manifest,verify_manifest,seal_asset,open_asset,export_provider,load_provider,load_consumer
class DataMarketplace:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS providers(provider_id TEXT PRIMARY KEY,verify_key BLOB NOT NULL,status TEXT NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS assets(asset_id TEXT NOT NULL,version INTEGER NOT NULL,provider TEXT NOT NULL,metadata BLOB NOT NULL,encapsulation BLOB NOT NULL,nonce BLOB NOT NULL,ciphertext BLOB NOT NULL,manifest BLOB NOT NULL,signature BLOB NOT NULL,PRIMARY KEY(asset_id,version))")
   db.execute("CREATE TABLE IF NOT EXISTS access_audit(audit_id INTEGER PRIMARY KEY AUTOINCREMENT,asset_id TEXT NOT NULL,version INTEGER NOT NULL,consumer TEXT NOT NULL)")
 def register_provider(self,provider,public):
  if not provider:raise ValueError('provider required')
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO providers VALUES(?,?,'active')",(provider,export_provider(public)))
 def publish_asset(self,asset_id,provider,version,metadata,data,consumer_public,signing_private):
  with sqlite3.connect(self.path) as db:
   p=db.execute("SELECT verify_key,status FROM providers WHERE provider_id=?",(provider,)).fetchone();prev=db.execute("SELECT MAX(version) FROM assets WHERE asset_id=?",(asset_id,)).fetchone()[0] or 0
   if p is None or p[1]!='active':raise PermissionError('provider unavailable')
   if version!=prev+1:raise ValueError('asset versions must be consecutive')
   enc,n,ct=seal_asset(data,consumer_public);manifest=canonical_manifest(asset_id,provider,version,metadata,ct);sig=sign_manifest(manifest,signing_private)
   if not verify_manifest(manifest,sig,load_provider(p[0])):raise PermissionError('signer is not the registered provider')
   db.execute("INSERT INTO assets VALUES(?,?,?,?,?,?,?,?,?)",(asset_id,version,provider,metadata,enc,n,ct,manifest,sig))
 def retrieve_asset(self,asset_id,version,provider,consumer,consumer_private):
  with sqlite3.connect(self.path) as db:
   r=db.execute("SELECT version,provider,metadata,encapsulation,nonce,ciphertext,manifest,signature FROM assets WHERE asset_id=? AND version=?",(asset_id,version)).fetchone();p=db.execute("SELECT verify_key,status FROM providers WHERE provider_id=?",(provider,)).fetchone()
   if r is None:raise KeyError('asset version not found')
   if r[1]!=provider or p is None or p[1]!='active':raise PermissionError('provider mismatch or inactive')
   if not verify_manifest(r[6],r[7],load_provider(p[0])):raise ValueError('manifest signature invalid')
   data=open_asset((r[3],r[4],r[5]),consumer_private)
   if canonical_manifest(asset_id,provider,r[0],r[2],r[5])!=r[6]:raise ValueError('asset manifest does not match stored fields')
   db.execute("INSERT INTO access_audit(asset_id,version,consumer) VALUES(?,?,?)",(asset_id,version,consumer));return data
 def access_count(self,asset_id):
  with sqlite3.connect(self.path) as db:r=db.execute("SELECT COUNT(*) FROM access_audit WHERE asset_id=?",(asset_id,)).fetchone()
  return r[0]
