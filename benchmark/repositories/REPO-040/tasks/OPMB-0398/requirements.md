# OPMB-0398: VendorOrder: Encode recipient public-key material

Replace RSA PEM serialization with the pinned provider raw ML-KEM-768 public-key encoding and update consumers. VendorOrder workflow: Buyer and supplier purchase orders with currency, integer totals, and fulfillment transitions. Domain-specific invariants: Order total must be positive integer cents and currency must be a three-letter uppercase code. The task concerns fields order_id, buyer_id, supplier_id, currency, total_cents, created_at, status and legal transitions draft -> submitted -> accepted -> fulfilled -> cancelled.

## Required changes

- Migrate the identified operation to ML-KEM-768.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
