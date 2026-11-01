import pytest
from zoneseal.crypto import generate_zsk,canonical_zone,export_zsk,load_zsk
from zoneseal.service import ZoneSeal
def test_publish_transfer_and_serial_increase(tmp_path):
 sk,pk=generate_zsk();z=ZoneSeal(tmp_path/'z.db');z.register_zone('example.test',pk);rr=[('www.example.test.','a','192.0.2.4',300),('@','soa','ns.example.test',60)];z.publish_zone('example.test',1,rr,sk);out=z.transfer_zone('example.test',pk);assert b'192.0.2.4' in out and z.active_serial('example.test')==1
 with pytest.raises(ValueError):z.publish_zone('example.test',1,rr,sk)
def test_wrong_key_and_revoked_zone_rejected(tmp_path):
 sk,pk=generate_zsk();_,wrong=generate_zsk();z=ZoneSeal(tmp_path/'z.db');z.register_zone('x.test',pk);z.publish_zone('x.test',1,[('a.x.test','A','192.0.2.1',5)],sk)
 with pytest.raises(ValueError):z.transfer_zone('x.test',wrong)
 assert z.revoke_zone('x.test')
 with pytest.raises(PermissionError):z.transfer_zone('x.test',pk)
def test_canonicalization_and_key_serialization():
 _,pk=generate_zsk();a=canonical_zone('EXAMPLE.TEST.',2,[('WWW.','a','1.2.3.4',30)]);b=canonical_zone('example.test',2,[('www','A','1.2.3.4',30)]);assert a==b;assert load_zsk(export_zsk(pk)) is not None
