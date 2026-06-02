SELECT count(*) AS total_quiries,
    count(*) FILTER (WHERE state='active') AS active_queries
FROM pg_stat_activity;