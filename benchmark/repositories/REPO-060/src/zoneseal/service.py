"""Signed zone publication with serial anti-rollback and verification."""
import sqlite3
from pathlib import Path
from .crypto import canonical_zone,sign_zone,verify_zone,export_zsk,load_zsk
class ZoneSeal:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS zones(zone TEXT PRIMARY KEY,verify_key BLOB NOT NULL,status TEXT NOT NULL,serial INTEGER NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS snapshots(zone TEXT NOT NULL,serial INTEGER NOT NULL,records BLOB NOT NULL,signature BLOB NOT NULL,PRIMARY KEY(zone,serial))")
 def register_zone(self,zone,public):
  if not zone:raise ValueError('zone required')
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO zones VALUES(?,?,'active',0)",(zone.lower().rstrip('.'),export_zsk(public)))
 def revoke_zone(self,zone):
  with sqlite3.connect(self.path) as db:return db.execute("UPDATE zones SET status='revoked' WHERE zone=? AND status='active'",(zone.lower().rstrip('.'),)).rowcount==1
 def publish_zone(self,zone,serial,records,private):
  key=zone.lower().rstrip('.');payload=canonical_zone(key,serial,records);sig=sign_zone(payload,private)
  with sqlite3.connect(self.path) as db:
   row=db.execute("SELECT serial,status FROM zones WHERE zone=?",(key,)).fetchone()
   if row is None or row[1]!='active':raise PermissionError('zone is not active')
   if serial<=row[0]:raise ValueError('zone serial must increase')
   db.execute("INSERT INTO snapshots VALUES(?,?,?,?)",(key,serial,payload,sig));db.execute("UPDATE zones SET serial=? WHERE zone=?",(serial,key))
 def transfer_zone(self,zone,public):
  key=zone.lower().rstrip('.')
  with sqlite3.connect(self.path) as db:
   row=db.execute("SELECT verify_key,status,serial FROM zones WHERE zone=?",(key,)).fetchone()
   if row is None or row[1]!='active':raise PermissionError('zone is not active')
   snap=db.execute("SELECT records,signature FROM snapshots WHERE zone=? AND serial=?",(key,row[2])).fetchone()
  if snap is None:raise KeyError('zone snapshot missing')
  stored=load_zsk(row[0])
  if not verify_zone(snap[0],snap[1],stored) or not verify_zone(snap[0],snap[1],public):raise ValueError('zone snapshot signature invalid')
  return snap[0]
 def active_serial(self,zone):
  with sqlite3.connect(self.path) as db:r=db.execute("SELECT serial FROM zones WHERE zone=? AND status='active'",(zone.lower().rstrip('.'),)).fetchone()
  return None if r is None else r[0]
