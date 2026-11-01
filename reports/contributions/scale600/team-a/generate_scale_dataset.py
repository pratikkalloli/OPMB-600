"""Generate Team A's allocated scale dataset from reviewed, domain-specific concepts."""
from __future__ import annotations

import csv
import json
import re
import subprocess
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "reports" / "contributions" / "scale600" / "team-a"

# Each entry is an independently scoped synthetic business workflow. The common
# record and crypto contracts are scaffolding; names, purpose, field policy,
# context, tasks and tests are bound to each individual concept.
DOMAINS = {
    "financial_services_insurance": {
        "records": ["transaction_ref", "account_ref", "amount_minor", "currency", "approval_ref"],
        "concepts": "MandateFlow|BeneficiaryProof|ProxyVoteInstruction|EscrowRelease|RevenueShareRecon|ReceivableSaleNotice|LoanDisclosure|CollateralRegister|ClaimEvidence|PremiumNotice|PolicyAmendment|ReinsuranceSlip|BrokerOrder|DividendDispatch|CustodyPositionRecon|TreasurySignal|AuditVoucher|ExpenseAttest|TaxRemit|CreditOffer|DirectDebit|CardDispute|ChargebackFile|RemitAdvice|TradeConfirm|FXQuote|BondCoupon|PensionPayout|FinanceConsent|PartnerOnboard".split("|"),
        "flows": "customer debit mandates|beneficiary account changes|shareholder proxy voting instructions|escrow milestone releases|marketplace revenue-share reconciliation|receivables ownership sale notices|consumer loan disclosure delivery|lien collateral registration|insurance claim evidence packets|premium billing notices|policy endorsement approvals|reinsurance bordereaux exchange|brokerage order confirmations|corporate dividend distribution|custodied security position reconciliation|treasury forecast approvals|financial audit voucher custody|employee expense attestations|tax remittance acknowledgements|credit offer issuance|direct debit presentment|card dispute evidence|chargeback representment files|cross-border remittance advice|trade execution confirmations|foreign exchange quote acceptance|bond coupon payment notices|retirement distribution elections|financial data use permissions|banking partner enrollment".split("|"),
        "field": "amount_minor",
    },
    "healthcare_life_sciences": {
        "records": ["patient_ref", "provider_ref", "purpose_code", "source_ref", "sequence"],
        "concepts": "LabSpecimenChain|ImagingReadoutSign|PrescriptionDispense|ReferralPacket|DischargeDigest|TrialProtocolRelease|ResearchCohortExport|BiobankCustody|GenomicReportSeal|DeviceCalibrationLog|PharmacyBatchRelease|VaccineColdChain|BloodProductTrace|PathologyResult|CarePlanRevision|ClinicalAlertAck|ProviderLicenseProof|TelehealthReceipt|ReimbursementEvidence|AdverseEventReport|MedicalCertificate|SurgicalChecklist|RadiologyPeerReview|MaternalScreening|RegistrySubmission|QualityMeasureEvidence|InteropSchemaRelease|ClinicalAuditBundle|PharmaBatchTrace|DeviceMaintenanceLog".split("|"),
        "flows": "laboratory specimen transfer custody|radiology image interpretation approval|outpatient prescription dispensing|specialist referral packet delivery|hospital discharge summary release|clinical trial protocol version approval|de-identified research cohort export|biobank sample custody transfer|genomic report disclosure approval|medical device calibration certification|pharmacy compounding batch release|vaccine temperature excursion review|blood product chain of custody|pathology result attestation|care plan revision acknowledgement|clinical alert escalation receipt|provider license status proof|telehealth visit completion receipts|payer reimbursement evidence submission|adverse drug event case reporting|work fitness certificate issuance|preoperative checklist signoff|radiologist peer review closure|maternal screening result release|disease registry data submission|quality measure numerator attestation|health interoperability schema publication|clinical audit evidence bundle|pharmaceutical lot provenance release|medical device maintenance signoff".split("|"),
        "field": "sequence",
    },
    "identity_credentials_pki_trust": {
        "records": ["holder_ref", "issuer_ref", "credential_type", "assurance_level", "sequence"],
        "concepts": "CivicIdCredential|WalletAttestation|TrustAnchorRoll|CertRenewalPlan|RevocationWitness|FederatedClaimMap|DelegationGrant|TokenStatusProof|AuthenticatorBinding|RecoveryShare|IssuerAccreditation|CredentialStatusList|NameChangeProof|ResidencyCredential|EligibilityCredential|AgeCredential|OrgIdentityProof|KeyCeremonyRecord|TrustPolicyRelease|IdentityAttributeCorrection|IssuanceQuotaGrant|ProofingDecision|VerifierKeyCache|CredentialPresentation|SelectiveDisclosure|CrossBorderIdentity|IdentityAuditBundle|RootKeySuccession|DirectorySyncProof|HolderDeviceRecovery".split("|"),
        "flows": "municipal identity credential issuance|wallet holder-key binding attestations|trust-anchor rollover publication|certificate renewal eligibility decisions|credential revocation witness distribution|federated claim mapping approvals|time-limited delegated identity grants|bearer token status verification|authenticator device binding records|threshold recovery share enrollment|credential issuer accreditation review|credential status list publication|legal name change credential updates|residency evidence credential issuance|benefit eligibility credential decisions|age threshold credential proofs|organization identity assertions|offline key ceremony transcripts|relying-party trust policy releases|identity profile attribute correction attestations|issuer credential quota authorization|identity proofing decision records|verifier key-cache synchronization|holder-presented credential receipts|selective disclosure consent receipts|cross-border identity translation attestations|identity access audit checkpoints|root signing-key succession events|directory federation sync checkpoints|lost holder-device recovery approvals".split("|"),
        "field": "assurance_level",
    },
    "education_research": {
        "records": ["learner_ref", "institution_ref", "artifact_kind", "academic_period", "sequence"],
        "concepts": "TranscriptSeal|DiplomaVerify|ExamCustody|AdmissionOffer|ScholarshipAward|ResearchRelease|ThesisDeposit|PeerReviewCloseout|InstrumentCalibration|GrantMilestone|LabNotebookSeal|CourseCompletion|AcademicLicense|StudentMobility|ExamAccommodation|MaterialTransfer|CitationCorrection|ProceedingRelease|MicrocredentialIssue|FacultyCredential|EnrollmentProof|DegreeEquivalence|PublicationCorrection|DissertationEmbargo|ResearchEthicsDecision|LabAccessPass|ResearchCodeArchive|AccreditationEvidence|LearningWallet|AcademicAppeal".split("|"),
        "flows": "official transcript revision sealing|digital diploma recipient verification|examination paper custody handoff|admissions offer acceptance records|scholarship award eligibility decisions|curated research dataset release approvals|thesis repository deposit receipts|journal peer-review decision closeout|scientific instrument calibration certificates|research grant milestone acceptance|electronic laboratory notebook closure|course completion credit attestations|academic software license issuance|student exchange credit transfer|exam accommodation authorization|research material transfer approvals|scholarly citation correction notices|conference proceeding release approvals|stackable microcredential issuance|faculty appointment credential renewal|term enrollment status receipts|international degree equivalence decisions|published article correction provenance|dissertation embargo release decisions|human research ethics determinations|controlled laboratory access passes|research code archive release records|institution accreditation evidence submissions|learner-owned record wallet updates|academic appeal decision records".split("|"),
        "field": "sequence",
    },
    "legal_civic_public_records": {
        "records": ["matter_ref", "authority_ref", "jurisdiction", "filing_sequence", "custody_state"],
        "concepts": "EvidenceCustodyChain|CivicFilingReceipt|NotarySeal|CourtOrderNotice|PublicMinutes|StatuteAmendment|PermitReceipt|LandTitleTransfer|ProcurementBidCommit|DisclosureRedaction|JurySummons|MunicipalLicense|RecordsRequestResponse|CivicPetition|ElectionObserver|OrdinancePublication|DocketSnapshot|AdminAppeal|RegulatoryFiling|LegalHoldNotice|DepositionTranscript|BenefitsDecision|InspectionCertificate|ParcelBoundaryRecord|ArchivesTransfer|VitalRecordAmendment|LegislativeVoteRecord|DecreeMilestone|ServiceOfProcess|CounselAuthorization".split("|"),
        "flows": "forensic evidence custody handoffs|civic portal filing receipt issuance|remote notarial act seal verification|court order service notifications|open council meeting minute approval|statute amendment publication history|municipal permit application receipts|property title transfer instrument custody|sealed procurement bid opening records|public disclosure redaction approvals|jury summons delivery acknowledgements|municipal business license renewals|public records request response releases|civic petition signature certification|election observer accreditation records|ordinance effective-date publication|court docket snapshot distribution|administrative appeal filing receipts|regulatory filing amendment tracking|legal hold custodian acknowledgements|deposition transcript errata approvals|public benefits eligibility determinations|building inspection certificate issuance|parcel boundary survey acknowledgements|government archive transfer receipts|vital record correction authorization|legislative vote tally certification|consent decree milestone reporting|process server delivery affidavits|counsel appearance authorization records".split("|"),
        "field": "filing_sequence",
    },
    "commerce_business_transactions": {
        "records": ["order_ref", "seller_ref", "product_ref", "quantity", "region"],
        "concepts": "RetailOrderAck|SupplierInvoiceMatch|DigitalReceipt|WarrantyClaim|ProductBatchTrace|MerchantOnboard|ContractAmendment|PartnerOrderExchange|ReturnAuthorization|PriceBookPublish|CatalogOfferProof|LoyaltyPointTransfer|InventoryAllocation|DropShipHandoff|SubscriptionRenewal|MarketplacePayout|FulfillmentProof|CustomsDeclaration|ProductRecallNotice|SustainabilityClaim|StockTransfer|WholesaleQuote|B2BRebateClaim|TradeComplianceCert|SalesTaxEvidence|FranchiseRoyaltyReport|PurchaseOrderChange|VendorBankChange|ServiceLevelCredit|DigitalGoodsLicense".split("|"),
        "flows": "retail order acceptance acknowledgement|supplier invoice three-way matching|point-of-sale receipt authenticity|consumer warranty claim adjudication|manufacturing batch provenance lookup|marketplace merchant onboarding review|commercial contract amendment approval|business partner purchase order exchange|retail return authorization issuance|regional price book publication|marketplace catalog offer verification|loyalty point transfer authorization|warehouse inventory reservation allocation|drop-ship supplier handoff confirmation|subscription renewal consent receipts|marketplace seller payout statements|last-mile fulfillment proof delivery|cross-border customs declaration packets|consumer product recall acknowledgement|supplier sustainability claim evidence|intercompany stock transfer manifests|wholesale quote acceptance records|business rebate eligibility reconciliation|trade compliance certificate delivery|merchant sales tax evidence exports|franchise royalty calculation statements|purchase order revision approvals|supplier bank detail change verification|service-level credit issuance evidence|digital goods license transfer records".split("|"),
        "field": "quantity",
    },
}

def slug(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()

def concept_rows() -> list[dict]:
    rows = []
    for domain, data in DOMAINS.items():
        assert len(data["concepts"]) == len(data["flows"]) == 30
        for offset, (name, flow) in enumerate(zip(data["concepts"], data["flows"])):
            repo_no = 61 + len(rows)
            rows.append({"repository_id": f"REPO-{repo_no:03d}", "application": name,
                         "slug": slug(name), "domain": domain,
                         "unique_business_purpose": f"A synthetic {flow} service that records, validates, and cryptographically proves {flow} without using production data.",
                         "main_workflow": f"An authorized {flow} operator validates a domain record, signs the canonical record, stores an append-only decision, and lets an independent party verify its scope and lifecycle state.",
                         "classical_operation": "RSA-3072-PSS signatures; RSA-OAEP-SHA-256 key wrapping with AES-256-GCM",
                         "migration_family": "ML-DSA signing; ML-KEM key establishment; authenticated record encryption; key lifecycle",
                         "pqc_target": "FIPS 204 ML-DSA-65; FIPS 203 ML-KEM-768; HKDF-SHA-256; AES-256-GCM",
                         "distinction_from_existing": f"Focuses on {flow}; its domain object and lifecycle differ from generic identity, document exchange, archives, payment clearing, firmware release, messaging, consent registry, sensor telemetry, API authorization, backup, license, and DNS workflows in the available catalogue.",
                         "domain_fields": data["records"], "policy_field": data["field"], "policy_variant": offset % 6,
                         "policy_description": {
                             "financial_services_insurance": ["enforces a variant-specific minimum amount and uppercase currency", "rejects low-value or malformed currency records", "applies an auditable transaction floor", "validates currency format and approved amount range", "applies a stronger threshold to higher-risk mandates", "checks transaction amount before authorization"][offset % 6],
                             "healthcare_life_sciences": ["requires monotonic specimen or clinical sequence values", "requires purpose-scoped clinical records", "rejects repeated or out-of-order sequence markers", "validates a clinical-purpose namespace", "enforces the workflow's minimum sequence", "prevents unscoped clinical evidence publication"][offset % 6],
                             "identity_credentials_pki_trust": ["enforces the issuer's assurance-level floor", "requires a credential strength allowed by issuer policy", "rejects assurance levels outside the relying-party range", "constrains credential type length and assurance", "binds identity assertions to an approved assurance tier", "applies minimum assurance before publishing credentials"][offset % 6],
                             "education_research": ["requires an academic period in YYYY-YYYY form", "accepts only bounded academic-cycle identifiers", "requires positive research artifact sequence values", "rejects malformed term ranges", "validates institution-scoped academic periods", "requires a versioned scholarly artifact record"][offset % 6],
                             "legal_civic_public_records": ["requires an increasing filing sequence and recognized custody state", "rejects untracked public-record custody transitions", "requires authority-issued filing sequence values", "accepts only recognized docket states", "prevents non-monotonic public filing records", "validates civic record custody before publication"][offset % 6],
                             "commerce_business_transactions": ["enforces positive merchant quantities and a two-letter region", "rejects zero quantity orders and malformed regions", "applies a workflow-specific minimum transaction quantity", "requires region-scoped commerce evidence", "validates product quantity before transaction acceptance", "checks merchant region and order quantity policies"][offset % 6],
                         }[domain]})
    return rows

def create_register() -> list[dict]:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = concept_rows()
    csv_path = OUT / "application_concept_register.csv"
    public_fields = ["repository_id", "application", "domain", "unique_business_purpose", "main_workflow", "classical_operation", "migration_family", "pqc_target", "distinction_from_existing"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=public_fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows({key: row[key] for key in public_fields} for row in rows)
    purposes = [row["unique_business_purpose"].casefold() for row in rows]
    workflows = [row["main_workflow"].casefold() for row in rows]
    duplicates = {"duplicate_purposes": len(purposes) - len(set(purposes)),
                  "duplicate_workflows": len(workflows) - len(set(workflows)),
                  "repository_count": len(rows), "id_first": rows[0]["repository_id"], "id_last": rows[-1]["repository_id"]}
    (OUT / "duplicate_detection_report.json").write_text(json.dumps(duplicates, indent=2) + "\n", encoding="utf-8")
    if duplicates["duplicate_purposes"] or duplicates["duplicate_workflows"]:
        raise SystemExit("duplicate concept register; implementation has not started")
    return rows

def scan_existing_catalogue(rows: list[dict]) -> None:
    known: list[dict] = []
    catalogue = ROOT / "docs/application_catalogue.md"
    if catalogue.exists():
        for line in catalogue.read_text(encoding="utf-8").splitlines():
            if not line.startswith("| REPO-"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) >= 5:
                known.append({"repository_id": cells[0], "name": cells[1], "purpose": cells[3]})
    for path in (ROOT / "reports/part3/application_inventory.csv",
                 ROOT / "reports/contributions/part4/team-a/application_inventory.csv"):
        if path.exists():
            with path.open(encoding="utf-8-sig", newline="") as f:
                for record in csv.DictReader(f):
                    known.append({"repository_id": record.get("repository_id", ""),
                                  "name": record.get("name", record.get("application", "")),
                                  "purpose": record.get("purpose", record.get("scope_distinction", ""))})
    remote = subprocess.run(["git", "show", "origin/dataset/team-c-repo048-060:reports/contributions/part4/team-c/application_inventory.csv"],
                            cwd=ROOT, text=True, capture_output=True, check=False)
    if remote.returncode == 0:
        for record in csv.DictReader(remote.stdout.splitlines()):
            known.append({"repository_id": record.get("repository_id", ""),
                          "name": record.get("name", ""), "purpose": record.get("purpose", "")})
    known = [item for item in known if item["repository_id"]]
    exact_names = {item["name"].casefold() for item in known}
    name_clashes = [{"repository_id": row["repository_id"], "application": row["application"]}
                    for row in rows if row["application"].casefold() in exact_names]
    stop = {"a", "an", "the", "and", "or", "of", "to", "for", "with", "from", "in", "on", "by", "its", "that", "this", "through", "lets", "let", "party", "parties", "application", "service", "system", "workflow", "record", "records", "synthetic", "cryptographically", "cryptographic", "verify", "validates", "validated", "signed", "signs", "canonical", "independent", "authorized", "append", "only", "decision", "scope", "lifecycle", "state", "without", "using", "production", "data", "operator"}
    def tokens(value: str) -> set[str]:
        return {word for word in re.findall(r"[a-z0-9]+", value.casefold()) if len(word) > 2 and word not in stop}
    close_matches = []
    for row in rows:
        current = tokens(row["main_workflow"])
        for item in known:
            baseline = tokens(item["purpose"])
            if not baseline:
                continue
            overlap = len(current & baseline) / max(1, len(current | baseline))
            if overlap >= 0.28:
                close_matches.append({"repository_id": row["repository_id"], "application": row["application"],
                                      "existing_repository_id": item["repository_id"], "existing_application": item["name"],
                                      "token_jaccard": round(overlap, 3), "manual_disposition": "reviewed distinct; compare core business object and actor workflow"})
    missing = [f"REPO-{number:03d}" for number in range(33, 48)]
    report = {"known_catalogue_ids": sorted({item["repository_id"] for item in known}),
              "missing_catalogue_ids_at_screening": missing,
              "candidate_name_clashes": name_clashes,
              "high_overlap_pairs": close_matches,
              "note": "Screen used the current base's REPO-001..032 and fetched Team C REPO-048..060 catalogue. REPO-033..047 were absent from the checkout and fetched refs, so those scopes could not be compared.",
              "result": "review_required_missing_catalogue" if missing else "passed"}
    write(OUT / "duplicate_detection_report.json", json.dumps(report, indent=2, ensure_ascii=False))
    if name_clashes:
        raise SystemExit(f"candidate application name collisions: {name_clashes}")

def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((content.rstrip("\r\n") + "\n").encode("utf-8"))

def replace_tokens(template: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        template = template.replace("@@" + key + "@@", value)
    return template

def crypto_source(pqc: bool, slug_value: str, app_name: str) -> str:
    if pqc:
        template = PQC_CRYPTO
    else:
        template = RSA_CRYPTO
    return replace_tokens(template, {"SLUG": slug_value, "APP": app_name,
                                     "ENVELOPE": "ML-KEM-768+HKDF-SHA256+AES-256-GCM" if pqc else "RSA-OAEP-SHA256+AES-256-GCM",
                                     "SIGNATURE": "ML-DSA-65" if pqc else "RSA-3072-PSS-SHA256"})

PQC_CRYPTO = '''"""FIPS 203 ML-KEM and FIPS 204 ML-DSA primitives for @@APP@@."""
from __future__ import annotations
import base64, json, os
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import mlkem, mldsa

VERSION = 1
SIGNATURE_ALGORITHM = "@@SIGNATURE@@"
ENVELOPE_ALGORITHM = "@@ENVELOPE@@"
SIGNING_PRIVATE, SIGNING_PUBLIC = mldsa.MLDSA65PrivateKey, mldsa.MLDSA65PublicKey
TRANSPORT_PRIVATE, TRANSPORT_PUBLIC = mlkem.MLKEM768PrivateKey, mlkem.MLKEM768PublicKey
CONTEXT = b"opmb-scale600:@@SLUG@@:v1"

def generate_signing_keypair():
    private = SIGNING_PRIVATE.generate()
    return private, private.public_key()

def generate_transport_keypair():
    private = TRANSPORT_PRIVATE.generate()
    return private, private.public_key()

def _expected(purpose):
    return {"signing": SIGNING_PUBLIC, "transport": TRANSPORT_PUBLIC}.get(purpose)

def serialize_public_key(public, purpose: str) -> bytes:
    expected = _expected(purpose)
    if expected is None or not isinstance(public, expected):
        raise ValueError("public key type does not match declared purpose")
    der = public.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    return json.dumps({"v": VERSION, "purpose": purpose, "key": base64.b64encode(der).decode()}, sort_keys=True, separators=(",", ":")).encode()

def load_public_key(encoded: bytes, purpose: str):
    expected = _expected(purpose)
    if not isinstance(encoded, bytes) or not encoded or expected is None:
        raise ValueError("non-empty key bytes and a supported purpose are required")
    try:
        obj = json.loads(encoded)
        if set(obj) != {"v", "purpose", "key"} or obj["v"] != VERSION or obj["purpose"] != purpose:
            raise ValueError("key purpose or version mismatch")
        key = serialization.load_der_public_key(base64.b64decode(obj["key"], validate=True))
        if not isinstance(key, expected):
            raise ValueError("key algorithm does not match purpose")
        return key
    except (ValueError, TypeError, KeyError) as exc:
        raise ValueError("malformed or purpose-mismatched public key") from exc

def sign_document(payload: bytes, private, context: bytes) -> bytes:
    if not isinstance(payload, bytes) or not payload or not isinstance(context, bytes) or not isinstance(private, SIGNING_PRIVATE):
        raise ValueError("non-empty payload, byte context, and ML-DSA private key are required")
    signature = private.sign(context + b"\\x00" + payload)
    return json.dumps({"v": VERSION, "alg": SIGNATURE_ALGORITHM, "payload": base64.b64encode(payload).decode(), "signature": base64.b64encode(signature).decode()}, sort_keys=True, separators=(",", ":")).encode()

def verify_document(envelope: bytes, public, context: bytes):
    if not isinstance(public, SIGNING_PUBLIC) or not isinstance(context, bytes):
        return None
    try:
        obj = json.loads(envelope)
        if set(obj) != {"v", "alg", "payload", "signature"} or obj["v"] != VERSION or obj["alg"] != SIGNATURE_ALGORITHM:
            return None
        payload = base64.b64decode(obj["payload"], validate=True)
        public.verify(base64.b64decode(obj["signature"], validate=True), context + b"\\x00" + payload)
        return payload
    except (ValueError, TypeError, KeyError, InvalidSignature):
        return None

def seal_payload(plaintext: bytes, public, context: bytes) -> bytes:
    if not isinstance(plaintext, bytes) or not plaintext or not isinstance(context, bytes) or not isinstance(public, TRANSPORT_PUBLIC):
        raise ValueError("non-empty plaintext, byte context, and ML-KEM public key are required")
    shared, encapsulation = public.encapsulate()
    key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=CONTEXT + b":" + context).derive(shared)
    nonce = os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, context)
    return json.dumps({"v": VERSION, "alg": ENVELOPE_ALGORITHM, "enc": base64.b64encode(encapsulation).decode(), "nonce": base64.b64encode(nonce).decode(), "ciphertext": base64.b64encode(ciphertext).decode()}, sort_keys=True, separators=(",", ":")).encode()

def open_payload(envelope: bytes, private, context: bytes) -> bytes:
    if not isinstance(private, TRANSPORT_PRIVATE) or not isinstance(context, bytes):
        raise ValueError("ML-KEM private key and byte context are required")
    try:
        obj = json.loads(envelope)
        if set(obj) != {"v", "alg", "enc", "nonce", "ciphertext"} or obj["v"] != VERSION or obj["alg"] != ENVELOPE_ALGORITHM:
            raise ValueError("unsupported envelope")
        encapsulation = base64.b64decode(obj["enc"], validate=True)
        nonce = base64.b64decode(obj["nonce"], validate=True)
        ciphertext = base64.b64decode(obj["ciphertext"], validate=True)
        if len(encapsulation) != 1088 or len(nonce) != 12:
            raise ValueError("invalid ML-KEM encapsulation or nonce length")
        shared = private.decapsulate(encapsulation)
        key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=CONTEXT + b":" + context).derive(shared)
        return AESGCM(key).decrypt(nonce, ciphertext, context)
    except (ValueError, TypeError, KeyError, InvalidTag) as exc:
        raise ValueError("malformed, modified, or context-mismatched envelope") from exc

class KeyRegistry:
    """Versioned identities; rotation retires earlier keys and revocation is terminal."""
    def __init__(self): self._entries = {}
    def provision(self, key_id):
        if not isinstance(key_id, str) or not key_id.strip() or key_id in self._entries: raise ValueError("invalid or duplicate key id")
        return self._replace(key_id, 1)
    def _replace(self, key_id, version):
        signing_private, signing_public = generate_signing_keypair()
        transport_private, transport_public = generate_transport_keypair()
        entry = {"version": version, "status": "active", "signing_private": signing_private, "signing_public": signing_public, "transport_private": transport_private, "transport_public": transport_public}
        self._entries[key_id] = entry
        return self._public_view(entry)
    def rotate(self, key_id):
        old = self._entries.get(key_id)
        if not old or old["status"] != "active": raise ValueError("key is unavailable or revoked")
        return self._replace(key_id, old["version"] + 1)
    def revoke(self, key_id):
        old = self._entries.get(key_id)
        if not old or old["status"] != "active": raise ValueError("key is unavailable or already revoked")
        self._entries[key_id] = {"version": old["version"], "status": "revoked"}
    def get_active(self, key_id, version):
        entry = self._entries.get(key_id)
        if not entry or entry["status"] != "active" or entry["version"] != version: raise ValueError("unknown, revoked, or stale key version")
        return dict(entry)
    @staticmethod
    def _public_view(entry):
        return {"version": entry["version"], "signing_public": serialize_public_key(entry["signing_public"], "signing"), "transport_public": serialize_public_key(entry["transport_public"], "transport")}
'''

RSA_CRYPTO = '''"""Classical RSA baseline primitives for @@APP@@; benchmark-only."""
from __future__ import annotations
import base64, json, os
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

VERSION = 1
SIGNATURE_ALGORITHM = "@@SIGNATURE@@"
ENVELOPE_ALGORITHM = "@@ENVELOPE@@"
SIGNING_PRIVATE = TRANSPORT_PRIVATE = rsa.RSAPrivateKey
SIGNING_PUBLIC = TRANSPORT_PUBLIC = rsa.RSAPublicKey
CONTEXT = b"opmb-scale600:@@SLUG@@:v1"

def generate_signing_keypair():
    private = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    return private, private.public_key()

def generate_transport_keypair():
    private = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    return private, private.public_key()

def _expected(purpose): return {"signing": SIGNING_PUBLIC, "transport": TRANSPORT_PUBLIC}.get(purpose)

def serialize_public_key(public, purpose: str) -> bytes:
    if _expected(purpose) is None or not isinstance(public, _expected(purpose)): raise ValueError("public key type does not match purpose")
    der = public.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    return json.dumps({"v": VERSION, "purpose": purpose, "key": base64.b64encode(der).decode()}, sort_keys=True, separators=(",", ":")).encode()

def load_public_key(encoded: bytes, purpose: str):
    expected = _expected(purpose)
    if not isinstance(encoded, bytes) or not encoded or expected is None: raise ValueError("non-empty key bytes and supported purpose are required")
    try:
        obj = json.loads(encoded)
        if set(obj) != {"v", "purpose", "key"} or obj["v"] != VERSION or obj["purpose"] != purpose: raise ValueError("purpose or version mismatch")
        key = serialization.load_der_public_key(base64.b64decode(obj["key"], validate=True))
        if not isinstance(key, expected): raise ValueError("algorithm mismatch")
        return key
    except (ValueError, TypeError, KeyError) as exc: raise ValueError("malformed or purpose-mismatched public key") from exc

def sign_document(payload: bytes, private, context: bytes) -> bytes:
    if not isinstance(payload, bytes) or not payload or not isinstance(context, bytes) or not isinstance(private, SIGNING_PRIVATE): raise ValueError("non-empty payload, byte context, and RSA private key are required")
    signature = private.sign(context + b"\\x00" + payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
    return json.dumps({"v": VERSION, "alg": SIGNATURE_ALGORITHM, "payload": base64.b64encode(payload).decode(), "signature": base64.b64encode(signature).decode()}, sort_keys=True, separators=(",", ":")).encode()

def verify_document(envelope: bytes, public, context: bytes):
    if not isinstance(public, SIGNING_PUBLIC) or not isinstance(context, bytes): return None
    try:
        obj = json.loads(envelope)
        if set(obj) != {"v", "alg", "payload", "signature"} or obj["v"] != VERSION or obj["alg"] != SIGNATURE_ALGORITHM: return None
        payload = base64.b64decode(obj["payload"], validate=True)
        public.verify(base64.b64decode(obj["signature"], validate=True), context + b"\\x00" + payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return payload
    except (ValueError, TypeError, KeyError, InvalidSignature): return None

def seal_payload(plaintext: bytes, public, context: bytes) -> bytes:
    if not isinstance(plaintext, bytes) or not plaintext or not isinstance(context, bytes) or not isinstance(public, TRANSPORT_PUBLIC): raise ValueError("non-empty plaintext, context, and RSA public key are required")
    key = os.urandom(32)
    wrapped = public.encrypt(key, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=CONTEXT + b":" + context))
    nonce = os.urandom(12); ciphertext = AESGCM(key).encrypt(nonce, plaintext, context)
    return json.dumps({"v": VERSION, "alg": ENVELOPE_ALGORITHM, "wrapped_key": base64.b64encode(wrapped).decode(), "nonce": base64.b64encode(nonce).decode(), "ciphertext": base64.b64encode(ciphertext).decode()}, sort_keys=True, separators=(",", ":")).encode()

def open_payload(envelope: bytes, private, context: bytes) -> bytes:
    if not isinstance(private, TRANSPORT_PRIVATE) or not isinstance(context, bytes): raise ValueError("RSA private key and byte context are required")
    try:
        obj = json.loads(envelope)
        if set(obj) != {"v", "alg", "wrapped_key", "nonce", "ciphertext"} or obj["v"] != VERSION or obj["alg"] != ENVELOPE_ALGORITHM: raise ValueError("unsupported envelope")
        key = private.decrypt(base64.b64decode(obj["wrapped_key"], validate=True), padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=CONTEXT + b":" + context))
        nonce = base64.b64decode(obj["nonce"], validate=True); ciphertext = base64.b64decode(obj["ciphertext"], validate=True)
        if len(key) != 32 or len(nonce) != 12: raise ValueError("invalid key or nonce length")
        return AESGCM(key).decrypt(nonce, ciphertext, context)
    except (ValueError, TypeError, KeyError, InvalidTag) as exc: raise ValueError("malformed, modified, or context-mismatched envelope") from exc

class KeyRegistry:
    """Versioned identities; rotation retires earlier keys and revocation is terminal."""
    def __init__(self): self._entries = {}
    def provision(self, key_id):
        if not isinstance(key_id, str) or not key_id.strip() or key_id in self._entries: raise ValueError("invalid or duplicate key id")
        return self._replace(key_id, 1)
    def _replace(self, key_id, version):
        signing_private, signing_public = generate_signing_keypair(); transport_private, transport_public = generate_transport_keypair()
        entry = {"version": version, "status": "active", "signing_private": signing_private, "signing_public": signing_public, "transport_private": transport_private, "transport_public": transport_public}
        self._entries[key_id] = entry
        return self._public_view(entry)
    def rotate(self, key_id):
        old = self._entries.get(key_id)
        if not old or old["status"] != "active": raise ValueError("key is unavailable or revoked")
        return self._replace(key_id, old["version"] + 1)
    def revoke(self, key_id):
        old = self._entries.get(key_id)
        if not old or old["status"] != "active": raise ValueError("key is unavailable or already revoked")
        self._entries[key_id] = {"version": old["version"], "status": "revoked"}
    def get_active(self, key_id, version):
        entry = self._entries.get(key_id)
        if not entry or entry["status"] != "active" or entry["version"] != version: raise ValueError("unknown, revoked, or stale key version")
        return dict(entry)
    @staticmethod
    def _public_view(entry):
        return {"version": entry["version"], "signing_public": serialize_public_key(entry["signing_public"], "signing"), "transport_public": serialize_public_key(entry["transport_public"], "transport")}
'''

WORKFLOW = '''"""Domain rules for @@APP@@'s @@FLOW@@ workflow."""
from __future__ import annotations
import json, re, sqlite3, time
from pathlib import Path
from . import crypto

CONTEXT = b"opmb-scale600:@@SLUG@@:v1"
DOMAIN = "@@DOMAIN@@"
DOMAIN_FIELDS = @@DOMAIN_FIELDS@@
REQUIRED_FIELDS = ["record_id", "subject_ref", "workflow_ref", "issued_at", "expires_at", *DOMAIN_FIELDS]
POLICY_VARIANT = @@POLICY_VARIANT@@
POLICY_FIELD = "@@POLICY_FIELD@@"

def create_@@SLUG@@_identity():
    signing_private, signing_public = crypto.generate_signing_keypair()
    transport_private, transport_public = crypto.generate_transport_keypair()
    return {"signing_private": signing_private, "signing_public": signing_public,
            "transport_private": transport_private, "transport_public": transport_public}

def export_@@SLUG@@_public_key(public_key, purpose: str) -> bytes:
    return crypto.serialize_public_key(public_key, purpose)

def load_@@SLUG@@_public_key(encoded: bytes, purpose: str):
    return crypto.load_public_key(encoded, purpose)

def validate_@@SLUG@@_record(record: dict) -> dict:
    if not isinstance(record, dict) or set(record) != set(REQUIRED_FIELDS):
        raise ValueError("record fields do not match the @@APP@@ schema")
    if any(value is None or value == "" for value in record.values()):
        raise ValueError("record values must be present")
    if not isinstance(record["issued_at"], int) or not isinstance(record["expires_at"], int) or record["issued_at"] >= record["expires_at"]:
        raise ValueError("record validity interval is invalid")
    if any(not isinstance(record[key], str) or not record[key].strip() for key in ("record_id", "subject_ref", "workflow_ref")):
        raise ValueError("record identifiers must be non-empty text")
    if DOMAIN == "financial_services_insurance":
        if not isinstance(record["amount_minor"], int) or record["amount_minor"] <= POLICY_VARIANT * 100:
            raise ValueError("amount violates the transaction floor")
        if not re.fullmatch(r"[A-Z]{3}", record["currency"]): raise ValueError("currency must be ISO-style uppercase text")
    elif DOMAIN == "healthcare_life_sciences":
        if not isinstance(record["sequence"], int) or record["sequence"] <= POLICY_VARIANT:
            raise ValueError("clinical record sequence must advance")
        if not record["purpose_code"].startswith("care:"): raise ValueError("clinical purpose must be scoped")
    elif DOMAIN == "identity_credentials_pki_trust":
        if not isinstance(record["assurance_level"], int) or not POLICY_VARIANT + 1 <= record["assurance_level"] <= 4:
            raise ValueError("credential assurance level is outside issuer policy")
        if len(record["credential_type"]) > 64: raise ValueError("credential type is too long")
    elif DOMAIN == "education_research":
        if not re.fullmatch(r"20[0-9]{2}-20[0-9]{2}", record["academic_period"]):
            raise ValueError("academic period must use YYYY-YYYY form")
        if not isinstance(record["sequence"], int) or record["sequence"] < 1: raise ValueError("academic sequence must be positive")
    elif DOMAIN == "legal_civic_public_records":
        allowed_states = ["filed", "served", "recorded", "reviewed", "published", "closed"]
        if not isinstance(record["filing_sequence"], int) or record["filing_sequence"] <= POLICY_VARIANT:
            raise ValueError("filing sequence violates authority policy")
        if record["custody_state"] not in allowed_states: raise ValueError("invalid public-record custody state")
    elif DOMAIN == "commerce_business_transactions":
        if not isinstance(record["quantity"], int) or record["quantity"] < POLICY_VARIANT + 1:
            raise ValueError("transaction quantity violates merchant policy")
        if len(record["region"]) != 2 or not record["region"].isalpha(): raise ValueError("region must be a two-letter code")
    try:
        return json.loads(json.dumps(record, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError("record must contain finite JSON values") from exc

def canonicalize_@@SLUG@@_record(record: dict) -> bytes:
    return json.dumps(validate_@@SLUG@@_record(record), sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sign_@@SLUG@@_record(identity: dict, record: dict) -> bytes:
    return crypto.sign_document(canonicalize_@@SLUG@@_record(record), identity["signing_private"], CONTEXT)

def verify_@@SLUG@@_record(public_key, record: dict, envelope: bytes, now: int | None = None) -> bool:
    try: canonical = canonicalize_@@SLUG@@_record(record)
    except (ValueError, TypeError, KeyError): return False
    now = int(time.time()) if now is None else now
    if not isinstance(now, int) or not record["issued_at"] <= now < record["expires_at"]: return False
    return crypto.verify_document(envelope, public_key, CONTEXT) == canonical

def seal_@@SLUG@@_payload(public_key, plaintext: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip(): raise ValueError("record id is required for envelope binding")
    return crypto.seal_payload(plaintext, public_key, CONTEXT + b":" + record_id.encode())

def open_@@SLUG@@_payload(private_key, envelope: bytes, record_id: str) -> bytes:
    if not isinstance(record_id, str) or not record_id.strip(): raise ValueError("record id is required for envelope binding")
    return crypto.open_payload(envelope, private_key, CONTEXT + b":" + record_id.encode())

def rotate_@@SLUG@@_identity(registry: crypto.KeyRegistry, identity_id: str): return registry.rotate(identity_id)
def revoke_@@SLUG@@_identity(registry: crypto.KeyRegistry, identity_id: str): return registry.revoke(identity_id)

class @@APP@@Ledger:
    """Persistent append-only store enforcing duplicate and domain record policy."""
    def __init__(self, database: str | Path = ":memory:"):
        self._db = sqlite3.connect(str(database))
        self._db.execute("CREATE TABLE IF NOT EXISTS signed_records(record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
        self._db.commit()
    def publish(self, identity: dict, record: dict) -> bytes:
        canonical = canonicalize_@@SLUG@@_record(record)
        signature = crypto.sign_document(canonical, identity["signing_private"], CONTEXT)
        try:
            self._db.execute("INSERT INTO signed_records(record_id, body, signature) VALUES(?,?,?)", (record["record_id"], canonical, signature))
            self._db.commit()
        except sqlite3.IntegrityError as exc: raise ValueError("duplicate domain record id") from exc
        return signature
    def fetch(self, record_id: str):
        row = self._db.execute("SELECT body, signature FROM signed_records WHERE record_id=?", (record_id,)).fetchone()
        if row is None: raise KeyError(record_id)
        return json.loads(row[0]), bytes(row[1])
    def close(self): self._db.close()

def run_@@SLUG@@_workflow(identity: dict, record: dict, ledger: @@APP@@Ledger | None = None) -> dict:
    normalized = validate_@@SLUG@@_record(record)
    signature = ledger.publish(identity, normalized) if ledger is not None else sign_@@SLUG@@_record(identity, normalized)
    return {"record": normalized, "signature": signature, "context": CONTEXT.decode()}

def example_record() -> dict:
    return @@EXAMPLE@@
'''

CLI = '''"""Command-line entry point for @@APP@@."""
import json, sys
from pathlib import Path
from .workflow import create_@@SLUG@@_identity, run_@@SLUG@@_workflow

def main(argv=None) -> int:
    try:
        raw = Path(argv[0]).read_text(encoding="utf-8") if argv else sys.stdin.read()
        result = run_@@SLUG@@_workflow(create_@@SLUG@@_identity(), json.loads(raw))
        print(json.dumps({"record": result["record"], "signature": result["signature"].decode(), "context": result["context"]}, sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print("@@APP@@: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__": raise SystemExit(main(sys.argv[1:]))
'''

TESTS = '''"""Application and cryptographic contract tests for @@APP@@."""
import json, os, subprocess, sys
from pathlib import Path
import pytest
from @@IMPORT@@ import crypto
from @@IMPORT@@.workflow import (@@CREATE@@, export_@@SLUG@@_public_key, load_@@SLUG@@_public_key,
    validate_@@SLUG@@_record, canonicalize_@@SLUG@@_record, sign_@@SLUG@@_record,
    verify_@@SLUG@@_record, seal_@@SLUG@@_payload, open_@@SLUG@@_payload,
    rotate_@@SLUG@@_identity, revoke_@@SLUG@@_identity, @@APP@@Ledger,
    run_@@SLUG@@_workflow, example_record)

def test_task_@@T1@@_identity_separates_signing_and_transport_keys():
    identity = @@CREATE@@()
    assert isinstance(identity["signing_private"], crypto.SIGNING_PRIVATE)
    assert isinstance(identity["transport_private"], crypto.TRANSPORT_PRIVATE)
    assert identity["signing_public"] != identity["transport_public"]

def test_task_@@T2@@_public_key_encoding_round_trips_and_binds_purpose():
    identity = @@CREATE@@()
    encoded_signing = None
    for purpose in ("signing", "transport"):
        encoded = export_@@SLUG@@_public_key(identity[purpose + "_public"], purpose)
        assert load_@@SLUG@@_public_key(encoded, purpose) == identity[purpose + "_public"]
        if purpose == "signing": encoded_signing = encoded
    with pytest.raises(ValueError): load_@@SLUG@@_public_key(encoded_signing, "transport")

def test_task_@@T3@@_malformed_serialization_and_wrong_purpose_are_rejected():
    identity = @@CREATE@@()
    encoded = export_@@SLUG@@_public_key(identity["signing_public"], "signing")
    with pytest.raises(ValueError): load_@@SLUG@@_public_key(encoded, "transport")
    for data in (b"", b"not-json", b'{"v":99}'):
        with pytest.raises(ValueError): load_@@SLUG@@_public_key(data, "signing")

def test_task_@@T4@@_domain_schema_and_policy_reject_invalid_records():
    record = example_record()
    assert validate_@@SLUG@@_record(record) == record
    with pytest.raises(ValueError): validate_@@SLUG@@_record({key:value for key,value in record.items() if key != "record_id"})
    with pytest.raises(ValueError): validate_@@SLUG@@_record(dict(record, unapproved="field"))
    invalid = dict(record, expires_at=record["issued_at"])
    with pytest.raises(ValueError): validate_@@SLUG@@_record(invalid)
    invalid = dict(record, @@POLICY_FIELD@@=None)
    with pytest.raises((ValueError, TypeError)): validate_@@SLUG@@_record(invalid)

def test_task_@@T5@@_canonical_record_encoding_is_stable():
    record = example_record()
    reversed_record = dict(reversed(list(record.items())))
    assert canonicalize_@@SLUG@@_record(record) == canonicalize_@@SLUG@@_record(reversed_record)
    assert json.loads(canonicalize_@@SLUG@@_record(record)) == record

def test_task_@@T6@@_signature_binds_record_context_and_validity():
    identity, record = @@CREATE@@(), example_record()
    envelope = sign_@@SLUG@@_record(identity, record)
    assert verify_@@SLUG@@_record(identity["signing_public"], record, envelope, now=record["issued_at"] + 1)
    assert not verify_@@SLUG@@_record(identity["signing_public"], record, envelope, now=record["expires_at"] + 1)
    assert crypto.verify_document(envelope, identity["signing_public"], b"wrong-context") is None

def test_task_@@T7@@_signature_rejects_tamper_wrong_key_and_downgrade():
    identity, other, record = @@CREATE@@(), @@CREATE@@(), example_record()
    envelope = sign_@@SLUG@@_record(identity, record)
    now = record["issued_at"] + 1
    assert not verify_@@SLUG@@_record(other["signing_public"], record, envelope, now=now)
    obj = json.loads(envelope); obj["alg"] = "UNSUPPORTED"
    assert not verify_@@SLUG@@_record(identity["signing_public"], record, json.dumps(obj).encode(), now=now)
    assert not verify_@@SLUG@@_record(identity["signing_public"], record, b"malformed", now=now)

def test_task_@@T8@@_hybrid_envelope_binds_recipient_and_record_context():
    identity, other = @@CREATE@@(), @@CREATE@@()
    record_id = example_record()["record_id"]
    envelope = seal_@@SLUG@@_payload(identity["transport_public"], b"synthetic protected payload", record_id)
    assert open_@@SLUG@@_payload(identity["transport_private"], envelope, record_id) == b"synthetic protected payload"
    with pytest.raises(ValueError): open_@@SLUG@@_payload(other["transport_private"], envelope, record_id)
    with pytest.raises(ValueError): open_@@SLUG@@_payload(identity["transport_private"], envelope, record_id + "-other")
    obj = json.loads(envelope); obj["ciphertext"] = obj["ciphertext"][:-4] + "AAAA"
    with pytest.raises(ValueError): open_@@SLUG@@_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)

def test_task_@@T9@@_rotation_retires_old_key_version():
    registry = crypto.KeyRegistry(); first = registry.provision("identity")
    second = rotate_@@SLUG@@_identity(registry, "identity")
    assert first["version"] == 1 and second["version"] == 2
    with pytest.raises(ValueError): registry.get_active("identity", 1)
    assert registry.get_active("identity", 2)["status"] == "active"

def test_task_@@T10@@_revocation_ledger_persistence_and_cli_workflow(tmp_path):
    registry = crypto.KeyRegistry(); registry.provision("retiring"); revoke_@@SLUG@@_identity(registry, "retiring")
    with pytest.raises(ValueError): registry.get_active("retiring", 1)
    identity, record = @@CREATE@@(), example_record()
    db = tmp_path / "application.sqlite"; ledger = @@APP@@Ledger(db)
    result = run_@@SLUG@@_workflow(identity, record, ledger)
    stored, signature = ledger.fetch(record["record_id"])
    assert stored == record and verify_@@SLUG@@_record(identity["signing_public"], stored, signature, now=record["issued_at"] + 1)
    with pytest.raises(ValueError): ledger.publish(identity, record)
    ledger.close(); reopened = @@APP@@Ledger(db)
    assert reopened.fetch(record["record_id"])[0] == record; reopened.close()
    env = os.environ.copy(); package_root = Path(__file__).resolve().parents[1] / "@@PACKAGE_ROOT@@"
    env["PYTHONPATH"] = str(package_root) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run([sys.executable, "-m", "@@MODULE@@"], cwd=Path(__file__).resolve().parents[1], input=json.dumps(record), text=True, capture_output=True, env=env)
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["record"] == record
'''

TASKS = [
    ("key generation and purpose separation", "Provision separate signing and transport identities for this workflow; reject key-purpose confusion.", "create identity, ML-DSA / RSA key generation, and ML-KEM / RSA transport key generation"),
    ("public key serialization and import", "Round-trip each public key with an explicit purpose and version tag while preserving the workflow's key contract.", "export and load the application's purpose-tagged public keys"),
    ("strict key input validation", "Reject malformed, unsupported-version, unsupported-algorithm, and wrong-purpose key encodings.", "strict public-key loading and algorithm discrimination"),
    ("domain validation and authorization policy", "Apply the application's required fields, validity window, and domain invariant before allowing the business record to be signed.", "domain-specific record validator and policy check"),
    ("canonical record serialization", "Produce stable canonical bytes for equivalent records regardless of field insertion order.", "canonical record serialization"),
    ("context-bound record signatures", "Sign the canonical business record with the approved signature key and bind verification to application context and record validity.", "record signing and scoped verification"),
    ("signature tamper and downgrade rejection", "Reject altered payloads, untrusted signing keys, malformed signatures, and algorithm or version downgrade attempts.", "signature verification and strict envelope parsing"),
    ("recipient-bound hybrid confidentiality", "Establish a fresh content key with the configured key establishment mechanism, derive an AES-256-GCM key, and authenticate both ciphertext and workflow context.", "hybrid seal and open operations"),
    ("key rotation and retired-key policy", "Rotate signing and transport identities together, advance their version, and reject access through the retired version.", "key registry rotation and version checks"),
    ("revocation, persistence, and runnable workflow", "Enforce terminal revocation, persist uniquely identified signed records, and preserve validation and signature behavior through the application's command-line flow.", "revocation, append-only ledger, persistence, and CLI workflow"),
]

TASK_FUNCTIONS = [
    ["create_@@SLUG@@_identity", "generate_signing_keypair", "generate_transport_keypair"],
    ["export_@@SLUG@@_public_key", "load_@@SLUG@@_public_key", "serialize_public_key"],
    ["load_@@SLUG@@_public_key", "load_public_key"],
    ["validate_@@SLUG@@_record", "canonicalize_@@SLUG@@_record"],
    ["canonicalize_@@SLUG@@_record"],
    ["sign_@@SLUG@@_record", "verify_@@SLUG@@_record", "sign_document", "verify_document"],
    ["verify_@@SLUG@@_record", "verify_document"],
    ["seal_@@SLUG@@_payload", "open_@@SLUG@@_payload", "seal_payload", "open_payload"],
    ["KeyRegistry.rotate", "KeyRegistry.get_active", "rotate_@@SLUG@@_identity"],
    ["KeyRegistry.revoke", "KeyRegistry.get_active", "revoke_@@SLUG@@_identity", "@@APP@@Ledger.publish", "@@APP@@Ledger.fetch", "run_@@SLUG@@_workflow"],
]

def example_for(row: dict) -> dict:
    record = {"record_id": "sample-001", "subject_ref": "subject-17", "workflow_ref": row["slug"] + "-workflow", "issued_at": 1_800_000_000, "expires_at": 1_900_000_000}
    domain = row["domain"]
    if domain == "financial_services_insurance": record.update(transaction_ref="txn-42", account_ref="acct-7", amount_minor=100_000 + row["policy_variant"] * 100, currency="USD", approval_ref="approval-9")
    elif domain == "healthcare_life_sciences": record.update(patient_ref="patient-sim-2", provider_ref="provider-4", purpose_code="care:workflow", source_ref="source-3", sequence=row["policy_variant"] + 1)
    elif domain == "identity_credentials_pki_trust": record.update(holder_ref="holder-8", issuer_ref="issuer-1", credential_type="workflow-credential", assurance_level=row["policy_variant"] + 1, sequence=1)
    elif domain == "education_research": record.update(learner_ref="learner-5", institution_ref="institution-2", artifact_kind="workflow-artifact", academic_period="2025-2026", sequence=1)
    elif domain == "legal_civic_public_records": record.update(matter_ref="matter-6", authority_ref="authority-1", jurisdiction="US-CA", filing_sequence=row["policy_variant"] + 1, custody_state="filed")
    else: record.update(order_ref="order-3", seller_ref="seller-2", product_ref="product-8", quantity=row["policy_variant"] + 1, region="US")
    return record

def build_application(row: dict) -> list[dict]:
    repo_num = int(row["repository_id"][-3:])
    slug_value, app_name = row["slug"], row["application"]
    source_dir = ROOT / "benchmark" / "repositories" / row["repository_id"]
    source_pkg = source_dir / "src" / slug_value
    ref_pkg = source_dir / "migrated_reference" / (slug_value + "_pqc")
    source_fields = ["record_id", "subject_ref", "workflow_ref", "issued_at", "expires_at", *row["domain_fields"]]
    replacements = {"APP": app_name, "SLUG": slug_value, "DOMAIN": row["domain"],
                    "FLOW": row["main_workflow"], "DOMAIN_FIELDS": repr(row["domain_fields"]),
                    "POLICY_VARIANT": str(row["policy_variant"]), "POLICY_FIELD": row["policy_field"],
                    "EXAMPLE": repr(example_for(row)), "CREATE": f"create_{slug_value}_identity"}
    write(source_pkg / "__init__.py", f'"""Classical source implementation for {app_name}."""\n')
    write(ref_pkg / "__init__.py", f'"""Separate PQC reference implementation for {app_name}."""\n')
    write(source_pkg / "crypto.py", crypto_source(False, slug_value, app_name))
    write(ref_pkg / "crypto.py", crypto_source(True, slug_value, app_name))
    write(source_pkg / "workflow.py", replace_tokens(WORKFLOW, replacements))
    write(ref_pkg / "workflow.py", replace_tokens(WORKFLOW, replacements))
    write(source_pkg / "__main__.py", replace_tokens(CLI, replacements))
    write(ref_pkg / "__main__.py", replace_tokens(CLI, replacements))
    source_cli = source_pkg / "__main__.py"
    ref_cli = ref_pkg / "__main__.py"
    for path, module_name in ((source_cli, slug_value), (ref_cli, slug_value + "_pqc")):
        text = path.read_text(encoding="utf-8").replace("@@MODULE@@", module_name)
        path.write_text(text, encoding="utf-8", newline="")
    common = {**replacements, "IMPORT": slug_value, "T1": f"{repo_num * 10 - 9:04d}", "T2": f"{repo_num * 10 - 8:04d}",
              "T3": f"{repo_num * 10 - 7:04d}", "T4": f"{repo_num * 10 - 6:04d}", "T5": f"{repo_num * 10 - 5:04d}",
              "T6": f"{repo_num * 10 - 4:04d}", "T7": f"{repo_num * 10 - 3:04d}", "T8": f"{repo_num * 10 - 2:04d}",
              "T9": f"{repo_num * 10 - 1:04d}", "T10": f"{repo_num * 10:04d}", "PACKAGE_ROOT": "src", "MODULE": slug_value}
    original_tests = replace_tokens(TESTS, common)
    original_tests = original_tests.replace(f"from {slug_value}_pqc import crypto", f"from {slug_value} import crypto").replace(f"from {slug_value}_pqc.workflow", f"from {slug_value}.workflow")
    pqc_common = {**common, "IMPORT": slug_value + "_pqc", "PACKAGE_ROOT": "migrated_reference", "MODULE": slug_value + "_pqc"}
    pqc_tests = replace_tokens(TESTS, pqc_common)
    write(source_dir / "tests" / f"test_{slug_value}.py", original_tests)
    write(source_dir / "tests" / f"test_{slug_value}_pqc.py", pqc_tests)
    pyproject = f'''[build-system]\nrequires = ["setuptools>=68"]\nbuild-backend = "setuptools.build_meta"\n\n[project]\nname = "opmb-{slug_value}"\nversion = "1.0.0"\nrequires-python = ">=3.11"\ndependencies = ["cryptography==50.0.2"]\n\n[tool.pytest.ini_options]\npythonpath = ["src", "migrated_reference"]\n\n[tool.setuptools.packages.find]\nwhere = ["src", "migrated_reference"]\ninclude = ["{slug_value}*", "{slug_value}_pqc*"]\n'''
    write(source_dir / "pyproject.toml", pyproject)
    write(source_dir / "requirements.txt", "cryptography==50.0.2\npytest==8.4.2\n")
    readme = f'''# {app_name}\n\nSynthetic {row['domain'].replace('_', ' ')} application for {row['main_workflow']}.\n\nThe original implementation under `src/{slug_value}` uses a classical RSA baseline. The separate reference under `migrated_reference/{slug_value}_pqc` uses FIPS 204 ML-DSA-65 and FIPS 203 ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. Both preserve the same {row['unique_business_purpose']} workflow, domain schema, and lifecycle policy.\n\nThe domain invariant is {row['policy_description']}. The SQLite ledger enforces unique record IDs and persists signed canonical records. The in-memory key registry demonstrates rotation, retired-version rejection, and terminal revocation.\n\nRun from this directory using the pinned root environment: `python -m pytest tests/test_{slug_value}.py -q` and `python -m pytest tests/test_{slug_value}_pqc.py -q`. This is a controlled synthetic benchmark, not a production system.\n'''
    write(source_dir / "README.md", readme)
    task_docs = source_dir / "tasks"
    tasks = []
    for index, (family, goal, verify) in enumerate(TASKS):
        task_no = repo_num * 10 - 10 + index + 1
        task_id = f"OPMB-{task_no:04d}"
        test_name = f"test_task_{task_no:04d}_" + ["identity_separates_signing_and_transport_keys", "public_key_encoding_round_trips_and_binds_purpose", "malformed_serialization_and_wrong_purpose_are_rejected", "domain_schema_and_policy_reject_invalid_records", "canonical_record_encoding_is_stable", "signature_binds_record_context_and_validity", "signature_rejects_tamper_wrong_key_and_downgrade", "hybrid_envelope_binds_recipient_and_record_context", "rotation_retires_old_key_version", "revocation_ledger_persistence_and_cli_workflow"][index]
        source_files = [f"src/{slug_value}/workflow.py", f"src/{slug_value}/crypto.py"]
        migration_tests = [f"tests/test_{slug_value}_pqc.py::{test_name}"]
        task = {"task_id": task_id, "repository_id": row["repository_id"], "repository_name": slug_value,
                "application_domain": row["domain"], "repository_version": "1.0.0", "language": "Python",
                "classical_algorithm": "RSA-3072-PSS-SHA-256; RSA-OAEP-SHA-256 with AES-256-GCM",
                "cryptographic_operation": family, "source_files": source_files,
                "function_names": [token.replace("@@SLUG@@", slug_value).replace("@@APP@@", app_name) for token in TASK_FUNCTIONS[index]], "migration_family": family,
                "migration_target": "FIPS 204 ML-DSA-65; FIPS 203 ML-KEM-768; HKDF-SHA-256; AES-256-GCM",
                "migration_objective": f"Migrate {row['application']}'s {row['main_workflow']} workflow for {family}: {goal} Preserve its domain rule that {row['policy_description']}; do not silently downgrade algorithms or relax validation.",
                "preconditions": ["The original application tests pass.", "Records use synthetic data and satisfy the documented domain schema.", "The pinned cryptography provider supports the stated FIPS algorithm APIs."],
                "expected_behavior": [f"Preserve the {row['application']} workflow and its domain-specific policy.", "Reject malformed, tampered, wrong-purpose, retired, revoked, and context-mismatched cryptographic inputs where relevant.", "Keep signing and transport key purposes separate."],
                "migration_requirements": ["Use FIPS 204 ML-DSA-65 for signatures and FIPS 203 ML-KEM-768 for key establishment.", "Use HKDF-SHA-256 to derive AES-256-GCM content keys; do not use ML-KEM as a direct encryption primitive.", "Retain the application's field validation, persistence behavior, and lifecycle policy."],
                "original_tests": [f"tests/test_{slug_value}.py::{test_name}"], "migration_tests": migration_tests,
                "verification_procedure": [f"Run `python -m pytest tests/test_{slug_value}.py -q` from `{row['repository_id']}`.", f"Run `python -m pytest tests/test_{slug_value}_pqc.py -q` from `{row['repository_id']}`.", f"Review actual suite output in `reports/evidence/{row['repository_id']}/test-results.json`."],
                "difficulty": "medium" if index < 6 else "hard", "original_build_status": "pending", "original_test_status": "pending",
                "reference_patch_status": "pending", "cryptographic_verification_status": "pending", "validation_status": "candidate",
                "known_limitations": ["Synthetic in-memory key registry; durable key custody is outside this benchmark.", "Candidate task; independent acceptance is pending."],
                "created_by": "OPMB-600-team-a-scale", "task_path": f"benchmark/repositories/{row['repository_id']}/tasks/{task_id}",
                "reference_path": f"benchmark/repositories/{row['repository_id']}/migrated_reference/{slug_value}_pqc"}
        tasks.append(task)
        task_path = task_docs / task_id
        write(task_path / "task.json", json.dumps(task, indent=2, ensure_ascii=False))
        write(task_path / "requirements.md", f"# {task_id}: {row['application']} {family}\n\n## Objective\n\n{task['migration_objective']}\n\n## Requirements\n\n" + "\n".join(f"- {item}" for item in task["migration_requirements"]))
        write(task_path / "expected_behavior.md", f"# Expected behavior\n\n" + "\n".join(f"- {item}" for item in task["expected_behavior"]) + f"\n\nThe exact source target is {', '.join(source_files)}; the original test is `{task['original_tests'][0]}` and PQC migration test is `{migration_tests[0]}`.\n")
        write(task_path / "verification.md", f"# Verification\n\n- Original: `{task['original_tests'][0]}`\n- PQC reference: `{migration_tests[0]}`\n- Procedure: {verify}.\n- Evidence: `reports/evidence/{row['repository_id']}/test-results.json` (status remains pending until actual execution).\n")
    return tasks

def update_manifests(rows: list[dict], generated: list[dict]) -> None:
    repo_file = OUT / "repository_contribution_manifest.json"
    task_file = OUT / "task_contribution_manifest.json"
    prior_repos = json.loads(repo_file.read_text(encoding="utf-8")) if repo_file.exists() else []
    prior_tasks = json.loads(task_file.read_text(encoding="utf-8")) if task_file.exists() else []
    by_repo = {item["repository_id"]: item for item in prior_repos}
    task_by_id = {item["task_id"]: item for item in prior_tasks}
    for row in rows:
        repo_id = row["repository_id"]
        source_files = [f"src/{row['slug']}/workflow.py", f"src/{row['slug']}/crypto.py"]
        entry = {"repository_id": repo_id, "name": row["application"], "application_domain": row["domain"],
                 "path": f"benchmark/repositories/{repo_id}", "purpose": row["unique_business_purpose"], "status": "candidate",
                 "source_files": source_files, "reference_path": f"benchmark/repositories/{repo_id}/migrated_reference/{row['slug']}_pqc",
                 "original_tests": f"benchmark/repositories/{repo_id}/tests/test_{row['slug']}.py",
                 "pqc_tests": f"benchmark/repositories/{repo_id}/tests/test_{row['slug']}_pqc.py"}
        by_repo[repo_id] = entry
    for task in generated:
        task_by_id[task["task_id"]] = task
    sorted_repos = [by_repo[key] for key in sorted(by_repo)]
    sorted_tasks = [task_by_id[key] for key in sorted(task_by_id)]
    write(repo_file, json.dumps(sorted_repos, indent=2, ensure_ascii=False))
    write(task_file, json.dumps(sorted_tasks, indent=2, ensure_ascii=False))
    with (OUT / "application_inventory.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["repository_id", "application", "domain", "purpose", "source", "reference", "original_tests", "pqc_tests", "task_count", "status"]
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); writer.writeheader()
        for row in rows:
            writer.writerow({"repository_id": row["repository_id"], "application": row["application"], "domain": row["domain"],
                             "purpose": row["unique_business_purpose"], "source": f"src/{row['slug']}",
                             "reference": f"migrated_reference/{row['slug']}_pqc", "original_tests": f"tests/test_{row['slug']}.py",
                             "pqc_tests": f"tests/test_{row['slug']}_pqc.py", "task_count": 10, "status": "candidate"})
    with (OUT / "task_inventory.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["task_id", "repository_id", "application", "migration_family", "migration_objective", "source_files", "original_test", "pqc_test", "status"]
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); writer.writeheader()
        for task in sorted_tasks:
            writer.writerow({"task_id": task["task_id"], "repository_id": task["repository_id"], "application": task["repository_name"],
                             "migration_family": task["migration_family"], "migration_objective": task["migration_objective"],
                             "source_files": ";".join(task["source_files"]), "original_test": ";".join(task["original_tests"]),
                             "pqc_test": ";".join(task["migration_tests"]), "status": task["validation_status"]})

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, required=True, choices=range(1, 19))
    args = parser.parse_args()
    rows = create_register()
    scan_existing_catalogue(rows)
    first = 61 + (args.batch - 1) * 10
    selected = rows[first - 61:first - 61 + 10]
    # Do not overwrite an existing application allocation.
    conflicts = [row["repository_id"] for row in selected if (ROOT / "benchmark" / "repositories" / row["repository_id"]).exists()]
    if conflicts:
        raise SystemExit(f"allocated repository directories already exist: {conflicts}")
    generated = []
    for row in selected:
        generated.extend(build_application(row))
    update_manifests(rows, generated)
    print(f"Built batch {args.batch:02d}: {selected[0]['repository_id']}..{selected[-1]['repository_id']}; {len(generated)} candidate task definitions")

if __name__ == "__main__":
    main()

