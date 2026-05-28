CREATE OR REPLACE FUNCTION payment.create_uuid()
RETURNS UUID AS $$
DECLARE
    raw_uuid TEXT := md5(random()::text || clock_timestamp()::text);
    uuid_text TEXT;
BEGIN
    uuid_text :=
        substr(raw_uuid, 1, 8) || '-' ||
        substr(raw_uuid, 9, 4) || '-' ||
        '4' || substr(raw_uuid, 14, 3) || '-' ||
        (ARRAY['8', '9', 'a', 'b'])[floor(random() * 4 + 1)::int] || substr(raw_uuid, 18, 3) || '-' ||
        substr(raw_uuid, 21, 12);

    RETURN uuid_text::uuid;
END;
$$ LANGUAGE plpgsql;