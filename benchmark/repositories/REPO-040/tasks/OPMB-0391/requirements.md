# OPMB-0391: VendorOrder: Validate and canonicalize the domain entity

Preserve required fields, canonical encoding, identifier binding, and legal lifecycle states as signed domain records migrate. VendorOrder workflow: Buyer and supplier purchase orders with currency, integer totals, and fulfillment transitions. Domain-specific invariants: Order total must be positive integer cents and currency must be a three-letter uppercase code. The task concerns fields order_id, buyer_id, supplier_id, currency, total_cents, created_at, status and legal transitions draft -> submitted -> accepted -> fulfilled -> cancelled.

## Required changes

- Migrate the identified operation to ML-DSA-65.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
