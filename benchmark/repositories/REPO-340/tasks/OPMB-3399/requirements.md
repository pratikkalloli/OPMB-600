# OPMB-3399: Recover an artifact and reject malformed or altered envelopes

The migration must preserve the Reconciles parcel scans through sortation lanes and flags missing or duplicate handoffs; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the shipment_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and ParcelSortationManifest context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
