# ClearingDesk

ClearingDesk records synthetic payment instructions and requires two distinct treasury approvers before settlement. The baseline uses RSA-PSS for approval attestations; the reference uses ML-DSA-65. Transfer exports are sealed to the receiving desk with X25519/AES-GCM in the baseline and ML-KEM-768/AES-GCM in the reference. This is a test application, not a payment network.

Install requirements.txt and run pytest from this directory.
