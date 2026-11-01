# OPMB-0472: RSA-PSS invoice signature verification

Migrate signature verification and retain fail-closed modified-payload and wrong-key behavior.

Update all affected callers and serialization boundaries. Preserve the business rule that signed versions remain historical records.
