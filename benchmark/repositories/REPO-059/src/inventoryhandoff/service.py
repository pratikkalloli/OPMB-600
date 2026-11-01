"""Item registration, signed custody transfers, and chain verification."""
import sqlite3
from pathlib import Path
from .crypto import canonical_transfer,sign_transfer,verify_transfer,export_actor,load_actor
class InventoryHandoff:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS actors(actor_id TEXT PRIMARY KEY,verify_key BLOB NOT NULL,status TEXT NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS items(item_id TEXT PRIMARY KEY,batch_id TEXT NOT NULL,owner TEXT NOT NULL,status TEXT NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS transfers(item_id TEXT NOT NULL,sequence INTEGER NOT NULL,timestamp INTEGER NOT NULL,sender TEXT NOT NULL,recipient TEXT NOT NULL,record BLOB NOT NULL,signature BLOB NOT NULL,PRIMARY KEY(item_id,sequence))")
 def register_actor(self,actor,public):
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO actors VALUES(?,?,'active')",(actor,export_actor(public)))
 def register_item(self,item,batch,owner):
  with sqlite3.connect(self.path) as db:
   if db.execute("SELECT status FROM actors WHERE actor_id=?",(owner,)).fetchone()!=( 'active',):raise PermissionError('owner must be active')
   db.execute("INSERT INTO items VALUES(?,?,?,'active')",(item,batch,owner))
 def transfer_item(self,item,sender,recipient,sequence,timestamp,private):
  with sqlite3.connect(self.path) as db:
   row=db.execute("SELECT batch_id,owner,status FROM items WHERE item_id=?",(item,)).fetchone();actors={r[0]:r[1:] for r in db.execute("SELECT actor_id,verify_key,status FROM actors WHERE actor_id IN (?,?)",(sender,recipient)).fetchall()}
   if row is None:raise KeyError(item)
   if row[2]!='active' or row[1]!=sender or sender not in actors or recipient not in actors or actors[sender][1]!='active' or actors[recipient][1]!='active':raise PermissionError('invalid custody participants')
   last=db.execute("SELECT MAX(sequence) FROM transfers WHERE item_id=?",(item,)).fetchone()[0] or 0
   if sequence!=last+1:raise ValueError('transfer sequence must increase')
   record=canonical_transfer(item,row[0],sequence,timestamp,sender,recipient);sig=sign_transfer(record,private)
   if not verify_transfer(record,sig,load_actor(actors[sender][0])):raise PermissionError('sender key mismatch')
   db.execute("INSERT INTO transfers VALUES(?,?,?,?,?,?,?)",(item,sequence,timestamp,sender,recipient,record,sig));db.execute("UPDATE items SET owner=? WHERE item_id=?",(recipient,item));return True
 def verify_chain(self,item):
  with sqlite3.connect(self.path) as db:rows=db.execute("SELECT sequence,timestamp,sender,recipient,record,signature FROM transfers WHERE item_id=? ORDER BY sequence",(item,)).fetchall();r=db.execute("SELECT batch_id FROM items WHERE item_id=?",(item,)).fetchone();keys={x[0]:x[1] for x in db.execute("SELECT actor_id,verify_key FROM actors").fetchall()}
  if r is None:return False
  return all(row[0]==i+1 and row[2] in keys and verify_transfer(row[4],row[5],load_actor(keys[row[2]])) and canonical_transfer(item,r[0],row[0],row[1],row[2],row[3])==row[4] for i,row in enumerate(rows))
 def custody_history(self,item):
  with sqlite3.connect(self.path) as db:return db.execute("SELECT sequence,timestamp,sender,recipient FROM transfers WHERE item_id=? ORDER BY sequence",(item,)).fetchall()
