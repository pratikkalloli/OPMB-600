"""Generate Team A's isolated REPO-018 through REPO-032 contribution."""
from __future__ import annotations

import json
import re
import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
START_TASK = 171

APPS = [
    dict(name="DNSZoneGuard", slug="dnszoneguard", repo="REPO-018", domain="dns_zone_integrity", entity="zone_update", plural="zone updates", noun="zone signing", title="DNS zone integrity and signed zone updates", required=["zone", "serial", "changes", "published_at"], key="zone", rules=["if not isinstance(record['serial'], int) or record['serial'] < 1: raise ValueError('zone serial must be a positive integer')", "if not isinstance(record['changes'], list) or not record['changes']: raise ValueError('zone changes must be a non-empty list')", "if not str(record['zone']).strip().endswith('.'): raise ValueError('zone name must be fully qualified')"], sample={"zone":"example.test.","serial":1,"changes":[{"name":"www.example.test.","type":"A","value":"192.0.2.10"}],"published_at":"2030-01-01T00:00:00Z"}),
    dict(name="WebhookShield", slug="webhookshield", repo="REPO-019", domain="signed_webhook_delivery", entity="delivery", plural="webhook deliveries", noun="delivery signing", title="Signed webhook delivery and replay protection", required=["endpoint_id", "event_id", "nonce", "timestamp", "body"], key="event_id", rules=["if not str(record['nonce']).strip(): raise ValueError('nonce is required')", "if not isinstance(record['body'], dict): raise ValueError('webhook body must be an object')"], sample={"endpoint_id":"billing-hook","event_id":"evt-001","nonce":"n-001","timestamp":1893456000,"body":{"kind":"invoice.paid","invoice":"inv-123"}}),
    dict(name="TimeSeal", slug="timeseal", repo="REPO-020", domain="timestamp_tokens", entity="timestamp_token", plural="timestamp tokens", noun="timestamp-token signing", title="Signed timestamp-token simulation", required=["token_id", "subject_digest", "issued_at", "expires_at", "authority"], key="token_id", rules=["if record['issued_at'] >= record['expires_at']: raise ValueError('token expiry must follow issuance')", "if len(str(record['subject_digest'])) != 64: raise ValueError('subject digest must be a SHA-256 hex digest')"], sample={"token_id":"tsa-001","subject_digest":"a"*64,"issued_at":1893456000,"expires_at":1893459600,"authority":"test-authority"}),
    dict(name="MailGuard", slug="mailguard", repo="REPO-021", domain="secure_email_envelopes", entity="mail_envelope", plural="mail envelopes", noun="email-envelope signing", title="Secure email envelopes and attachments", required=["message_id", "sender", "recipient", "subject", "body", "attachments"], key="message_id", rules=["if '@' not in str(record['sender']) or '@' not in str(record['recipient']): raise ValueError('sender and recipient must be email addresses')", "if not isinstance(record['attachments'], list): raise ValueError('attachments must be a list')"], sample={"message_id":"mail-001","sender":"sender@example.test","recipient":"recipient@example.test","subject":"Report","body":"Quarterly report attached","attachments":[{"name":"report.pdf","digest":"b"*64}]}),
    dict(name="SessionExchange", slug="sessionexchange", repo="REPO-022", domain="secure_session_establishment", entity="session_offer", plural="session offers", noun="session-negotiation signing", title="Secure session establishment and negotiation", required=["session_id", "initiator", "responder", "offered_suites", "nonce", "transcript_hash"], key="session_id", rules=["if not record['offered_suites']: raise ValueError('at least one suite must be offered')", "if record['initiator'] == record['responder']: raise ValueError('session peers must be distinct')"], sample={"session_id":"sess-001","initiator":"client-1","responder":"gateway-1","offered_suites":["ML-KEM-768+A256GCM"],"nonce":"c"*32,"transcript_hash":"d"*64}),
    dict(name="ConfigSign", slug="configsign", repo="REPO-023", domain="signed_configuration_distribution", entity="configuration_release", plural="configuration releases", noun="configuration-release signing", title="Signed configuration distribution and rollback protection", required=["system_id", "version", "settings", "issued_at"], key="system_id", rules=["if not isinstance(record['version'], int) or record['version'] < 1: raise ValueError('configuration version must be positive')", "if not isinstance(record['settings'], dict): raise ValueError('settings must be an object')"], sample={"system_id":"edge-west","version":1,"settings":{"log_level":"info","feature_x":True},"issued_at":"2030-01-01T00:00:00Z"}),
    dict(name="DataProvenance", slug="dataprovenance", repo="REPO-024", domain="verifiable_data_provenance", entity="provenance_checkpoint", plural="provenance checkpoints", noun="provenance-checkpoint signing", title="Signed data provenance and verifiable checkpoints", required=["object_id", "sequence", "source", "payload_digest", "previous_digest"], key="object_id", rules=["if not isinstance(record['sequence'], int) or record['sequence'] < 1: raise ValueError('checkpoint sequence must be positive')", "if len(str(record['payload_digest'])) != 64: raise ValueError('payload digest must be SHA-256 hex')"], sample={"object_id":"dataset-7","sequence":1,"source":"ingest-01","payload_digest":"e"*64,"previous_digest":"0"*64}),
    dict(name="MediaRights", slug="mediarights", repo="REPO-025", domain="protected_media_rights", entity="rights_manifest", plural="rights manifests", noun="media-rights signing", title="Protected media distribution and signed rights manifests", required=["asset_id", "owner", "licensee", "starts_at", "expires_at", "rights", "territories"], key="asset_id", rules=["if record['starts_at'] >= record['expires_at']: raise ValueError('rights expiry must follow start')", "if not record['rights'] or not record['territories']: raise ValueError('rights and territories must be non-empty')"], sample={"asset_id":"movie-42","owner":"studio-a","licensee":"library-b","starts_at":1893456000,"expires_at":1896048000,"rights":["stream"],"territories":["US"]}),
    dict(name="SecureSurvey", slug="securesurvey", repo="REPO-026", domain="encrypted_survey_submissions", entity="survey_submission", plural="survey submissions", noun="survey-receipt signing", title="Encrypted survey responses and signed submission receipts", required=["survey_id", "response_id", "answers", "submitted_at"], key="response_id", rules=["if not isinstance(record['answers'], dict) or not record['answers']: raise ValueError('answers must be a non-empty object')", "if not str(record['survey_id']).strip(): raise ValueError('survey id is required')"], sample={"survey_id":"study-1","response_id":"resp-001","answers":{"q1":"yes","q2":4},"submitted_at":"2030-01-01T00:00:00Z"}),
    dict(name="GeoDispatch", slug="geodispatch", repo="REPO-027", domain="protected_dispatch_instructions", entity="dispatch_instruction", plural="dispatch instructions", noun="dispatch-instruction signing", title="Protected dispatch instructions and signed location records", required=["dispatch_id", "vehicle_id", "destination", "issued_at", "expires_at"], key="dispatch_id", rules=["if not isinstance(record['destination'], dict) or not {'lat','lon'} <= set(record['destination']): raise ValueError('destination requires latitude and longitude')", "if not -90 <= record['destination']['lat'] <= 90 or not -180 <= record['destination']['lon'] <= 180: raise ValueError('destination coordinates out of range')", "if record['issued_at'] >= record['expires_at']: raise ValueError('dispatch expiry must follow issuance')"], sample={"dispatch_id":"dispatch-1","vehicle_id":"truck-9","destination":{"lat":37.7749,"lon":-122.4194},"issued_at":1893456000,"expires_at":1893463200}),
    dict(name="DesktopUpdateProof", slug="desktopupdateproof", repo="REPO-028", domain="desktop_update_integrity", entity="update_release", plural="desktop update releases", noun="desktop-release signing", title="Desktop software update integrity and signed releases", required=["product", "version", "platform", "sha256", "released_at"], key="product", rules=["if len(str(record['sha256'])) != 64: raise ValueError('release digest must be SHA-256 hex')", "if not all(str(record[x]).strip() for x in ('product','version','platform')): raise ValueError('product, version, and platform are required')"], sample={"product":"editor","version":"2.4.0","platform":"windows-x64","sha256":"f"*64,"released_at":"2030-01-01T00:00:00Z"}),
    dict(name="PackageMirror", slug="packagemirror", repo="REPO-029", domain="package_mirror_integrity", entity="package_index", plural="package indexes", noun="package-index signing", title="Software package mirror integrity and signed indexes", required=["package", "version", "platform", "digest", "published_at"], key="package", rules=["if len(str(record['digest'])) != 64: raise ValueError('package digest must be SHA-256 hex')", "if not all(str(record[x]).strip() for x in ('package','version','platform')): raise ValueError('package, version, and platform are required')"], sample={"package":"libsample","version":"1.2.3","platform":"any","digest":"a"*64,"published_at":"2030-01-01T00:00:00Z"}),
    dict(name="ApprovalFlow", slug="approvalflow", repo="REPO-030", domain="quorum_approval_signatures", entity="approval_request", plural="approval requests", noun="approval-stage signing", title="Multi-stage approval signatures and quorum verification", required=["request_id", "stage", "approver_id", "decision", "payload_digest"], key="request_id", rules=["if record['decision'] not in ('approve','reject'): raise ValueError('decision must be approve or reject')", "if not isinstance(record['stage'], int) or record['stage'] < 1: raise ValueError('approval stage must be positive')"], sample={"request_id":"change-77","stage":1,"approver_id":"alice","decision":"approve","payload_digest":"b"*64}),
    dict(name="ClinicalConsent", slug="clinicalconsent", repo="REPO-031", domain="synthetic_clinical_consent", entity="consent_record", plural="consent records", noun="consent-record signing", title="Synthetic healthcare consent records and revocation", required=["consent_id", "subject_token", "scopes", "consented_at", "expires_at"], key="consent_id", rules=["if not record['scopes'] or not all(isinstance(x, str) for x in record['scopes']): raise ValueError('consent scopes must be non-empty strings')", "if record['consented_at'] >= record['expires_at']: raise ValueError('consent expiry must follow consent')"], sample={"consent_id":"consent-1","subject_token":"subject-opaque-7","scopes":["research:survey"],"consented_at":1893456000,"expires_at":1924992000}),
    dict(name="FleetPermit", slug="fleetpermit", repo="REPO-032", domain="offline_vehicle_permits", entity="vehicle_permit", plural="vehicle permits", noun="vehicle-permit signing", title="Vehicle permit issuance and offline verification simulation", required=["permit_id", "vehicle_id", "jurisdiction", "permit_class", "valid_from", "valid_until"], key="permit_id", rules=["if record['valid_from'] >= record['valid_until']: raise ValueError('permit validity interval is invalid')", "if not all(str(record[x]).strip() for x in ('vehicle_id','jurisdiction','permit_class')): raise ValueError('permit identity fields are required')"], sample={"permit_id":"permit-001","vehicle_id":"truck-7","jurisdiction":"CA","permit_class":"oversize","valid_from":1893456000,"valid_until":1924992000}),
]

# State transitions make each SQLite ledger specific to its application domain.
POLICIES = {
    "DNSZoneGuard": {"record_key": "f\"{record['zone']}:{record['serial']}\"", "policy": '''        rows = [json.loads(row[0]) for row in self._db.execute("SELECT body FROM signed_records").fetchall()]
        if any(item["zone"] == record["zone"] and item["serial"] >= record["serial"] for item in rows):
            raise ValueError("zone serial must advance monotonically")''', "business_test": '''    later = dict(record, serial=record["serial"] + 1)
    ledger = DNSZoneGuardLedger(tmp_path / "dns-ledger.sqlite")
    ledger.publish(identity, record)
    assert ledger.fetch(f"{record['zone']}:{record['serial']}")[0] == record
    with pytest.raises(ValueError): ledger.publish(identity, dict(record, serial=record["serial"] - 1))
    ledger.close()''', "key": "serial"},
    "WebhookShield": {"record_key": "str(record['event_id'])", "policy": '''        rows = [json.loads(row[0]) for row in self._db.execute("SELECT body FROM signed_records").fetchall()]
        if any(item["nonce"] == record["nonce"] for item in rows):
            raise ValueError("webhook nonce replay detected")''', "business_test": '''    ledger = WebhookShieldLedger(tmp_path / "webhook-ledger.sqlite")
    ledger.publish(identity, record)
    with pytest.raises(ValueError): ledger.publish(identity, dict(record, event_id="evt-002"))
    ledger.close()''', "key": "event_id"},
    "TimeSeal": {"record_key": "str(record['token_id'])", "policy": '''        rows = [json.loads(row[0]) for row in self._db.execute("SELECT body FROM signed_records").fetchall()]
        prior = [item["issued_at"] for item in rows if item["authority"] == record["authority"]]
        if prior and record["issued_at"] < max(prior):
            raise ValueError("timestamp issuance cannot move backwards")''', "business_test": '''    ledger = TimeSealLedger(tmp_path / "time-ledger.sqlite")
    ledger.publish(identity, record)
    earlier = dict(record, token_id="tsa-002", issued_at=record["issued_at"] - 1, expires_at=record["expires_at"])
    with pytest.raises(ValueError): ledger.publish(identity, earlier)
    ledger.close()''', "key": "token_id"},
    "MailGuard": {"record_key": "str(record['message_id'])", "policy": "", "business_test": '''    duplicate = dict(record, attachments=[{"name":"same.txt"},{"name":"same.txt"}])
    with pytest.raises(ValueError): validate_mail_envelope(duplicate)''', "key": "message_id"},
    "SessionExchange": {"record_key": "str(record['session_id'])", "policy": "", "business_test": '''    assert negotiate_session_suite(record, ["ML-KEM-768+A256GCM"]) == "ML-KEM-768+A256GCM"
    with pytest.raises(ValueError): negotiate_session_suite(record, ["unsupported-suite"])''', "key": "session_id"},
    "ConfigSign": {"record_key": "f\"{record['system_id']}:{record['version']}\"", "policy": '''        rows = [json.loads(row[0]) for row in self._db.execute("SELECT body FROM signed_records").fetchall()]
        versions = [item["version"] for item in rows if item["system_id"] == record["system_id"]]
        if versions and record["version"] <= max(versions):
            raise ValueError("configuration version rollback or duplicate")''', "business_test": '''    ledger = ConfigSignLedger(tmp_path / "config-ledger.sqlite")
    ledger.publish(identity, record)
    with pytest.raises(ValueError): ledger.publish(identity, dict(record, version=record["version"]))
    ledger.close()''', "key": "system_id"},
    "DataProvenance": {"record_key": "f\"{record['object_id']}:{record['sequence']}\"", "policy": '''        rows = [json.loads(row[0]) for row in self._db.execute("SELECT body FROM signed_records").fetchall()]
        prior = [item for item in rows if item["object_id"] == record["object_id"]]
        if not prior:
            if record["sequence"] != 1 or record["previous_digest"] != "0" * 64:
                raise ValueError("first checkpoint must start a new provenance chain")
        else:
            latest = max(prior, key=lambda item: item["sequence"])
            if record["sequence"] != latest["sequence"] + 1 or record["previous_digest"] != latest["payload_digest"]:
                raise ValueError("provenance checkpoint does not extend the latest digest")''', "business_test": '''    second = dict(record, sequence=2, payload_digest="c"*64, previous_digest=record["payload_digest"])
    ledger = DataProvenanceLedger(tmp_path / "provenance.sqlite")
    ledger.publish(identity, record)
    ledger.publish(identity, second)
    with pytest.raises(ValueError): ledger.publish(identity, dict(second, sequence=3, previous_digest="0"*64))
    ledger.close()''', "key": "object_id"},
    "MediaRights": {"record_key": "f\"{record['asset_id']}:{record['licensee']}:{record['starts_at']}\"", "policy": '''        rows = [json.loads(row[0]) for row in self._db.execute("SELECT body FROM signed_records").fetchall()]
        for item in rows:
            same_grant = item["asset_id"] == record["asset_id"] and item["licensee"] == record["licensee"]
            overlaps = record["starts_at"] < item["expires_at"] and item["starts_at"] < record["expires_at"]
            if same_grant and overlaps:
                raise ValueError("media-rights grant overlaps an existing active interval")''', "business_test": '''    ledger = MediaRightsLedger(tmp_path / "rights.sqlite")
    ledger.publish(identity, record)
    with pytest.raises(ValueError): ledger.publish(identity, dict(record, starts_at=record["starts_at"] + 1))
    ledger.close()''', "key": "asset_id"},
    "SecureSurvey": {"record_key": "str(record['response_id'])", "policy": "", "business_test": '''    ledger = SecureSurveyLedger(tmp_path / "survey.sqlite")
    ledger.publish(identity, record)
    with pytest.raises(ValueError): ledger.publish(identity, dict(record, survey_id="study-2"))
    ledger.close()''', "key": "response_id"},
    "GeoDispatch": {"record_key": "str(record['dispatch_id'])", "policy": "", "business_test": '''    with pytest.raises(ValueError): validate_dispatch_instruction(dict(record, destination={"lat":91,"lon":0}))''', "key": "dispatch_id"},
    "DesktopUpdateProof": {"record_key": "f\"{record['product']}:{record['platform']}:{record['version']}\"", "policy": '''        rows = [json.loads(row[0]) for row in self._db.execute("SELECT body FROM signed_records").fetchall()]
        versions = [tuple(int(part) for part in item["version"].split(".")) for item in rows if item["product"] == record["product"] and item["platform"] == record["platform"]]
        incoming = tuple(int(part) for part in record["version"].split("."))
        if versions and incoming <= max(versions):
            raise ValueError("desktop update version rollback or duplicate")''', "business_test": '''    ledger = DesktopUpdateProofLedger(tmp_path / "updates.sqlite")
    ledger.publish(identity, record)
    with pytest.raises(ValueError): ledger.publish(identity, dict(record, version="2.3.9"))
    ledger.close()''', "key": "product"},
    "PackageMirror": {"record_key": "f\"{record['package']}:{record['platform']}:{record['version']}\"", "policy": '''        rows = [json.loads(row[0]) for row in self._db.execute("SELECT body FROM signed_records").fetchall()]
        versions = [tuple(int(part) for part in item["version"].split(".")) for item in rows if item["package"] == record["package"] and item["platform"] == record["platform"]]
        incoming = tuple(int(part) for part in record["version"].split("."))
        if versions and incoming <= max(versions):
            raise ValueError("package index version rollback or duplicate")''', "business_test": '''    ledger = PackageMirrorLedger(tmp_path / "mirror.sqlite")
    ledger.publish(identity, record)
    with pytest.raises(ValueError): ledger.publish(identity, dict(record, version="1.2.2"))
    ledger.close()''', "key": "package"},
    "ApprovalFlow": {"record_key": "f\"{record['request_id']}:{record['stage']}:{record['approver_id']}\"", "policy": "", "business_test": '''    ledger = ApprovalFlowLedger(tmp_path / "approvals.sqlite")
    first = dict(record, approver_id="alice")
    ledger.publish(identity, first)
    ledger.publish(identity, dict(record, approver_id="bob"))
    assert ledger.approval_quorum_met(record["request_id"], record["stage"], 2)
    with pytest.raises(ValueError): ledger.publish(identity, first)
    ledger.close()''', "key": "request_id"},
    "ClinicalConsent": {"record_key": "str(record['consent_id'])", "policy": "", "business_test": '''    ledger = ClinicalConsentLedger(tmp_path / "consents.sqlite")
    ledger.publish(identity, record)
    assert ledger.is_consent_active(record["consent_id"])
    ledger.revoke_consent(record["consent_id"])
    assert not ledger.is_consent_active(record["consent_id"])
    with pytest.raises(ValueError): ledger.publish(identity, dict(record, consent_id="consent-2"))
    ledger.close()''', "key": "consent_id"},
    "FleetPermit": {"record_key": "str(record['permit_id'])", "policy": "", "business_test": '''    assert verify_vehicle_permit(identity["signing_public"], record, sign_vehicle_permit(identity, record), now=record["valid_from"] + 1)
    assert not verify_vehicle_permit(identity["signing_public"], record, sign_vehicle_permit(identity, record), now=record["valid_until"] + 1)''', "key": "permit_id"},
}
for _app in APPS:
    _app.update(POLICIES.get(_app["name"], {}))

DISTINCTIONS = {
    "WebhookShield": "focuses on HTTP event delivery identifiers, nonce replay detection, and signed request bodies; it is not a network tunnel or general peer session protocol.",
    "MailGuard": "models MIME-like message metadata and per-message attachments; it is not clinical messaging or matter-scoped legal document exchange.",
    "SessionExchange": "models application-level client/server suite negotiation and transcript binding; it does not establish a gateway tunnel or protect telemetry.",
    "DataProvenance": "tracks general dataset/object lineage through chained digest checkpoints; it does not attest software builds or release artifacts.",
    "DesktopUpdateProof": "verifies desktop-client product/platform release manifests and downgrade policy; it is separate from staged firmware fleet rollout.",
    "PackageMirror": "verifies mirrored package-index entries and package version monotonicity; it does not attest build workers or software release provenance.",
    "ApprovalFlow": "implements multi-approver request-stage quorums; it is distinct from delegated policy-bundle approval and authorization decisions.",
    "ClinicalConsent": "stores synthetic subject-scoped permissions with cryptographically verified revocation; it does not exchange clinical messages.",
    "FleetPermit": "issues portable vehicle permits for offline signature and validity checks; it is unrelated to device enrollment or firmware delivery.",
}
for _app in APPS:
    if _app["name"] in DISTINCTIONS:
        _app["distinction"] = DISTINCTIONS[_app["name"]]

POLICIES["MailGuard"]["extra_validation"] = '''    names = [item.get("name") for item in normalized["attachments"] if isinstance(item, dict)]
    if len(names) != len(normalized["attachments"]) or len(names) != len(set(names)):
        raise ValueError("attachments must be objects with distinct names")'''
POLICIES["MailGuard"]["business_test"] = '''    with pytest.raises(ValueError): validate_mail_envelope(dict(record, attachments=[{"name":"same.txt"},{"name":"same.txt"}]))'''
POLICIES["SessionExchange"].update({
    "extra_validation": '''    suites = normalized["offered_suites"]
    if not isinstance(suites, list) or not suites or not all(isinstance(x, str) for x in suites) or len(suites) != len(set(suites)):
        raise ValueError("offered suites must be a non-empty list of unique strings")''',
    "extra_workflow": '''def negotiate_session_suite(record: dict, supported_suites: list[str]) -> str:
    offered = validate_session_offer(record)["offered_suites"]
    selected = next((suite for suite in offered if suite in supported_suites), None)
    if selected is None:
        raise ValueError("no mutually supported session suite")
    return selected''',
    "business_test": '''    assert negotiate_session_suite(record, ["ML-KEM-768+A256GCM"]) == "ML-KEM-768+A256GCM"
    with pytest.raises(ValueError): negotiate_session_suite(record, ["unsupported-suite"])''',
    "test_imports": "from {pkg}.workflow import negotiate_session_suite",
})
POLICIES["ApprovalFlow"].update({
    "extra_ledger": '''    def approval_quorum_met(self, request_id: str, stage: int, quorum: int, signer_keys: dict[str, object]) -> bool:
        if not isinstance(quorum, int) or quorum < 1:
            raise ValueError("quorum must be positive")
        rows = self._db.execute("SELECT body, signature FROM signed_records").fetchall()
        approvers = set()
        for body, signature in rows:
            item = json.loads(body)
            approver = item["approver_id"]
            if item["request_id"] != request_id or item["stage"] != stage or item["decision"] != "approve":
                continue
            public_key = signer_keys.get(approver)
            if public_key is not None and crypto.verify_document(bytes(signature), public_key, CONTEXT) == bytes(body):
                approvers.add(approver)
        return len(approvers) >= quorum''',
    "business_test": '''    ledger = ApprovalFlowLedger(tmp_path / "approvals.sqlite")
    first = dict(record, approver_id="alice")
    ledger.publish(identity, first)
    bob_identity = create_approval_request_identity()
    ledger.publish(bob_identity, dict(record, approver_id="bob"))
    assert ledger.approval_quorum_met(record["request_id"], record["stage"], 2, {"alice":identity["signing_public"],"bob":bob_identity["signing_public"]})
    with pytest.raises(ValueError): ledger.publish(identity, first)
    assert not ledger.approval_quorum_met(record["request_id"], record["stage"], 2, {"alice":identity["signing_public"]})
    ledger.close()''',
})
POLICIES["ClinicalConsent"].update({
    "extra_validation": '''    if not isinstance(normalized["scopes"], list) or not normalized["scopes"] or not all(isinstance(scope, str) and scope.strip() for scope in normalized["scopes"]):
        raise ValueError("consent requires non-empty string scopes")''',
    "extra_ledger": '''    def revoke_consent(self, consent_id: str) -> None:
        exists = self._db.execute("SELECT 1 FROM signed_records WHERE record_id=?", (consent_id,)).fetchone()
        if not exists:
            raise KeyError(consent_id)
        self._db.execute("INSERT OR IGNORE INTO revoked_consents(consent_id) VALUES(?)", (consent_id,))
        self._db.commit()
    def is_consent_active(self, consent_id: str, signing_public, now: int) -> bool:
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (consent_id,)).fetchone()
        if row is None:
            return False
        if self._db.execute("SELECT 1 FROM revoked_consents WHERE consent_id=?", (consent_id,)).fetchone():
            return False
        body, signature = bytes(row[0]), bytes(row[1])
        record = json.loads(body)
        return (crypto.verify_document(signature, signing_public, CONTEXT) == body
                and record["consented_at"] <= now < record["expires_at"])''',
    "business_test": '''    ledger = ClinicalConsentLedger(tmp_path / "consents.sqlite")
    ledger.publish(identity, record)
    assert ledger.is_consent_active(record["consent_id"], identity["signing_public"], record["consented_at"] + 1)
    ledger.revoke_consent(record["consent_id"])
    assert not ledger.is_consent_active(record["consent_id"], identity["signing_public"], record["consented_at"] + 1)
    ledger.close()''',
})
POLICIES["FleetPermit"].update({
    "verify_args": ", now: int | None = None",
    "verify_time_policy": '''    if now is None:
        now = int(__import__("time").time())
    if not isinstance(now, int) or not record.get("valid_from") <= now < record.get("valid_until"):
        return False''',
    "verify_test_args": ", now=record['valid_from'] + 1",
    "business_test": '''    signed_permit = sign_vehicle_permit(identity, record)
    assert verify_vehicle_permit(identity["signing_public"], record, signed_permit, now=record["valid_from"] + 1)
    assert not verify_vehicle_permit(identity["signing_public"], record, signed_permit, now=record["valid_until"] + 1)''',
})
for _app in APPS:
    _app.update(POLICIES.get(_app["name"], {}))

TASKS = [
    ("key provisioning", "create_{entity}_identity", "ML-DSA-65 signing and ML-KEM-768 transport key generation"),
    ("public-key serialization", "export_{entity}_public_key", "Versioned DER SubjectPublicKeyInfo encoding with purpose separation"),
    ("public-key loading", "load_{entity}_public_key", "Strict ML-DSA/ML-KEM public-key decoding and type validation"),
    ("business validation", "validate_{record}", "Domain-specific input and authorization preconditions"),
    ("canonical representation", "canonicalize_{record}", "Stable canonical JSON for signature input"),
    ("record signing", "sign_{record}", "Context-bound ML-DSA-65 signature over the canonical record"),
    ("record verification", "verify_{record}", "ML-DSA verification with tamper and context rejection"),
    ("confidential delivery", "seal_{record}_payload", "ML-KEM-768, HKDF-SHA-256, and AES-256-GCM envelope"),
    ("key rotation", "rotate_{entity}_identity", "Versioned signing and transport key rotation"),
    ("key revocation", "revoke_{entity}_identity", "Fail-closed key revocation and stale-version rejection"),
]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((content.rstrip("\r\n") + "\n").encode("utf-8"))


def crypto_source(app: dict, pqc: bool) -> str:
    slug, label = app["slug"], app["name"]
    if pqc:
        imports = "from cryptography.hazmat.primitives.asymmetric import mlkem, mldsa"
        gen_sign = "mldsa.MLDSA65PrivateKey.generate()"
        gen_kem = "mlkem.MLKEM768PrivateKey.generate()"
        sign_priv, sign_pub, kem_priv, kem_pub = "mldsa.MLDSA65PrivateKey", "mldsa.MLDSA65PublicKey", "mlkem.MLKEM768PrivateKey", "mlkem.MLKEM768PublicKey"
        sig_alg, kem_alg = "ML-DSA-65", "ML-KEM-768+HKDF-SHA256+AES-256-GCM"
        sign_call = "private.sign(context + b'\\x00' + payload)"
        verify_call = "public.verify(signature, context + b'\\x00' + payload)"
        seal_key = f"shared, enc = public.encapsulate(); key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'OPMB-600:{slug}:v1:' + context).derive(shared); wrapped = base64.b64encode(enc).decode()"
        open_key = (f"enc = base64.b64decode(obj['enc'], validate=True)\n"
                    "        if len(enc) != 1088:\n"
                    "            raise ValueError('invalid ML-KEM-768 ciphertext length')\n"
                    "        shared = private.decapsulate(enc)\n"
                    f"        key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'OPMB-600:{slug}:v1:' + context).derive(shared)")
        allowed = "{'v', 'alg', 'enc', 'nonce', 'ciphertext'}"
        envelope_fields = "'enc': wrapped, "
        key_check = ""
    else:
        imports = "from cryptography.hazmat.primitives.asymmetric import padding, rsa"
        gen_sign = "rsa.generate_private_key(public_exponent=65537, key_size=3072)"
        gen_kem = "rsa.generate_private_key(public_exponent=65537, key_size=3072)"
        sign_priv, sign_pub, kem_priv, kem_pub = "rsa.RSAPrivateKey", "rsa.RSAPublicKey", "rsa.RSAPrivateKey", "rsa.RSAPublicKey"
        sig_alg, kem_alg = "RSA-PSS-SHA256", "RSA-OAEP-SHA256+AES-256-GCM"
        sign_call = "private.sign(context + b'\\x00' + payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())"
        verify_call = "public.verify(signature, context + b'\\x00' + payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())"
        seal_key = "key = os.urandom(32); wrapped_bytes = public.encrypt(key, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=context)); wrapped = base64.b64encode(wrapped_bytes).decode()"
        open_key = "wrapped_bytes = base64.b64decode(obj['wrapped_key'], validate=True); key = private.decrypt(wrapped_bytes, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=context))"
        allowed = "{'v', 'alg', 'wrapped_key', 'nonce', 'ciphertext'}"
        envelope_fields = "'wrapped_key': wrapped, "
        key_check = "if len(key) != 32: raise ValueError('invalid content key')"
    return f'''"""{label} cryptographic primitives; {'FIPS 203/204' if pqc else 'classical RSA baseline'}."""
from __future__ import annotations
import base64, json, os
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
{imports}

VERSION = 1
SIGNATURE_ALGORITHM = "{sig_alg}"
ENVELOPE_ALGORITHM = "{kem_alg}"
SIGNING_PRIVATE = {sign_priv}
SIGNING_PUBLIC = {sign_pub}
TRANSPORT_PRIVATE = {kem_priv}
TRANSPORT_PUBLIC = {kem_pub}

def generate_signing_keypair():
    private = {gen_sign}
    return private, private.public_key()

def generate_transport_keypair():
    private = {gen_kem}
    return private, private.public_key()

def serialize_public_key(public, purpose: str) -> bytes:
    if not isinstance(public, (SIGNING_PUBLIC, TRANSPORT_PUBLIC)):
        raise ValueError("unsupported public-key type")
    expected = {{"signing": SIGNING_PUBLIC, "transport": TRANSPORT_PUBLIC}}.get(purpose)
    if expected is None or not isinstance(public, expected):
        raise ValueError("public-key algorithm does not match its purpose")
    der = public.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    return json.dumps({{"v": VERSION, "purpose": purpose, "key": base64.b64encode(der).decode()}}, sort_keys=True, separators=(",", ":")).encode()

def load_public_key(encoded: bytes, purpose: str):
    if not isinstance(encoded, bytes) or not encoded:
        raise ValueError("encoded public key must be non-empty bytes")
    try:
        obj = json.loads(encoded)
        if set(obj) != {{"v", "purpose", "key"}} or obj["v"] != VERSION or obj["purpose"] != purpose:
            raise ValueError("public-key purpose or version mismatch")
        der = base64.b64decode(obj["key"], validate=True)
        key = serialization.load_der_public_key(der)
    except (ValueError, TypeError, KeyError) as exc:
        raise ValueError("malformed or purpose-mismatched public key") from exc
    expected = {{"signing": SIGNING_PUBLIC, "transport": TRANSPORT_PUBLIC}}.get(purpose)
    if expected is None or not isinstance(key, expected):
        raise ValueError("public-key algorithm does not match its purpose")
    return key

def sign_document(payload: bytes, private, context: bytes) -> bytes:
    if not isinstance(payload, bytes) or not payload or not isinstance(context, bytes):
        raise ValueError("payload and byte context are required")
    if not isinstance(private, SIGNING_PRIVATE):
        raise ValueError("wrong signing private-key type")
    signature = {sign_call}
    return json.dumps({{"v": VERSION, "alg": SIGNATURE_ALGORITHM,
                       "payload": base64.b64encode(payload).decode(),
                       "signature": base64.b64encode(signature).decode()}},
                      sort_keys=True, separators=(",", ":")).encode()

def verify_document(envelope: bytes, public, context: bytes):
    if not isinstance(public, SIGNING_PUBLIC) or not isinstance(context, bytes):
        return None
    try:
        obj = json.loads(envelope)
        if set(obj) != {{"v", "alg", "payload", "signature"}} or obj["v"] != VERSION or obj["alg"] != SIGNATURE_ALGORITHM:
            return None
        payload = base64.b64decode(obj["payload"], validate=True)
        signature = base64.b64decode(obj["signature"], validate=True)
        {verify_call}
        return payload
    except (ValueError, TypeError, KeyError, InvalidSignature):
        return None

def seal_payload(plaintext: bytes, public, context: bytes) -> bytes:
    if not isinstance(plaintext, bytes) or not plaintext or not isinstance(context, bytes):
        raise ValueError("plaintext and byte context are required")
    if not isinstance(public, TRANSPORT_PUBLIC):
        raise ValueError("wrong transport public-key type")
    {seal_key}
    nonce = os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, context)
    return json.dumps({{"v": VERSION, "alg": ENVELOPE_ALGORITHM, {envelope_fields}"nonce": base64.b64encode(nonce).decode(), "ciphertext": base64.b64encode(ciphertext).decode()}}, sort_keys=True, separators=(",", ":")).encode()

def open_payload(envelope: bytes, private, context: bytes) -> bytes:
    if not isinstance(private, TRANSPORT_PRIVATE) or not isinstance(context, bytes):
        raise ValueError("wrong transport private-key type or context")
    try:
        obj = json.loads(envelope)
        if set(obj) != {allowed} or obj["v"] != VERSION or obj["alg"] != ENVELOPE_ALGORITHM:
            raise ValueError("unsupported envelope")
        nonce = base64.b64decode(obj["nonce"], validate=True)
        ciphertext = base64.b64decode(obj["ciphertext"], validate=True)
        if len(nonce) != 12:
            raise ValueError("invalid nonce length")
        {open_key}
{('        ' + key_check) if key_check else ''}
        return AESGCM(key).decrypt(nonce, ciphertext, context)
    except (ValueError, TypeError, KeyError, InvalidTag) as exc:
        raise ValueError("invalid, modified, or context-mismatched envelope") from exc

class KeyRegistry:
    """In-memory versioned identities with final revocation semantics."""
    def __init__(self):
        self._entries = {{}}
    def provision(self, key_id: str):
        if not isinstance(key_id, str) or not key_id.strip() or key_id in self._entries:
            raise ValueError("invalid or duplicate key identifier")
        signing_private, signing_public = generate_signing_keypair()
        transport_private, transport_public = generate_transport_keypair()
        entry = {{"version": 1, "status": "active", "signing_private": signing_private,
                 "signing_public": signing_public, "transport_private": transport_private,
                 "transport_public": transport_public}}
        self._entries[key_id] = entry
        return self._public_view(entry)
    def rotate(self, key_id: str):
        old = self._entries.get(key_id)
        if not old or old["status"] != "active":
            raise ValueError("key is unavailable or revoked")
        signing_private, signing_public = generate_signing_keypair()
        transport_private, transport_public = generate_transport_keypair()
        entry = {{"version": old["version"] + 1, "status": "active",
                 "signing_private": signing_private, "signing_public": signing_public,
                 "transport_private": transport_private, "transport_public": transport_public}}
        self._entries[key_id] = entry
        return self._public_view(entry)
    def revoke(self, key_id: str):
        entry = self._entries.get(key_id)
        if not entry or entry["status"] != "active":
            raise ValueError("key is unavailable or already revoked")
        self._entries[key_id] = {{"version": entry["version"], "status": "revoked"}}
    def get_active(self, key_id: str, version: int):
        entry = self._entries.get(key_id)
        if not entry or entry["status"] != "active" or entry["version"] != version:
            raise ValueError("unknown, revoked, or stale key version")
        return dict(entry)
    @staticmethod
    def _public_view(entry):
        return {{"version": entry["version"],
                "signing_public": serialize_public_key(entry["signing_public"], "signing"),
                "transport_public": serialize_public_key(entry["transport_public"], "transport")}}
'''


def workflow_source(app: dict) -> str:
    slug, entity, record = app["slug"], app["entity"], app["entity"]
    required = repr(app["required"])
    model_name = "".join(part.capitalize() for part in app["entity"].split("_")) + "Record"
    def annotation(value):
        if isinstance(value, bool): return "bool"
        if isinstance(value, int): return "int"
        if isinstance(value, float): return "float"
        if isinstance(value, list): return "list[Any]"
        if isinstance(value, dict): return "dict[str, Any]"
        return "str"
    model_fields = "\n".join(f"    {key}: {annotation(value)}" for key, value in app["sample"].items())
    rules = "\n".join("        " + line for line in app["rules"])
    context = f"opmb-600:{slug}:v1"
    id_field = app.get("key", "record_id")
    record_key_expr = app.get("record_key", f"str(record[{id_field!r}])")
    state_policy = app.get("policy", "        return") or "        return"
    extra_validation = app.get("extra_validation", "")
    extra_workflow = app.get("extra_workflow", "")
    extra_ledger = app.get("extra_ledger", "")
    verify_time_policy = app.get("verify_time_policy", "")
    verify_args = app.get("verify_args", "")
    verify_test_args = app.get("verify_test_args", "")
    sample_json = json.dumps(app["sample"], sort_keys=True, separators=(",", ":"))
    return f'''"""{app['name']} domain workflows for {app['title'].lower()}."""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any, TypedDict
from . import crypto

class {model_name}(TypedDict):
{model_fields}

CONTEXT = b"{context}"
REQUIRED_FIELDS = {required}

def create_{entity}_identity():
    sign_private, sign_public = crypto.generate_signing_keypair()
    transport_private, transport_public = crypto.generate_transport_keypair()
    return {{"signing_private": sign_private, "signing_public": sign_public,
            "transport_private": transport_private, "transport_public": transport_public}}

def export_{entity}_public_key(public_key, purpose: str) -> bytes:
    expected = "signing" if purpose == "signing" else "transport" if purpose == "transport" else None
    if expected is None:
        raise ValueError("purpose must be signing or transport")
    return crypto.serialize_public_key(public_key, expected)

def load_{entity}_public_key(encoded: bytes, purpose: str):
    return crypto.load_public_key(encoded, purpose)

def validate_{record}(record: {model_name}) -> {model_name}:
    if not isinstance(record, dict) or not all(field in record for field in REQUIRED_FIELDS):
        raise ValueError("record is missing required {app['entity']} fields")
    if set(record) != set(REQUIRED_FIELDS):
        raise ValueError("record contains unsupported {app['entity']} fields")
    if any(record[field] is None or record[field] == "" for field in REQUIRED_FIELDS):
        raise ValueError("required {app['entity']} fields cannot be empty")
    try:
{rules}
    except (TypeError, KeyError, IndexError) as exc:
        raise ValueError("malformed {app['entity']} domain value") from exc
    # Round-trip through JSON rejects non-serializable or ambiguous application data.
    try:
        normalized = json.loads(json.dumps(record, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError("record must contain finite JSON values") from exc
{extra_validation}
    return normalized

def canonicalize_{record}(record: {model_name}) -> bytes:
    normalized = validate_{record}(record)
    return json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sign_{record}(identity: dict, record: {model_name}) -> bytes:
    payload = canonicalize_{record}(record)
    return crypto.sign_document(payload, identity["signing_private"], CONTEXT)

def verify_{record}(public_key, record: {model_name}, envelope: bytes{verify_args}) -> bool:
    try:
        expected = canonicalize_{record}(record)
    except (ValueError, TypeError, KeyError):
        return False
{verify_time_policy}
    return crypto.verify_document(envelope, public_key, CONTEXT) == expected

def seal_{record}_payload(public_key, payload: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.seal_payload(payload, public_key, CONTEXT + b":" + record_id.encode())

def open_{record}_payload(private_key, envelope: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip():
        raise ValueError("record identifier is required for envelope binding")
    return crypto.open_payload(envelope, private_key, CONTEXT + b":" + record_id.encode())

def rotate_{entity}_identity(registry: crypto.KeyRegistry, identity_id: str):
    return registry.rotate(identity_id)

def revoke_{entity}_identity(registry: crypto.KeyRegistry, identity_id: str):
    registry.revoke(identity_id)
{extra_workflow}

class {app['name']}Ledger:
    """SQLite-backed append-only ledger for validated, signed {app['plural']}."""
    def __init__(self, database: str | Path = ":memory:"):
        self._db = sqlite3.connect(str(database))
        self._db.execute("CREATE TABLE IF NOT EXISTS signed_records (record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
        self._db.execute("CREATE TABLE IF NOT EXISTS revoked_consents (consent_id TEXT PRIMARY KEY)")
        self._db.commit()
    def _enforce_policy(self, record: {model_name}) -> None:
{state_policy}
    def publish(self, identity: dict, record: {model_name}) -> bytes:
        normalized = validate_{record}(record)
        record_id = {record_key_expr}
        if record_id is None or not str(record_id).strip():
            raise ValueError("{id_field} must identify the record")
        self._enforce_policy(normalized)
        body = canonicalize_{record}(normalized)
        signature = crypto.sign_document(body, identity["signing_private"], CONTEXT)
        try:
            self._db.execute("INSERT INTO signed_records(record_id, body, signature) VALUES(?,?,?)", (str(record_id), body, signature))
            self._db.commit()
        except sqlite3.IntegrityError as exc:
            raise ValueError("duplicate {app['entity']} identifier") from exc
        return signature
    def fetch(self, record_id: str):
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return json.loads(row[0]), bytes(row[1])
    def close(self):
        self._db.close()
{extra_ledger}

def run_{slug}_workflow(identity: dict, record: {model_name}, ledger: {app['name']}Ledger | None = None) -> dict:
    normalized = validate_{record}(record)
    signature = ledger.publish(identity, normalized) if ledger is not None else sign_{record}(identity, normalized)
    return {{"record": normalized, "signature": signature, "context": CONTEXT.decode()}}

def example_record() -> {model_name}:
    return json.loads({sample_json!r})
'''


def cli_source(app: dict) -> str:
    slug, entity = app["slug"], app["entity"]
    return f'''"""Command-line entry point for {app['name']}."""
import argparse
import json
import sys
from pathlib import Path
from .workflow import create_{entity}_identity, run_{slug}_workflow

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate and sign one {app['entity']} JSON record")
    parser.add_argument("record", nargs="?", help="JSON file; reads stdin when omitted")
    args = parser.parse_args(argv)
    try:
        raw = Path(args.record).read_text(encoding="utf-8") if args.record else sys.stdin.read()
        record = json.loads(raw)
        result = run_{slug}_workflow(create_{entity}_identity(), record)
        print(json.dumps({{"record": result["record"], "signature": result["signature"].decode(), "context": result["context"]}}, sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"{app['name']}: {{exc}}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
'''


def tests_source(app: dict, pqc: bool, task_start: int) -> str:
    pkg, entity = app["slug"], app["entity"]
    package_name = f"{pkg}_pqc" if pqc else pkg
    package_path = "migrated_reference" if pqc else "src"
    record_key_expr = app.get("record_key", f"str(record[{app.get('key', 'record_id')!r}])")
    test_imports = app.get("test_imports", "").format(pkg=pkg)
    business_test = app.get("business_test", "")
    verify_test_args = app.get("verify_test_args", "")
    test_prefix = "pqc" if pqc else "original"
    expected_class = "crypto.mldsa.MLDSA65PrivateKey" if pqc else "crypto.rsa.RSAPrivateKey"
    # RSA classes are exposed via `rsa` import only in the classical implementation.
    if not pqc:
        expected_class = "crypto.rsa.RSAPrivateKey"
    return f'''"""{app['name']} {test_prefix} application and cryptography contract tests."""
import json
import os
import subprocess
import sys
from pathlib import Path
import pytest
from {pkg} import crypto
from {pkg}.workflow import (create_{entity}_identity, export_{entity}_public_key,
    load_{entity}_public_key, validate_{entity}, canonicalize_{entity}, sign_{entity},
    verify_{entity}, seal_{entity}_payload, open_{entity}_payload,
    rotate_{entity}_identity, revoke_{entity}_identity, {app['name']}Ledger,
    run_{pkg}_workflow, example_record)
{test_imports}

def test_task_{task_start:04d}_identity_creation_separates_key_purposes():
    identity = create_{entity}_identity()
    assert isinstance(identity["signing_private"], {expected_class})
    assert isinstance(identity["transport_private"], crypto.TRANSPORT_PRIVATE)
    assert identity["signing_public"] is not identity["transport_public"]

def test_task_{task_start+1:04d}_public_key_serialization_round_trips_by_purpose():
    identity = create_{entity}_identity()
    sign_der = export_{entity}_public_key(identity["signing_public"], "signing")
    kem_der = export_{entity}_public_key(identity["transport_public"], "transport")
    assert load_{entity}_public_key(sign_der, "signing") == identity["signing_public"]
    assert load_{entity}_public_key(kem_der, "transport") == identity["transport_public"]
    with pytest.raises(ValueError): load_{entity}_public_key(sign_der, "transport")
    with pytest.raises(ValueError): load_{entity}_public_key(b"truncated", "signing")

def test_task_{task_start+2:04d}_key_purpose_and_encoding_inputs_are_strict():
    identity = create_{entity}_identity()
    with pytest.raises(ValueError): export_{entity}_public_key(identity["signing_public"], "encryption")
    with pytest.raises(ValueError): load_{entity}_public_key(b"", "signing")
    with pytest.raises(ValueError): load_{entity}_public_key(b"not DER", "unknown")

def test_task_{task_start+3:04d}_domain_validation_enforces_required_fields_and_policy():
    record = example_record()
    assert validate_{entity}(record) == record
    with pytest.raises(ValueError): validate_{entity}({{k:v for k,v in record.items() if k != {app['required'][0]!r}}})
    with pytest.raises(ValueError): validate_{entity}(dict(record, unexpected_field="downgrade"))
    invalid = dict(record)
    invalid[{app['required'][0]!r}] = None
    # Domain rules reject invalid values while accepting the canonical valid example.
    with pytest.raises((ValueError, TypeError)): canonicalize_{entity}(invalid)

def test_task_{task_start+4:04d}_canonicalization_is_deterministic():
    record = example_record()
    reversed_record = dict(reversed(list(record.items())))
    assert canonicalize_{entity}(record) == canonicalize_{entity}(reversed_record)
    assert json.loads(canonicalize_{entity}(record)) == record

def test_task_{task_start+5:04d}_signature_binds_record_and_application_context():
    identity = create_{entity}_identity()
    record = example_record()
    signed = sign_{entity}(identity, record)
    assert verify_{entity}(identity["signing_public"], record, signed{verify_test_args})
    changed = dict(record)
    changed[{app['required'][-1]!r}] = "changed"
    assert not verify_{entity}(identity["signing_public"], changed, signed{verify_test_args})
    assert crypto.verify_document(signed, identity["signing_public"], b"wrong-context") is None

def test_task_{task_start+6:04d}_signature_rejects_wrong_key_and_tampered_envelope():
    identity = create_{entity}_identity()
    other = create_{entity}_identity()
    record = example_record()
    signed = sign_{entity}(identity, record)
    assert not verify_{entity}(other["signing_public"], record, signed{verify_test_args})
    obj = json.loads(signed)
    obj["payload"] = "eA=="
    assert not verify_{entity}(identity["signing_public"], record, json.dumps(obj).encode(){verify_test_args})
    obj = json.loads(signed)
    obj["alg"] = "RSA-PSS-SHA256" if crypto.SIGNATURE_ALGORITHM != "RSA-PSS-SHA256" else "UNSUPPORTED"
    assert not verify_{entity}(identity["signing_public"], record, json.dumps(obj).encode(){verify_test_args})
    obj = json.loads(signed)
    obj["v"] = 99
    assert not verify_{entity}(identity["signing_public"], record, json.dumps(obj).encode(){verify_test_args})
    assert not verify_{entity}(identity["signing_public"], record, b"not-json"{verify_test_args})

def test_task_{task_start+7:04d}_hybrid_envelope_authenticates_context_and_recipient():
    identity = create_{entity}_identity()
    other = create_{entity}_identity()
    record_id = str(example_record()[{app.get('key','record_id')!r}])
    envelope = seal_{entity}_payload(identity["transport_public"], b"protected application payload", record_id)
    assert open_{entity}_payload(identity["transport_private"], envelope, record_id) == b"protected application payload"
    with pytest.raises(ValueError): open_{entity}_payload(identity["transport_private"], envelope, record_id + "-wrong")
    with pytest.raises(ValueError): open_{entity}_payload(other["transport_private"], envelope, record_id)
    obj = json.loads(envelope)
    obj["ciphertext"] = obj["ciphertext"][:-4] + "AAAA"
    with pytest.raises(ValueError): open_{entity}_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)
    obj = json.loads(envelope)
    obj["alg"] = "UNSUPPORTED"
    with pytest.raises(ValueError): open_{entity}_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)
    obj = json.loads(envelope)
    obj["v"] = 99
    with pytest.raises(ValueError): open_{entity}_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)

def test_task_{task_start+8:04d}_rotation_retires_old_version_and_generates_new_keys():
    registry = crypto.KeyRegistry()
    first = registry.provision("identity-a")
    second = rotate_{entity}_identity(registry, "identity-a")
    assert first["version"] == 1 and second["version"] == 2
    with pytest.raises(ValueError): registry.get_active("identity-a", 1)
    active = registry.get_active("identity-a", 2)
    assert active["signing_private"].public_key() != crypto.load_public_key(first["signing_public"], "signing")

def test_task_{task_start+9:04d}_revocation_and_append_only_application_workflow(tmp_path):
    registry = crypto.KeyRegistry()
    registry.provision("identity-b")
    revoke_{entity}_identity(registry, "identity-b")
    with pytest.raises(ValueError): registry.get_active("identity-b", 1)
    identity = create_{entity}_identity()
    database = tmp_path / "records.sqlite"
    ledger = {app['name']}Ledger(database)
    record = example_record()
    result = run_{pkg}_workflow(identity, record, ledger)
    stored, signature = ledger.fetch({record_key_expr})
    assert stored == record and verify_{entity}(identity["signing_public"], stored, signature{verify_test_args})
    with pytest.raises(ValueError): ledger.publish(identity, record)
    ledger.close()
    reopened = {app['name']}Ledger(database)
    stored_again, signature_again = reopened.fetch({record_key_expr})
    assert stored_again == record and verify_{entity}(identity["signing_public"], stored_again, signature_again{verify_test_args})
    reopened.close()
    environment = os.environ.copy()
    source_root = Path(__file__).resolve().parents[1] / {package_path!r}
    environment["PYTHONPATH"] = str(source_root) + os.pathsep + environment.get("PYTHONPATH", "")
    completed = subprocess.run([sys.executable, "-m", {package_name!r}], cwd=Path(__file__).resolve().parents[1],
                               input=json.dumps(record), text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, env=environment, check=False)
    assert completed.returncode == 0, completed.stderr
    cli_result = json.loads(completed.stdout)
    assert cli_result["record"] == record and cli_result["context"]
{business_test}
'''


def task_json(app: dict, index: int, task_id: int, test_file: str) -> dict:
    record = app["entity"]
    objective = TASKS[index][0]
    function = TASKS[index][1].format(entity=record, record=record)
    target = TASKS[index][2]
    migration_family = ["key provisioning and serialization", "key encoding compatibility", "key encoding compatibility", "input validation", "protocol serialization", "post-quantum signatures", "signature verification", "hybrid key establishment", "key rotation", "key revocation"][index]
    classic = "RSA-3072 PSS; RSA-OAEP with AES-256-GCM"
    return {
        "task_id": f"OPMB-{task_id:04d}", "repository_id": app["repo"],
        "repository_name": app["slug"], "application_domain": app["domain"],
        "repository_version": "1.0.0", "language": "Python", "classical_algorithm": classic,
        "cryptographic_operation": ["key generation", "public-key serialization", "public-key parsing", "record validation", "canonical JSON encoding", "record signing", "signature verification", "hybrid authenticated encryption", "key rotation", "key revocation"][index],
        "source_files": [f"src/{app['slug']}/workflow.py", f"src/{app['slug']}/crypto.py"],
        "function_names": [function], "migration_family": migration_family,
        "migration_target": target,
        "migration_objective": f"Within {app['name']}'s {app['title'].lower()} workflow, migrate {objective} from the RSA baseline to {target}, preserving the application contract and rejecting invalid or downgraded inputs.",
        "preconditions": [f"The original {app['name']} application tests pass.", "The application record satisfies the documented domain policy.", "No real personal, financial, or production data is used."],
        "expected_behavior": [f"Preserve {app['name']}'s domain workflow and validation rules.", "Reject malformed, wrong-purpose, stale, tampered, or context-mismatched cryptographic inputs.", "Keep signing and transport keys distinct."],
        "migration_requirements": ["Use the pinned cryptography provider and standardized FIPS 203 ML-KEM-768 / FIPS 204 ML-DSA-65 APIs.", "Use ML-KEM only for key establishment; derive AES-256-GCM content keys with HKDF-SHA-256.", "Do not silently fall back to classical cryptography."],
        "original_tests": [f"tests/test_{app['slug']}.py::test_task_{task_id:04d}_{['identity_creation_separates_key_purposes','public_key_serialization_round_trips_by_purpose','key_purpose_and_encoding_inputs_are_strict','domain_validation_enforces_required_fields_and_policy','canonicalization_is_deterministic','signature_binds_record_and_application_context','signature_rejects_wrong_key_and_tampered_envelope','hybrid_envelope_authenticates_context_and_recipient','rotation_retires_old_version_and_generates_new_keys','revocation_and_append_only_application_workflow'][index]}"],
        "migration_tests": [f"tests/test_{app['slug']}_pqc.py::test_task_{task_id:04d}_{['identity_creation_separates_key_purposes','public_key_serialization_round_trips_by_purpose','key_purpose_and_encoding_inputs_are_strict','domain_validation_enforces_required_fields_and_policy','canonicalization_is_deterministic','signature_binds_record_and_application_context','signature_rejects_wrong_key_and_tampered_envelope','hybrid_envelope_authenticates_context_and_recipient','rotation_retires_old_version_and_generates_new_keys','revocation_and_append_only_application_workflow'][index]}"],
        "verification_procedure": [f"Run `python -m pytest tests/test_{app['slug']}.py -q` from `{app['repo']}` using the pinned root environment.", f"Run `python -m pytest tests/test_{app['slug']}_pqc.py -q` from `{app['repo']}` using the pinned root environment.", "Review the linked application evidence for actual exit codes and per-suite counts."],
        "difficulty": ["medium", "medium", "medium", "easy", "medium", "medium", "hard", "hard", "hard", "hard"][index],
        "original_build_status": "pending", "original_test_status": "pending", "reference_patch_status": "pending",
        "cryptographic_verification_status": "pending", "validation_status": "candidate",
        "known_limitations": ["Synthetic in-memory key registry; persistent private-key custody is outside this benchmark application.", "Candidate task only; independent review and acceptance are pending."],
        "created_by": "OPMB-600-team-a", "task_path": f"benchmark/repositories/{app['repo']}/tasks/OPMB-{task_id:04d}",
        "reference_path": f"benchmark/repositories/{app['repo']}/migrated_reference/{app['slug']}_pqc",
        "original_test_evidence": f"reports/evidence/{app['repo']}/test-results.json",
        "reference_test_evidence": f"reports/evidence/{app['repo']}/test-results.json",
    }


def build_app(app: dict, task_start: int) -> list[dict]:
    base = ROOT / "benchmark" / "repositories" / app["repo"]
    pkg, slug = app["slug"], app["slug"]
    pqc_pkg = f"{slug}_pqc"
    write(base / "src" / pkg / "__init__.py", f'"""{app["name"]} original application."""\nfrom .workflow import *\n')
    write(base / "src" / pkg / "crypto.py", crypto_source(app, False))
    write(base / "src" / pkg / "workflow.py", workflow_source(app))
    write(base / "src" / pkg / "__main__.py", cli_source(app))
    write(base / "migrated_reference" / pqc_pkg / "__init__.py", f'"""{app["name"]} FIPS 203/204 reference migration."""\nfrom .workflow import *\n')
    write(base / "migrated_reference" / pqc_pkg / "crypto.py", crypto_source(app, True))
    write(base / "migrated_reference" / pqc_pkg / "workflow.py", workflow_source(app))
    write(base / "migrated_reference" / pqc_pkg / "__main__.py", cli_source(app))
    (base / "tests").mkdir(parents=True, exist_ok=True)
    write(base / "tests" / f"test_{slug}.py", tests_source(app, False, task_start))
    # Use the same domain contract tests against a separate PQC package.
    pqc_tests = tests_source(app, True, task_start).replace(f"from {pkg} import crypto", f"from {pqc_pkg} import crypto").replace(f"from {pkg}.workflow import", f"from {pqc_pkg}.workflow import")
    write(base / "tests" / f"test_{slug}_pqc.py", pqc_tests)
    (base / "tasks").mkdir(exist_ok=True)
    task_docs = []
    for index, (objective, template, target) in enumerate(TASKS):
        task_id = task_start + index
        task = task_json(app, index, task_id, f"tests/test_{slug}_pqc.py")
        task_dir = base / "tasks" / f"OPMB-{task_id:04d}"
        write(task_dir / "task.json", json.dumps(task, indent=2, ensure_ascii=False))
        write(task_dir / "requirements.md", f"# OPMB-{task_id:04d} requirements\n\n{task['migration_objective']}\n\n- Preserve domain validation and the existing call shape.\n- Use the standardized target named in task metadata.\n- Reject malformed data, wrong key purpose, tampering, stale keys, and context mismatch as applicable.\n- Keep signing and key-establishment keys separate.\n")
        write(task_dir / "expected_behavior.md", f"# OPMB-{task_id:04d} expected behavior\n\n- The {app['name']} {app['entity'].replace('_',' ')} workflow succeeds for valid input.\n- The migrated function `{template.format(entity=app['entity'], record=app['entity'])}` uses {target}.\n- Invalid domain records and invalid cryptographic data fail closed without a classical fallback.\n")
        write(task_dir / "verification.md", f"# OPMB-{task_id:04d} verification\n\n- Original: `python -m pytest tests/test_{slug}.py -q` from `{app['repo']}`.\n- Reference: `python -m pytest tests/test_{slug}_pqc.py -q` from `{app['repo']}`.\n- Task test: `test_task_{task_id:04d}_...` in each suite.\n- Evidence: `reports/evidence/{app['repo']}/test-results.json`.\n- Status remains candidate until independent review.\n")
        task_docs.append(task)
    distinction = app.get("distinction", "The workflow has its own application-specific records, validation policy, and context-bound cryptographic lifecycle.")
    write(base / "README.md", f"# {app['name']}\n\nControlled synthetic application for OPMB-600. {app['title']}. Classical baseline: RSA-3072 PSS and RSA-OAEP/AES-256-GCM. The independent reference package uses FIPS 204 ML-DSA-65 and FIPS 203 ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM.\n\n**Scope distinction:** {distinction}\n\nOriginal source is in `src/{pkg}/`; the migration reference is in `migrated_reference/{pqc_pkg}/`. Both implement the domain-specific `{app['entity'].replace('_',' ')}` model and workflow, strict field validation, a persistent SQLite signed-record ledger, a runnable CLI, key serialization, and key lifecycle.\n\nFrom this directory, run the original CLI with `PYTHONPATH=src python -m {pkg} [record.json]` on POSIX or `$env:PYTHONPATH='src'; python -m {pkg} [record.json]` in PowerShell. For the separate reference CLI, set `PYTHONPATH=migrated_reference` (PowerShell: `$env:PYTHONPATH='migrated_reference'`) and run `python -m {pqc_pkg} [record.json]`. Omit the file to read JSON from standard input. Run the two test suites with `python -m pytest tests/test_{slug}.py -q` and `python -m pytest tests/test_{slug}_pqc.py -q`. This synthetic benchmark is not a production system.\n")
    write(base / "requirements.txt", "cryptography==50.0.2\n")
    write(base / "pyproject.toml", f'''[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "opmb-{slug}"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = ["cryptography==50.0.2"]

[tool.pytest.ini_options]
pythonpath = ["src", "migrated_reference"]

[tool.setuptools.packages.find]
where = ["src", "migrated_reference"]
include = ["{slug}*", "{slug}_pqc*"]
''')
    return task_docs


def main() -> None:
    all_tasks = []
    for index, app in enumerate(APPS):
        start = START_TASK + 10 * index
        all_tasks.extend(build_app(app, start))
    contribution = ROOT / "reports" / "contributions" / "part4" / "team-a"
    repos_manifest = [{"repository_id": a["repo"], "name": a["name"], "application_domain": a["domain"], "path": f"benchmark/repositories/{a['repo']}", "purpose": a["title"], "status": "candidate", "task_ids": [f"OPMB-{START_TASK + 10*i + j:04d}" for j in range(10)]} for i, a in enumerate(APPS)]
    write(contribution / "repository_manifest.json", json.dumps({"repositories": repos_manifest}, indent=2, ensure_ascii=False))
    write(contribution / "task_manifest.json", json.dumps({"tasks": all_tasks}, indent=2, ensure_ascii=False))
    rows_io = io.StringIO()
    rows_writer = csv.writer(rows_io, lineterminator="\n")
    rows_writer.writerow(["repository_id","application","name","domain","scope_distinction","source","reference","original_tests","pqc_tests","tasks"])
    for i, a in enumerate(APPS):
        rows_writer.writerow([a["repo"], a["name"], a["slug"], a["domain"], a.get("distinction", "Application-specific record and workflow."), f"src/{a['slug']}", f"migrated_reference/{a['slug']}_pqc", f"tests/test_{a['slug']}.py", f"tests/test_{a['slug']}_pqc.py", 10])
    write(contribution / "application_inventory.csv", rows_io.getvalue())
    task_rows_io = io.StringIO()
    task_writer = csv.writer(task_rows_io, lineterminator="\n")
    task_writer.writerow(["task_id","repository_id","objective","source","function","original_test","reference_test","status"])
    for task in all_tasks:
        task_writer.writerow([task["task_id"], task["repository_id"], task["migration_objective"], task["source_files"][0], task["function_names"][0], task["original_tests"][0], task["migration_tests"][0], task["validation_status"]])
    write(contribution / "task_inventory.csv", task_rows_io.getvalue())
    write(contribution / "test_summary.json", json.dumps({"status": "not_run", "environment": None, "repositories": [{"repository_id": a["repo"], "original": {"status": "not_run"}, "pqc_reference": {"status": "not_run"}, "warnings": [], "errors": []} for a in APPS]}, indent=2))
    write(contribution / "crypto_verification_report.md", "# Cryptographic verification\n\nStatus: **pending execution**. The reference packages use the pinned `cryptography==50.0.2` API for FIPS 203 ML-KEM-768 and FIPS 204 ML-DSA-65. The suites exercise key-purpose separation, DER serialization, context-bound signatures, hybrid KEM/HKDF/AES-256-GCM envelopes, tamper rejection, wrong-key rejection, and versioned rotation/revocation. Do not treat this design statement as a test result.\n")
    write(contribution / "known_issues.md", "# Known issues\n\n- Tasks remain candidates pending independent review.\n- Key registries are in-memory; durable private-key custody and production deployment are outside this synthetic benchmark.\n- Test and cryptographic verification status remains pending until execution evidence is captured.\n")
    write(contribution / "implementation_report.md", "# Team A implementation report\n\nImplementation inventory is generated from the allocated application and task definitions. Test results and cryptographic verification will be populated only from actual executions.\n")
    write(contribution / "INTEGRATION_NOTES.md", "# Integration notes\n\n- Contribution owns REPO-018 through REPO-032 and OPMB-0171 through OPMB-0320 only.\n- Shared canonical manifests, README, catalogue, schemas, dependencies, and validation scripts are intentionally untouched.\n- No task is accepted; integration owner can merge the contribution manifests after review.\n")
    print(f"Generated {len(APPS)} applications and {len(all_tasks)} task definitions.")


if __name__ == "__main__":
    main()
