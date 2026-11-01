# OPMB-0473: RSA invoice signer key provisioning

Replace RSA invoice signer key generation with ML-DSA-65 and update signer key distribution.

Update all affected callers and serialization boundaries. Preserve the business rule that signed versions remain historical records.
