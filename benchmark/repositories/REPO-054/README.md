# CareConsent

CareConsent models synthetic patient consent grants for named research purposes. Each grant binds a consent ID, subject alias, study, scope, expiry, and grant revision. Revocation is append-only and later access checks fail closed. The baseline uses RSA-PSS signatures; the reference uses ML-DSA-65. No real health data is included.
