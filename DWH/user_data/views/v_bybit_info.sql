CREATE OR REPLACE VIEW user_data.v_bybit_info
AS 
WITH day_load AS (
  SELECT created_at::DATE   AS load_day,
         b.change_type_id   AS change_type_id,
         MIN(i.id)          AS first_load, 
         MAX(i.id)          AS last_load
    FROM raw_data.load_info   i
    JOIN raw_data.data_bybit  b ON b.load_id = i.id
   GROUP BY 1, 2
  ) 
SELECT li.created_at::DATE    AS oper_date,
       b.change_type_id       AS change_type_id,
       ROUND(AVG(b.price),2)  AS avg_price,
       MIN(b.price)           AS min_price,
       MAX(b.price)           AS max_price,
       MIN(b.price) FILTER (WHERE b.load_id = d.last_load)                                                                            AS current_price,
       ROUND(AVG(b.price) FILTER (WHERE b.load_id = d.first_load) - AVG(b.price) FILTER (WHERE b.load_id = d.last_load),2)            AS day_diff_avg,
       ROUND((AVG(b.price) FILTER (WHERE b.load_id = d.first_load) / AVG(b.price) FILTER (WHERE b.load_id = d.last_load))*100,2)-100  AS day_trend_avg,
       ROUND(MIN(b.price) FILTER (WHERE b.load_id = d.first_load) - MIN(b.price) FILTER (WHERE b.load_id = d.last_load),2)            AS day_diff_min,
       ROUND((MIN(b.price) FILTER (WHERE b.load_id = d.first_load) / MIN(b.price) FILTER (WHERE b.load_id = d.last_load))*100,2)-100  AS day_trend_min
  FROM raw_data.data_bybit  b
  JOIN raw_data.load_info   li  ON li.id = b.load_id
  JOIN day_load             d   ON d.load_day = li.created_at::DATE AND d.change_type_id = b.change_type_id
 WHERE b.limit_min > 1000
 GROUP BY li.created_at::DATE, b.change_type_id;