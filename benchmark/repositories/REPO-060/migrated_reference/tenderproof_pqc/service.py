"""Tender deadlines, bidder enrollment, confidential bid storage, and audit."""
import sqlite3,json
from pathlib import Path
from .crypto import canonical_bid,sign_bid,verify_bid,encrypt_bid,decrypt_bid,export_bidder_key,load_bidder_key,load_evaluator_key,export_evaluator_key
class TenderProof:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS tenders(tender_id TEXT PRIMARY KEY,deadline INTEGER NOT NULL,evaluator_key BLOB NOT NULL,status TEXT NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS bidders(tender_id TEXT NOT NULL,bidder TEXT NOT NULL,verify_key BLOB NOT NULL,status TEXT NOT NULL,PRIMARY KEY(tender_id,bidder))")
   db.execute("CREATE TABLE IF NOT EXISTS bids(bid_id TEXT PRIMARY KEY,tender_id TEXT NOT NULL,bidder TEXT NOT NULL,submitted_at INTEGER NOT NULL,record BLOB NOT NULL,signature BLOB NOT NULL,encapsulation BLOB NOT NULL,nonce BLOB NOT NULL,ciphertext BLOB NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS audit(bid_id TEXT NOT NULL,evaluator TEXT NOT NULL,opened_at INTEGER NOT NULL)")
 def create_tender(self,tender_id,deadline,evaluator_public):
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO tenders VALUES(?,?,?,'open')",(tender_id,deadline,evaluator_public.public_bytes_raw() if hasattr(evaluator_public,'public_bytes_raw') else evaluator_public.public_bytes(__import__('cryptography').hazmat.primitives.serialization.Encoding.Raw,__import__('cryptography').hazmat.primitives.serialization.PublicFormat.Raw)))
 def register_bidder(self,tender_id,bidder,public):
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO bidders VALUES(?,?,?,'active')",(tender_id,bidder,export_bidder_key(public)))
 def submit_bid(self,tender_id,bidder,bid_id,amount_minor,proposal,submitted_at,private):
  with sqlite3.connect(self.path) as db:
   t=db.execute("SELECT deadline,status,evaluator_key FROM tenders WHERE tender_id=?",(tender_id,)).fetchone();b=db.execute("SELECT verify_key,status FROM bidders WHERE tender_id=? AND bidder=?",(tender_id,bidder)).fetchone()
   if t is None or t[1]!='open' or b is None or b[1]!='active':raise PermissionError('tender or bidder unavailable')
   if submitted_at>t[0]:raise ValueError('bid deadline passed')
   record=canonical_bid(tender_id,bidder,bid_id,amount_minor,proposal,submitted_at);sig=sign_bid(record,private)
   if not verify_bid(record,sig,load_bidder_key(b[0])):raise PermissionError('bid signer mismatch')
   env=encrypt_bid(proposal,load_evaluator_key(t[2]));db.execute("INSERT INTO bids VALUES(?,?,?,?,?,?,?,?,?)",(bid_id,tender_id,bidder,submitted_at,record,sig,*env))
 def open_bid(self,bid_id,evaluator,private,*,now):
  with sqlite3.connect(self.path) as db:
   r=db.execute("SELECT tender_id,bidder,record,signature,encapsulation,nonce,ciphertext,submitted_at FROM bids WHERE bid_id=?",(bid_id,)).fetchone()
   if r is None:raise KeyError(bid_id)
   b=db.execute("SELECT verify_key,status FROM bidders WHERE tender_id=? AND bidder=?",(r[0],r[1])).fetchone();t=db.execute("SELECT evaluator_key FROM tenders WHERE tender_id=?",(r[0],)).fetchone()
   if b is None or b[1]!='active' or t is None:raise PermissionError('bidder or tender unavailable')
   if not verify_bid(r[2],r[3],load_bidder_key(b[0])):raise ValueError('bid signature invalid')
   if export_evaluator_key(private.public_key())!=t[0]:raise PermissionError('wrong evaluator key')
   proposal=decrypt_bid((r[4],r[5],r[6]),private);meta=json.loads(r[2]);expected=canonical_bid(r[0],r[1],bid_id,meta['amount_minor'],proposal,r[7])
   if expected!=r[2]:raise ValueError('bid metadata or proposal integrity failed')
   db.execute("INSERT INTO audit VALUES(?,?,?)",(bid_id,evaluator,now));return proposal
 def audit_history(self,bid_id):
  with sqlite3.connect(self.path) as db:return db.execute("SELECT evaluator,opened_at FROM audit WHERE bid_id=? ORDER BY rowid",(bid_id,)).fetchall()
