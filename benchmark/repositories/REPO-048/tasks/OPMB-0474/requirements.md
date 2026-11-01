# OPMB-0474: RSA PEM invoice signer public-key import

Replace PEM/RSA public-key loading with strict ML-DSA public-key decoding.

Update all affected callers and serialization boundaries. Preserve the business rule that signed versions remain historical records.
