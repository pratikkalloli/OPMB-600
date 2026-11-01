# ShipmentProof

ShipmentProof records synthetic custody handoffs as an append-only, hash-linked SQLite event sequence. Each handoff binds shipment, sequence, sender, recipient, location, timestamp, and previous-event digest before signing. The baseline uses RSA-PSS; the separate reference uses ML-DSA-65. This project simulates evidence handling and does not provide legal chain-of-custody certification.

Install requirements.txt and run pytest. Shipment data and identities are fictional.
