"""Synthetic workload measurement registration and policy verification history."""
import sqlite3,json
from pathlib import Path
from .crypto import canonical_evidence,sign_evidence,verify_evidence_signature,export_attestor,load_attestor,protect_evidence,open_evidence
class RemoteAttestation:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS workloads(workload_id TEXT PRIMARY KEY,verify_key BLOB NOT NULL,status TEXT NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS evidence(evidence_id TEXT PRIMARY KEY,workload_id TEXT NOT NULL,measurement TEXT NOT NULL,policy TEXT NOT NULL,issued_at INTEGER NOT NULL,expires_at INTEGER NOT NULL,record BLOB NOT NULL,signature BLOB NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS verification_history(id INTEGER PRIMARY KEY AUTOINCREMENT,evidence_id TEXT NOT NULL,verifier TEXT NOT NULL,checked_at INTEGER NOT NULL,result TEXT NOT NULL)")
 def register_workload(self,workload_id,attestor_public):
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO workloads VALUES(?,?,'active')",(workload_id,export_attestor(attestor_public)))
 def create_evidence(self,evidence_id,workload_id,measurement,policy,issued_at,expires_at,private):
  record=canonical_evidence(evidence_id,workload_id,measurement,policy,issued_at,expires_at);sig=sign_evidence(record,private)
  with sqlite3.connect(self.path) as db:
   w=db.execute("SELECT verify_key,status FROM workloads WHERE workload_id=?",(workload_id,)).fetchone()
   if w is None or w[1]!='active':raise PermissionError('workload unavailable')
   if not verify_evidence_signature(record,sig,load_attestor(w[0])):raise PermissionError('evidence signer is not the registered workload')
   db.execute("INSERT INTO evidence VALUES(?,?,?,?,?,?,?,?)",(evidence_id,workload_id,measurement,policy,issued_at,expires_at,record,sig))
 def verify_package(self,evidence_id,expected_measurement,now,verifier):
  with sqlite3.connect(self.path) as db:
   e=db.execute("SELECT workload_id,measurement,policy,issued_at,expires_at,record,signature FROM evidence WHERE evidence_id=?",(evidence_id,)).fetchone()
   if e is None:raise KeyError(evidence_id)
   w=db.execute("SELECT verify_key,status FROM workloads WHERE workload_id=?",(e[0],)).fetchone()
   canonical=canonical_evidence(evidence_id,e[0],e[1],e[2],e[3],e[4]);ok=bool(w and w[1]=='active' and e[3]<=now<e[4] and e[1]==expected_measurement and e[2]=='allow' and canonical==e[5] and verify_evidence_signature(e[5],e[6],load_attestor(w[0])))
   db.execute("INSERT INTO verification_history(evidence_id,verifier,checked_at,result) VALUES(?,?,?,?)",(evidence_id,verifier,now,'accepted' if ok else 'rejected'));return ok

 def export_evidence(self,evidence_id,verifier_public):
  with sqlite3.connect(self.path) as db:r=db.execute("SELECT record,signature FROM evidence WHERE evidence_id=?",(evidence_id,)).fetchone()
  if r is None:raise KeyError(evidence_id)
  package=json.dumps({'record':r[0].hex(),'signature':r[1].hex()},sort_keys=True,separators=(',',':')).encode();return protect_evidence(package,verifier_public)
 def open_evidence_package(self,envelope,verifier_private):
  try:return json.loads(open_evidence(envelope,verifier_private))
  except (ValueError,KeyError,TypeError) as exc:raise ValueError('invalid evidence package') from exc
 def verification_history(self,evidence_id):
  with sqlite3.connect(self.path) as db:return db.execute("SELECT verifier,checked_at,result FROM verification_history WHERE evidence_id=? ORDER BY id",(evidence_id,)).fetchall()
