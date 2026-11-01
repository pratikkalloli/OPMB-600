# OPMB-0478: Invoice digest compatibility

Update digest consumers and indexes to use the canonicalized invoice payload consistently.

Update all affected callers and serialization boundaries. Preserve the business rule that signed versions remain historical records.
