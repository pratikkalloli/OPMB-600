# InvoiceSeal

InvoiceSeal is a synthetic invoice ledger. It stores integer minor-unit amounts, currency, issuer and revision in SQLite. RSA-PSS signs canonical invoice versions; the separate reference uses ML-DSA-65. A signature proves a historical revision, not the current invoice state. This simulation is not an accounting or tax system.

Install requirements.txt and run pytest from this directory. Invoice and issuer data are synthetic.
