-- DROP MATERIALIZED VIEW staged_data.exchange_offer_current
CREATE MATERIALIZED VIEW staged_data.exchange_offer_current
AS 
SELECT ROW_NUMBER() OVER() AS sinth_id,
       d.change_type_id,
       ct.currency_out,
       ct.currency_gain,
       d.change_rate,
       lt.source_name,
       d.seller_name,
       fli.created_at                             AS from_ts,
       COALESCE(lli.created_at,clock_timestamp()) AS till_ts,
       clock_timestamp()                          AS created_at
  FROM (     
  SELECT q.change_type_id   AS change_type_id,
         q.price            AS change_rate,
         q.seller           AS seller_name,
         MIN(q.load_id)     AS first_load_id,
         MAX(q.load_id) + 1 AS last_load_id -- следующий за максимальныо полученным
    FROM (
    SELECT ROW_NUMBER() OVER (PARTITION BY db.change_type_id ORDER BY db.load_id) - ROW_NUMBER() OVER (PARTITION BY db.seller, db.price, db.change_type_id ORDER BY db.load_id) AS grp,
          db.load_id,
          db.change_type_id,
          db.seller,
          db.price
      FROM raw_data.data_bybit db
     WHERE db.load_id >= staged_data.day_load_id(CURRENT_DATE)
     UNION ALL
    SELECT ROW_NUMBER() OVER (PARTITION BY dk.change_type_id ORDER BY dk.load_id) - ROW_NUMBER() OVER (PARTITION BY dk.seller, dk.price, dk.change_type_id ORDER BY dk.load_id) AS grp,
           dk.load_id,
           dk.change_type_id,
           dk.seller,
           dk.price
      FROM raw_data.data_kucoin dk
     WHERE dk.load_id >= staged_data.day_load_id(CURRENT_DATE)
     UNION ALL
    SELECT ROW_NUMBER() OVER (PARTITION BY dg.change_type_id ORDER BY dg.load_id) - ROW_NUMBER() OVER (PARTITION BY dg.seller, dg.price, dg.change_type_id ORDER BY dg.load_id) AS grp,
           dg.load_id,
           dg.change_type_id,
           dg.seller,
           dg.price
      FROM raw_data.data_gatecom dg
     WHERE dg.load_id >= staged_data.day_load_id(CURRENT_DATE)
    ) q
   GROUP BY q.change_type_id, q.price, q.seller, q.grp
  ) d
  JOIN dict.change_type         ct  ON ct.id = d.change_type_id
  JOIN raw_data.load_info       fli ON fli.id = d.first_load_id
  LEFT JOIN raw_data.load_info  lli ON lli.id = d.last_load_id
  JOIN dict.load_type           lt  ON lt.id = fli.load_type;

  CREATE UNIQUE INDEX exchange_offer_uix ON staged_data.exchange_offer_current (sinth_id);