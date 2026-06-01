CREATE OR REPLACE FUNCTION day_load_id(pi_date DATE)
RETURNS BIGINT
IMMUTABLE
LANGUAGE SQL
AS $$
    SELECT MIN(load_id)::BIGINT
    FROM raw_data.load_info
    WHERE created_at::DATE = pi_date;
$$;