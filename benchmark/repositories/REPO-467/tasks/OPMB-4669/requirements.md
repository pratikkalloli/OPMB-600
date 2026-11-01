# Migration requirements

ContainerPromotionTicket: Keep signed containerpromotionticket issuance in SQLite and reject duplicate ticket_id records. Use ML-DSA-65 without classical fallback. Preserve canonical claims and application policy.
