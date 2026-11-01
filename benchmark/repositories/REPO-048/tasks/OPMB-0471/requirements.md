# OPMB-0471: RSA-PSS invoice signature generation

Move canonical invoice signatures from RSA-PSS to ML-DSA-65.

Update all affected callers and serialization boundaries. Preserve the business rule that signed versions remain historical records.
