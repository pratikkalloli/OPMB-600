# ZoneSeal

ZoneSeal stores synthetic DNS-style zone snapshots. Canonical zone data sorts resource records and binds the zone name and serial. Publishers must advance serials, and resolvers verify the signature before accepting a snapshot. The baseline uses ECDSA P-256; the reference uses ML-DSA-65. This is not a production DNSSEC implementation.
