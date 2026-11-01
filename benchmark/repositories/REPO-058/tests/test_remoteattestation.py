import pytest
from remoteattestation.crypto import generate_attestor
from remoteattestation.service import RemoteAttestation
def test_measurement_policy_expiration_and_history(tmp_path):
 sk,pk=generate_attestor();a=RemoteAttestation(tmp_path/'a.db');a.register_workload('svc',pk);a.create_evidence('e1','svc','sha256:abc','allow',10,50,sk);assert a.verify_package('e1','sha256:abc',20,'verifier');assert not a.verify_package('e1','sha256:wrong',20,'verifier');assert not a.verify_package('e1','sha256:abc',50,'verifier');assert [x[2] for x in a.verification_history('e1')]==['accepted','rejected','rejected']
def test_unknown_workload_and_missing_evidence(tmp_path):
 sk,pk=generate_attestor();a=RemoteAttestation(tmp_path/'a.db')
 with pytest.raises(PermissionError):a.create_evidence('e','missing','m','allow',1,5,sk)
 with pytest.raises(KeyError):a.verify_package('missing','m',2,'v')

def test_protected_evidence_exchange(tmp_path):
 from remoteattestation.crypto import generate_verifier_keypair
 sk,pk=generate_attestor();vk,vp=generate_verifier_keypair();a=RemoteAttestation(tmp_path/'exchange.db');a.register_workload('svc',pk);a.create_evidence('e','svc','m','allow',1,20,sk);env=a.export_evidence('e',vp);package=a.open_evidence_package(env,vk);assert bytes.fromhex(package['record']) and bytes.fromhex(package['signature'])
