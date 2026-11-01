# Expected behavior

Migrate ParcelSortationManifest validate the domain record and its lifecycle state from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Reconciles parcel scans through sortation lanes and flags missing or duplicate handoffs; intake, validate, approve, record transition, and preserve a verifiable audit artifact. semantics.

Valid parcel sortation manifest operations remain interoperable with the documented PQC format. Invalid state, bad revision_epoch, altered content, wrong keys, and unsupported versions are rejected.
