# OPMB-0475: Invoice signer public-key export format

Migrate the public-key distribution contract from SPKI PEM to ML-DSA raw encoding.

Update all affected callers and serialization boundaries. Preserve the business rule that signed versions remain historical records.
