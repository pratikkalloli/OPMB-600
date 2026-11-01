# OPMB-2446: Serialize the verification key in the algorithm format

The migration must preserve the Lot closeout, yield reconciliation, quality signoff, certificate publication, and correction through a new revision. business invariant and the batch_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and BatchYieldCertificate context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
