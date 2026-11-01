"""SQLite payment instruction state machine requiring two distinct approvers."""
import sqlite3
from pathlib import Path
from .crypto import canonical_instruction,sign_approval,verify_approval,export_approver
class ClearingDesk:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS instructions(id TEXT PRIMARY KEY,amount INTEGER NOT NULL,currency TEXT NOT NULL,beneficiary TEXT NOT NULL,status TEXT NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS approvals(instruction_id TEXT NOT NULL,approver TEXT NOT NULL,signature BLOB NOT NULL,PRIMARY KEY(instruction_id,approver))")
 def create_instruction(self,iid,amount,currency,beneficiary):
  canonical_instruction(iid,amount,currency,beneficiary)
  with sqlite3.connect(self.path) as db: db.execute("INSERT INTO instructions VALUES(?,?,?,?,'pending')",(iid,amount,currency.upper(),beneficiary))
 def approve_instruction(self,iid,approver,private):
  if not approver: raise ValueError('approver required')
  with sqlite3.connect(self.path) as db:
   row=db.execute("SELECT amount,currency,beneficiary,status FROM instructions WHERE id=?",(iid,)).fetchone()
   if row is None: raise KeyError(iid)
   if row[3]!='pending': raise ValueError('instruction is not pending')
   sig=sign_approval(canonical_instruction(iid,*row[:3])+b'|approver:'+approver.encode(),private); db.execute("INSERT INTO approvals VALUES(?,?,?)",(iid,approver,sig))
 def settle_instruction(self,iid,approver_keys):
  with sqlite3.connect(self.path) as db:
   row=db.execute("SELECT amount,currency,beneficiary,status FROM instructions WHERE id=?",(iid,)).fetchone()
   if row is None: raise KeyError(iid)
   if row[3]!='pending': raise ValueError('instruction is not pending')
   approvals=db.execute("SELECT approver,signature FROM approvals WHERE instruction_id=?",(iid,)).fetchall()
   valid={export_approver(approver_keys[name]) for name,sig in approvals if name in approver_keys and verify_approval(canonical_instruction(iid,*row[:3])+b'|approver:'+name.encode(),sig,approver_keys[name])}
   if len(valid)<2: raise PermissionError('two distinct valid approvers required')
   db.execute("UPDATE instructions SET status='settled' WHERE id=?",(iid,)); return True
 def status(self,iid):
  with sqlite3.connect(self.path) as db: row=db.execute("SELECT status FROM instructions WHERE id=?",(iid,)).fetchone()
  return None if row is None else row[0]
