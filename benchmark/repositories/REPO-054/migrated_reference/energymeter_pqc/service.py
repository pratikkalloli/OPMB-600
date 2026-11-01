"""Meter registry, key rotation, ordered readings, and audit history."""
import sqlite3
from pathlib import Path
from .crypto import canonical_reading,sign_reading,verify_reading,export_meter_key,load_meter_key
class EnergyMeter:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS meters(meter_id TEXT PRIMARY KEY,verify_key BLOB NOT NULL,key_version INTEGER NOT NULL,status TEXT NOT NULL,last_sequence INTEGER NOT NULL,last_timestamp INTEGER NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS meter_keys(meter_id TEXT NOT NULL,key_version INTEGER NOT NULL,verify_key BLOB NOT NULL,PRIMARY KEY(meter_id,key_version))")
   db.execute("CREATE TABLE IF NOT EXISTS readings(meter_id TEXT NOT NULL,sequence INTEGER NOT NULL,timestamp INTEGER NOT NULL,value REAL NOT NULL,unit TEXT NOT NULL,record BLOB NOT NULL,signature BLOB NOT NULL,key_version INTEGER NOT NULL,PRIMARY KEY(meter_id,sequence))")
 def register_meter(self,meter_id,public):
  if not meter_id:raise ValueError('meter ID required')
  with sqlite3.connect(self.path) as db:
   raw=export_meter_key(public);db.execute("INSERT INTO meters VALUES(?,?,1,'active',0,0)",(meter_id,raw));db.execute("INSERT INTO meter_keys VALUES(?,1,?)",(meter_id,raw))
 def rotate_meter_key(self,meter_id,new_public):
  with sqlite3.connect(self.path) as db:
   row=db.execute("SELECT key_version,status FROM meters WHERE meter_id=?",(meter_id,)).fetchone()
   if row is None or row[1]!='active':raise PermissionError('meter unavailable')
   version=row[0]+1;raw=export_meter_key(new_public);db.execute("UPDATE meters SET verify_key=?,key_version=? WHERE meter_id=?",(raw,version,meter_id));db.execute("INSERT INTO meter_keys VALUES(?,?,?)",(meter_id,version,raw));return version
 def submit_reading(self,meter_id,sequence,timestamp,value,unit,signature):
  record=canonical_reading(meter_id,sequence,timestamp,value,unit)
  with sqlite3.connect(self.path) as db:
   m=db.execute("SELECT verify_key,key_version,status,last_sequence,last_timestamp FROM meters WHERE meter_id=?",(meter_id,)).fetchone()
   if m is None or m[2]!='active':raise PermissionError('meter inactive')
   if sequence!=m[3]+1 or timestamp<m[4]:raise ValueError('meter sequence or time invalid')
   if not verify_reading(record,signature,load_meter_key(m[0])):raise PermissionError('meter signature invalid')
   db.execute("INSERT INTO readings VALUES(?,?,?,?,?,?,?,?)",(meter_id,sequence,timestamp,value,unit,record,signature,m[1]));db.execute("UPDATE meters SET last_sequence=?,last_timestamp=? WHERE meter_id=?",(sequence,timestamp,meter_id));return True
 def verify_history(self,meter_id):
  with sqlite3.connect(self.path) as db:r=db.execute("SELECT sequence,timestamp,value,unit,record,signature,key_version FROM readings WHERE meter_id=? ORDER BY sequence",(meter_id,)).fetchall();m=db.execute("SELECT 1 FROM meters WHERE meter_id=?",(meter_id,)).fetchone();keys={x[0]:x[1] for x in db.execute("SELECT key_version,verify_key FROM meter_keys WHERE meter_id=?",(meter_id,)).fetchall()}
  if m is None:return False
  return all(row[6] in keys and verify_reading(row[4],row[5],load_meter_key(keys[row[6]])) and canonical_reading(meter_id,row[0],row[1],row[2],row[3])==row[4] for row in r)
 def audit_history(self,meter_id):
  with sqlite3.connect(self.path) as db:return db.execute("SELECT sequence,timestamp,value,unit,key_version FROM readings WHERE meter_id=? ORDER BY sequence",(meter_id,)).fetchall()
