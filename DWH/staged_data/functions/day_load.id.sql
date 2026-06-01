CREATE OR REPLACE FUNCTION staged_data.day_load_id(pi_date DATE)
RETURNS BIGINT
LANGUAGE sql
STABLE
AS $$
    SELECT MIN(id)::BIGINT
    FROM raw_data.load_info
    WHERE created_at >= pi_date::TIMESTAMPTZ;
$$;