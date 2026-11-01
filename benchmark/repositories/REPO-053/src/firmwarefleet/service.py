"""SQLite firmware rollout registry with monotonic version enforcement."""
import sqlite3
from pathlib import Path
from .crypto import canonical_manifest,sign_release,verify_release
class FirmwareFleet:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS devices(device_id TEXT PRIMARY KEY,family TEXT NOT NULL,version TEXT NOT NULL,bootloader TEXT NOT NULL,status TEXT NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS releases(release_id TEXT PRIMARY KEY,family TEXT NOT NULL,version TEXT NOT NULL,image BLOB NOT NULL,bootloader TEXT NOT NULL,manifest BLOB NOT NULL,signature BLOB NOT NULL)")
 def enroll_device(self,device_id,family,version,bootloader):
  if not all((device_id,family,version,bootloader)):raise ValueError('device fields required')
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO devices VALUES(?,?,?,?,'active')",(device_id,family,version,bootloader))
 def publish_release(self,release_id,family,version,image,minimum_bootloader,private):
  manifest=canonical_manifest(release_id,family,version,image,minimum_bootloader);sig=sign_release(manifest,private)
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO releases VALUES(?,?,?,?,?,?,?)",(release_id,family,version,image,minimum_bootloader,manifest,sig))
 def install_release(self,device_id,release_id,public):
  with sqlite3.connect(self.path) as db:
   d=db.execute("SELECT family,version,bootloader,status FROM devices WHERE device_id=?",(device_id,)).fetchone();r=db.execute("SELECT family,version,image,bootloader,manifest,signature FROM releases WHERE release_id=?",(release_id,)).fetchone()
   if d is None or r is None:raise KeyError('device or release not found')
   if d[3]!='active':raise PermissionError('device is not active')
   if d[0]!=r[0]:raise ValueError('firmware family mismatch')
   if tuple(map(int,r[1].split('.')))<=tuple(map(int,d[1].split('.'))):raise ValueError('firmware rollback rejected')
   if tuple(map(int,d[2].split('.'))) < tuple(map(int,r[3].split('.'))):raise ValueError('bootloader too old')
   if not verify_release(r[4],r[5],public):raise PermissionError('release signature invalid')
   db.execute("UPDATE devices SET version=? WHERE device_id=?",(r[1],device_id));return r[2]
 def device_version(self,device_id):
  with sqlite3.connect(self.path) as db:row=db.execute("SELECT version FROM devices WHERE device_id=?",(device_id,)).fetchone()
  return None if row is None else row[0]
