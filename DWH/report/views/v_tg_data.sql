CREATE OR REPLACE VIEW report.v_tg_data 
AS
SELECT CONCAT_WS('    ', currency_out, currency_gain,change_rate,source_name,seller_name) AS currency_info, 
       from_ts, 
       change_type_id,
       change_rate
  FROM staged_data.exchange_offer_current;


GRANT SELECT ON TABLE report.v_tg_data TO tgbot_analitic;