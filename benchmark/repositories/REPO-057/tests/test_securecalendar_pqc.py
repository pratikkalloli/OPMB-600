from securecalendar_pqc.crypto import generate_host_signer,generate_participant_keypair
from securecalendar_pqc.service import SecureCalendar
def test_invitation_update_protection_and_cancel(tmp_path):
 sk=generate_host_signer();rk,rp=generate_participant_keypair();c=SecureCalendar(tmp_path/'c.db');c.create_calendar('cal','host',sk.public_key());c.register_participant('cal','guest',rp);c.invite('i','cal','host','guest',100,200,'Planning',sk);assert b'Planning' in c.verify_invitation('i','guest',rk);c.update_invitation('i','host',2,110,210,'Updated',sk);assert b'Updated' in c.verify_invitation('i','guest',rk);assert c.cancel_event('i','host');assert c.verify_invitation('i','guest',rk) is None
def test_wrong_participant_and_invalid_window(tmp_path):
 sk=generate_host_signer();rk,rp=generate_participant_keypair();c=SecureCalendar(tmp_path/'c.db');c.create_calendar('c','h',sk.public_key());c.register_participant('c','p',rp);c.invite('i','c','h','p',1,2,'x',sk)
 assert c.verify_invitation('i','other',generate_participant_keypair()[0]) is None
 try:c.invite('bad','c','h','p',3,3,'bad',sk);assert False
 except ValueError:pass
