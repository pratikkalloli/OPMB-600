# Expected behavior

PodcastEpisodeRelease: Keep signed podcastepisoderelease issuance in SQLite and reject duplicate release_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
