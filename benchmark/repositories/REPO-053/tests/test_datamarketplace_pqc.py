import pytest
from datamarketplace_pqc.crypto import generate_provider_signer,generate_consumer_keypair
from datamarketplace_pqc.service import DataMarketplace
def test_provider_publish_protected_exchange_and_audit(tmp_path):
 sk=generate_provider_signer();ck,cp=generate_consumer_keypair();m=DataMarketplace(tmp_path/'m.db');m.register_provider('p1',sk.public_key());m.publish_asset('asset','p1',1,b'catalog',b'synthetic data',cp,sk);assert m.retrieve_asset('asset',1,'p1','buyer',ck)==b'synthetic data';assert m.access_count('asset')==1;assert m.retrieve_asset('asset',1,'p1','buyer',ck)==b'synthetic data';assert m.access_count('asset')==2
def test_version_and_provider_checks(tmp_path):
 sk=generate_provider_signer();ck,cp=generate_consumer_keypair();m=DataMarketplace(tmp_path/'m.db');m.register_provider('p',sk.public_key())
 with pytest.raises(ValueError):m.publish_asset('a','p',2,b'm',b'd',cp,sk)
 with pytest.raises(PermissionError):m.publish_asset('a','missing',1,b'm',b'd',cp,sk)
def test_wrong_consumer_and_missing_asset(tmp_path):
 sk=generate_provider_signer();ck,cp=generate_consumer_keypair();m=DataMarketplace(tmp_path/'m.db');m.register_provider('p',sk.public_key());m.publish_asset('a','p',1,b'm',b'data',cp,sk)
 with pytest.raises(ValueError):m.retrieve_asset('a',1,'p','buyer',generate_consumer_keypair()[0])
 with pytest.raises(KeyError):m.retrieve_asset('a',2,'p','buyer',ck)
