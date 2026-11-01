# SecureMailbox

SecureMailbox stores synthetic encrypted messages addressed to registered recipients. Each message is signed by its sender and protected to the recipient key; message identifiers are unique and mailbox retrieval requires an active recipient. Baseline cryptography uses RSA-PSS, X25519, HKDF, and AES-GCM. The reference uses ML-DSA-65 and ML-KEM-768 while retaining HKDF and AES-GCM.
