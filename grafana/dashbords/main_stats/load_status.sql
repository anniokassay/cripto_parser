SELECT lt.source_name     AS source_name,
       MAX(li.CREATED_AT) AS last_load_ts
  FROM raw_data.load_info li
  JOIN dict.load_type     lt ON lt.id = li.load_type
 GROUP BY lt.source_name
 ORDER BY source_name;