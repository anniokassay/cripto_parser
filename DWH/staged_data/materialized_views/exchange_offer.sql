CREATE MATERIALIZED VIEW staged_data.exchange_offer
AS 
/* 
(
  change_type_id    INT,
  change_type_name  VARCHAR,
  source_name       VARCHAR,
  from_ts           TIMESTAMPTZ,
  till_ts           TIMESTAMPTZ,
  currency_out      varchar(6) NOT NULL,
  currency_gain     varchar(6) NOT NULL  
  )
*/
SELECT fli.created_at                                     AS from_ts,
       COALESCE(lli.created_at,'3000-01-01'::TIMESTAMPTZ) AS till_ts,
       ct.codename                                        AS change_type_name,
       ct.currency_out                                    AS currency_out,       
       ct.currency_gain                                   AS currency_gain,
       d.rate                                             AS rate,
       d.seller_name                                      AS seller_name
  FROM (
  SELECT d.change_type_id   AS change_type_id,
         --ct.codename        AS change_type_name,
         li.load_type       AS load_type_id,
         MIN(li.id)         AS first_load_id,
         MAX(li.id)+1       AS last_load_id,
         --ct.currency_out    AS currency_out,       
         --ct.currency_gain   AS currency_gain,
         d.price            AS rate,
         d.seller           AS seller_name
    FROM raw_data.data_bybit  d
    JOIN raw_data.load_info   li  ON li.id = d.load_id
    --JOIN dict.load_type       lt  ON lt.id = li.load_type
   WHERE d.limit_min > 500
   GROUP BY d.change_type_id,li.load_type,d.price,d.seller,d.limit_min, d.limit_max) d
  JOIN dict.change_type         ct  ON ct.id = d.change_type_id
  JOIN raw_data.load_info       fli ON fli.id = d.first_load_id
  LEFT JOIN raw_data.load_info  lli ON lli.id = d.last_load_id