"""Append-only shipment custody events and sequence verification."""
import sqlite3,time
from pathlib import Path
from .crypto import canonical_handoff,sign_handoff,verify_handoff,event_digest


class ShipmentLedger:
    def __init__(self,path:str|Path):
        self.path=str(path)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS shipments(shipment TEXT PRIMARY KEY,current_holder TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS handoffs(shipment TEXT NOT NULL,sequence INTEGER NOT NULL,sender TEXT NOT NULL,recipient TEXT NOT NULL,location TEXT NOT NULL,at INTEGER NOT NULL,previous TEXT NOT NULL,payload BLOB NOT NULL,signature BLOB NOT NULL,PRIMARY KEY(shipment,sequence))")

    def register_shipment(self,shipment:str,initial_holder:str)->None:
        if not shipment or not initial_holder: raise ValueError("shipment and holder are required")
        with sqlite3.connect(self.path) as db: db.execute("INSERT INTO shipments VALUES(?,?)",(shipment,initial_holder))

    def transfer_custody(self,shipment:str,sender:str,recipient:str,location:str,private,*,at:int|None=None)->int:
        timestamp=int(time.time()) if at is None else at
        with sqlite3.connect(self.path) as db:
            row=db.execute("SELECT current_holder FROM shipments WHERE shipment=?",(shipment,)).fetchone()
            if row is None: raise KeyError("shipment not found")
            if row[0]!=sender: raise PermissionError("sender is not current custodian")
            prior=db.execute("SELECT sequence,payload,signature FROM handoffs WHERE shipment=? ORDER BY sequence DESC LIMIT 1",(shipment,)).fetchone()
            sequence=1 if prior is None else prior[0]+1
            previous="0"*64 if prior is None else event_digest(prior[1],prior[2])
            payload=canonical_handoff(shipment,sequence,sender,recipient,location,timestamp,previous)
            signature=sign_handoff(payload,private)
            db.execute("INSERT INTO handoffs VALUES(?,?,?,?,?,?,?,?,?)",(shipment,sequence,sender,recipient,location,timestamp,previous,payload,signature))
            db.execute("UPDATE shipments SET current_holder=? WHERE shipment=?",(recipient,shipment))
            return sequence

    def verify_chain(self,shipment:str,public_keys:dict[str,object])->bool:
        with sqlite3.connect(self.path) as db: rows=db.execute("SELECT sequence,sender,recipient,location,at,previous,payload,signature FROM handoffs WHERE shipment=? ORDER BY sequence",(shipment,)).fetchall()
        if not rows: return False
        prior="0"*64; expected_sender=None
        for index,row in enumerate(rows,1):
            seq,sender,recipient,location,at,previous,payload,signature=row
            if seq!=index or previous!=prior or (expected_sender is not None and sender!=expected_sender): return False
            public=public_keys.get(sender)
            if public is None or not verify_handoff(canonical_handoff(shipment,seq,sender,recipient,location,at,previous),signature,public): return False
            prior=event_digest(payload,signature); expected_sender=recipient
        return True

    def history(self,shipment:str):
        with sqlite3.connect(self.path) as db: return db.execute("SELECT sequence,sender,recipient,location,at FROM handoffs WHERE shipment=? ORDER BY sequence",(shipment,)).fetchall()
