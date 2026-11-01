# OPMB-0393: VendorOrder: Sign a domain decision

Migrate domain decision signatures from RSA-PSS/SHA-256 to ML-DSA-65 while preserving canonical bytes and domain separation. VendorOrder workflow: Buyer and supplier purchase orders with currency, integer totals, and fulfillment transitions. Domain-specific invariants: Order total must be positive integer cents and currency must be a three-letter uppercase code. The task concerns fields order_id, buyer_id, supplier_id, currency, total_cents, created_at, status and legal transitions draft -> submitted -> accepted -> fulfilled -> cancelled.

## Required changes

- Migrate the identified operation to ML-DSA-65.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
