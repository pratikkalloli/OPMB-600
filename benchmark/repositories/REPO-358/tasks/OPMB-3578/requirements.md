# OPMB-3578: Protect a workflow artifact for an authorized recipient

The migration must preserve the Captures recipient acknowledgement and parcel identity for a delivery transfer; intake, validate, approve, record transition, and preserve a verifiable audit artifact. business invariant and the shipment_id scope.

- Keep cryptographic key roles separate.
- Bind an explicit version and DeliveryProofOfHandoff context.
- Reject malformed encodings and tampered input.
- Never use a classical fallback.
