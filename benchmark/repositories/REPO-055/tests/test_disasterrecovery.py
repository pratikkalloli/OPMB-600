from disasterrecovery.crypto import generate_recovery_signer,generate_recovery_keypair
from disasterrecovery.service import DisasterRecovery
def test_snapshot_plan_restore_compare_and_key_rotation(tmp_path):
 sk,sp=generate_recovery_signer();rk,rp=generate_recovery_keypair();d=DisasterRecovery(tmp_path/'dr.db');d.register_system('svc',rp,sp);d.create_snapshot('s1','svc',10,b'backup-a',sk);d.create_snapshot('s2','svc',20,b'backup-b',sk);assert d.plan_restore('svc',15)==['s1'];assert d.restore_snapshot('s1','svc',rk,now=30)==b'backup-a';assert d.compare_snapshots('s1','s2','svc',rk)['equal'] is False;assert len(d.restore_history('svc'))==1;sk2,sp2=generate_recovery_signer();rk2,rp2=generate_recovery_keypair();assert d.rotate_keys('svc',rp2,sp2)==2;d.create_snapshot('s3','svc',30,b'backup-c',sk2);assert d.restore_snapshot('s3','svc',rk2,now=31)==b'backup-c'
def test_missing_snapshot_and_system_binding(tmp_path):
 sk,sp=generate_recovery_signer();rk,rp=generate_recovery_keypair();d=DisasterRecovery(tmp_path/'dr.db');d.register_system('svc',rp,sp)
 try:d.restore_snapshot('missing','svc',rk,now=0);assert False
 except KeyError:pass
 d.create_snapshot('s','svc',1,b'x',sk)
 try:d.restore_snapshot('s','other',rk,now=2);assert False
 except PermissionError:pass
