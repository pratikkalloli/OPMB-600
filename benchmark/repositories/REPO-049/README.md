# EventPass

EventPass issues synthetic event credentials and verifies them offline. SQLite stores pass status and the signed credential bytes; a verifier can check issuer, event, holder alias, serial, and expiration without a live service. Revocation is supplied as a local verifier snapshot. The original uses RSA-PSS; the reference uses ML-DSA-65. This is a controlled simulation, not a production ticketing platform.

Install requirements.txt and run pytest. All events and participants are fictional.
