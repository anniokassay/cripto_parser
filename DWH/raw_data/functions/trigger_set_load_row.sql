
CREATE OR REPLACE FUNCTION raw_data.set_load_type_row()
RETURNS TRIGGER AS $$
DECLARE
    v_load_type_row BIGINT;
BEGIN
    SELECT COALESCE(MAX(load_type_row), 0) + 1 INTO v_load_type_row 
    FROM raw_data.load_info
    WHERE load_type = NEW.load_type;

    NEW.load_type_row := v_load_type_row;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tr_set_load_type_row ON raw_data.load_info;

CREATE TRIGGER tr_set_load_type_row
BEFORE INSERT ON raw_data.load_info
FOR EACH ROW
EXECUTE FUNCTION raw_data.set_load_type_row();

