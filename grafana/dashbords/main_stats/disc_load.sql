SELECT (pg_database_size(current_database()) / 1024 / 1024)           AS database_size_mb,
       (pg_database_size(current_database()) / 1024 / 1024)/ 204.80   AS disc_used_percent