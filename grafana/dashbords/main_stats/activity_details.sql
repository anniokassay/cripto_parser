SELECT usename, query, xact_start 
  FROM pg_stat_activity
 WHERE state='active';