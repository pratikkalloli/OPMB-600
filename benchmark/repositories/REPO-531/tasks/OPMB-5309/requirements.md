# Migration requirements

CreatorPayoutStatement: Keep signed creatorpayoutstatement issuance in SQLite and reject duplicate payout_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
