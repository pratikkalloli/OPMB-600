"""Calendar participant registry and protected invitation lifecycle."""
import sqlite3
from pathlib import Path
from .crypto import canonical_invitation,sign_invitation,verify_invitation,protect_event,open_event,export_host_key,load_host_key,export_participant_key,load_participant_key
class SecureCalendar:
 def __init__(self,path:str|Path):
  self.path=str(path)
  with sqlite3.connect(self.path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS calendars(calendar_id TEXT PRIMARY KEY,host TEXT NOT NULL,host_key BLOB NOT NULL,status TEXT NOT NULL)")
   db.execute("CREATE TABLE IF NOT EXISTS participants(calendar_id TEXT NOT NULL,participant TEXT NOT NULL,exchange_key BLOB NOT NULL,status TEXT NOT NULL,PRIMARY KEY(calendar_id,participant))")
   db.execute("CREATE TABLE IF NOT EXISTS invitations(invite_id TEXT PRIMARY KEY,calendar_id TEXT NOT NULL,host TEXT NOT NULL,participant TEXT NOT NULL,version INTEGER NOT NULL,start INTEGER NOT NULL,end INTEGER NOT NULL,title TEXT NOT NULL,encapsulation BLOB NOT NULL,nonce BLOB NOT NULL,ciphertext BLOB NOT NULL,signature BLOB NOT NULL,status TEXT NOT NULL)")
 def create_calendar(self,cid,host,host_public):
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO calendars VALUES(?,?,?,'active')",(cid,host,export_host_key(host_public)))
 def register_participant(self,cid,participant,exchange_public):
  with sqlite3.connect(self.path) as db:db.execute("INSERT INTO participants VALUES(?,?,?,'active')",(cid,participant,export_participant_key(exchange_public)))
 def _save(self,iid,cid,host,participant,version,start,end,title,host_private):
  with sqlite3.connect(self.path) as db:
   c=db.execute("SELECT host,host_key,status FROM calendars WHERE calendar_id=?",(cid,)).fetchone();p=db.execute("SELECT exchange_key,status FROM participants WHERE calendar_id=? AND participant=?",(cid,participant)).fetchone()
   if c is None or p is None or c[0]!=host or c[2]!='active' or p[1]!='active':raise PermissionError('calendar or participant unavailable')
   existing=db.execute("SELECT version FROM invitations WHERE invite_id=?",(iid,)).fetchone()
   if existing and version!=existing[0]+1:raise ValueError('invitation versions must increase')
   if not existing and version!=1:raise ValueError('initial invitation version must be one')
   data=canonical_invitation(iid,cid,host,participant,version,start,end,title);env=protect_event(data,load_participant_key(p[0]));sig=sign_invitation(data,host_private)
   if not verify_invitation(data,sig,load_host_key(c[1])):raise PermissionError('signer is not the calendar host')
   if existing:db.execute("UPDATE invitations SET version=?,start=?,end=?,title=?,encapsulation=?,nonce=?,ciphertext=?,signature=?,status='active' WHERE invite_id=?",(version,start,end,title,*env,sig,iid))
   else:db.execute("INSERT INTO invitations VALUES(?,?,?,?,?,?,?,?,?,?,?,?,'active')",(iid,cid,host,participant,version,start,end,title,*env,sig))
 def invite(self,iid,cid,host,participant,start,end,title,host_private):return self._save(iid,cid,host,participant,1,start,end,title,host_private)
 def update_invitation(self,iid,host,version,start,end,title,host_private):
  with sqlite3.connect(self.path) as db:r=db.execute("SELECT calendar_id,participant,status FROM invitations WHERE invite_id=?",(iid,)).fetchone()
  if r is None or r[2]!='active':raise PermissionError('invitation inactive or missing')
  return self._save(iid,r[0],host,r[1],version,start,end,title,host_private)
 def cancel_event(self,iid,host):
  with sqlite3.connect(self.path) as db:return db.execute("UPDATE invitations SET status='cancelled' WHERE invite_id=? AND host=? AND status='active'",(iid,host)).rowcount==1
 def verify_invitation(self,iid,participant,participant_private):
  with sqlite3.connect(self.path) as db:r=db.execute("SELECT calendar_id,host,participant,version,start,end,title,encapsulation,nonce,ciphertext,signature,status FROM invitations WHERE invite_id=?",(iid,)).fetchone();c=db.execute("SELECT host_key,status FROM calendars WHERE calendar_id=?",(r[0],)).fetchone() if r else None
  if r is None or r[2]!=participant or r[11]!='active' or c is None or c[1]!='active':return None
  data=open_event((r[7],r[8],r[9]),participant_private);record=canonical_invitation(iid,r[0],r[1],r[2],r[3],r[4],r[5],r[6])
  if data!=record or not verify_invitation(data,r[10],load_host_key(c[0])):raise ValueError('invitation verification failed')
  return data
