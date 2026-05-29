-- Заполнение таблицы за период 2026-05-27..2026-06-26:
-- 7500 случайных записей на каждый день.
INSERT INTO acquiring.output_transaction (
    operation_status,
    source_system_id,
    change_type_id,
    source_account_id,
    gateway_code,
    transaction_ts,
    description,
    is_verified,
    oper_amount,
    hold_amount
)
SELECT
    (ARRAY['NEW', 'PROCESSING', 'DONE', 'FAILED'])[floor(random() * 4 + 1)]::varchar(32)          AS operation_status,
    floor(random() * 2 + 1)::bigint                                                                  AS source_system_id, -- 1..2
    floor(random() * 5 + 1)::int                                                                     AS change_type_id,   -- 1..5
    floor(random() * 1000000000 + 1)::bigint                                                         AS source_account_id,
    'GW-' || upper(substr(md5(random()::text), 1, 8))                                                AS gateway_code,
    (d.dt::timestamp + (random() * interval '1 day'))::timestamptz                                   AS transaction_ts,
    'Auto generated transaction'                                                                      AS description,
    (random() >= 0.5)                                                                                 AS is_verified,
    round((random() * 100000)::numeric, 2)                                                           AS oper_amount,
    round((random() * 10000)::numeric, 2)                                                            AS hold_amount
FROM generate_series('2026-05-27'::date, '2026-06-26'::date, interval '1 day') AS d(dt)
CROSS JOIN generate_series(1, 7500) AS n(i);