"""PQC implementation of the fictional print release workflow."""
from . import crypto

class PrintService:
    def __init__(self):
        self.users = set()
        self.printers = {}
        self.jobs = {}
        self.audit = []
        self.audit_private, self.audit_public = crypto.generate_audit_keypair()

    def register_user(self, user_id):
        if not isinstance(user_id, str) or not user_id.strip() or user_id in self.users:
            raise ValueError("user identifier is empty or already registered")
        self.users.add(user_id)
        self.audit.append(("user_registered", user_id))

    def revoke_user(self, user_id):
        if user_id not in self.users:
            raise ValueError("unknown user")
        self.users.remove(user_id)
        self.audit.append(("user_revoked", user_id))

    def register_printer(self, printer_id):
        if not isinstance(printer_id, str) or not printer_id.strip() or printer_id in self.printers:
            raise ValueError("printer identifier is empty or already registered")
        private, public = crypto.generate_printer_keypair()
        self.printers[printer_id] = {"private": private, "public": public, "active": True}
        self.audit.append(("printer_registered", printer_id))
        return crypto.serialize_public_key(public)

    def submit_job(self, job_id, owner, printer_id, content):
        if owner not in self.users:
            raise ValueError("user is not authorized to submit print jobs")
        if not all(isinstance(value, str) and value.strip() for value in (job_id, owner, printer_id)):
            raise ValueError("job, owner, and printer identifiers are required")
        if not isinstance(content, bytes) or not content or len(content) > 2_000_000:
            raise ValueError("print content must be 1..2000000 bytes")
        printer = self.printers.get(printer_id)
        if not printer or not printer["active"] or job_id in self.jobs:
            raise ValueError("printer unavailable or job identifier already exists")
        package = crypto.encrypt_job_content(content, printer["public"], job_id)
        metadata = crypto.canonical_metadata(job_id, owner, printer_id, package["nonce"], package["ciphertext"], package["encapsulation"])
        signature = crypto.sign_job_metadata(metadata, self.audit_private)
        self.jobs[job_id] = {"owner": owner, "printer_id": printer_id, "package": package, "metadata": metadata, "signature": signature, "status": "queued"}
        self.audit.append(("job_submitted", job_id))

    def release_job(self, job_id, printer_id):
        job = self.jobs.get(job_id)
        if not job or job["printer_id"] != printer_id or job["status"] != "queued":
            raise ValueError("job is unavailable to this printer")
        if not crypto.verify_job_metadata(job["metadata"], job["signature"], self.audit_public):
            raise ValueError("job metadata authentication failed")
        content = crypto.decrypt_job_content(job["package"], self.printers[printer_id]["private"], job_id)
        job["status"] = "released"
        self.audit.append(("job_released", job_id))
        return content

    def cancel_job(self, job_id, owner):
        job = self.jobs.get(job_id)
        if not job or job["owner"] != owner or job["status"] != "queued":
            raise ValueError("only the owner can cancel a queued job")
        job["status"] = "cancelled"
        self.audit.append(("job_cancelled", job_id))
        return True
