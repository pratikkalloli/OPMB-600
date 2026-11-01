# Expected behavior

GalleryLoanConditionReport: Keep signed galleryloanconditionreport issuance in SQLite and reject duplicate report_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
