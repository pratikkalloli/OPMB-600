"""Sensor registry with fail-closed, monotonic reading acceptance."""
import sqlite3
from pathlib import Path
from .crypto import canonical_reading,sign_reading,verify_reading,export_device_key,load_device_key
class SensorAttest:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS devices(device_id TEXT PRIMARY KEY,verify_key BLOB NOT NULL,status TEXT NOT NULL,last_sequence INTEGER NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS readings(device_id TEXT NOT NULL,sequence INTEGER NOT NULL,timestamp INTEGER NOT NULL,metric TEXT NOT NULL,value REAL NOT NULL,record BLOB NOT NULL,signature BLOB NOT NULL,PRIMARY KEY(device_id,sequence))")
 def enroll(self,device_id,public):
  if not device_id:raise ValueError('device ID required')
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO devices VALUES(?,?,'active',0)",(device_id,export_device_key(public)))
 def deactivate(self,device_id):
  with sqlite3.connect(self.path) as db:return db.execute("UPDATE devices SET status='inactive' WHERE device_id=? AND status='active'",(device_id,)).rowcount==1
 def submit(self,device_id,sequence,timestamp,metric,value,signature):
  record=canonical_reading(device_id,sequence,timestamp,metric,value)
  with sqlite3.connect(self.path) as db:
   row=db.execute("SELECT verify_key,status,last_sequence FROM devices WHERE device_id=?",(device_id,)).fetchone()
   if row is None or row[1]!='active':raise PermissionError('sensor is not active')
   if sequence<=row[2]:raise ValueError('replayed or out-of-order sensor reading')
   if not verify_reading(record,signature,load_device_key(row[0])):raise PermissionError('sensor signature invalid')
   db.execute("INSERT INTO readings VALUES(?,?,?,?,?,?,?)",(device_id,sequence,timestamp,metric,value,record,signature));db.execute("UPDATE devices SET last_sequence=? WHERE device_id=?",(sequence,device_id));return True
 def last_sequence(self,device_id):
  with sqlite3.connect(self.path) as db:r=db.execute("SELECT last_sequence FROM devices WHERE device_id=?",(device_id,)).fetchone()
  return None if r is None else r[0]
