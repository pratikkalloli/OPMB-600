import pytest
from firmwarefleet_pqc.crypto import generate_release_signer,serialize_signer_public,load_signer_public
from firmwarefleet_pqc.service import FirmwareFleet
def test_verified_release_installs_and_version_advances(tmp_path):
 sk=generate_release_signer();pk=sk.public_key();app=FirmwareFleet(tmp_path/'fleet.db');app.enroll_device('d1','sensor-v2','1.0.0','2.1.0');app.publish_release('r2','sensor-v2','2.0.0',b'firmware image','2.0.0',sk);assert app.install_release('d1','r2',pk)==b'firmware image';assert app.device_version('d1')=='2.0.0'
def test_wrong_signer_family_and_rollback_rejected(tmp_path):
 sk=generate_release_signer();pk=sk.public_key();wrong=generate_release_signer().public_key();app=FirmwareFleet(tmp_path/'fleet.db');app.enroll_device('d1','sensor','2.0.0','4.0.0');app.publish_release('old','sensor','1.0.0',b'old','1.0.0',sk);app.publish_release('new','other','3.0.0',b'new','1.0.0',sk)
 with pytest.raises(ValueError):app.install_release('d1','old',pk)
 app.enroll_device('d2','other','1.0.0','4.0.0')
 with pytest.raises(PermissionError):app.install_release('d2','new',wrong)
def test_key_serialization_and_invalid_manifest():
 sk=generate_release_signer();assert load_signer_public(serialize_signer_public(sk.public_key())) is not None
 from firmwarefleet_pqc.crypto import canonical_manifest
 with pytest.raises(ValueError):canonical_manifest('r','f','1.0',b'','1.0')
