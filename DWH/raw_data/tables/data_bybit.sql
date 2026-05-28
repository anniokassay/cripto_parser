-- DROP TABLE raw_data.data_bybit;

CREATE TABLE raw_data.data_bybit (
  change_type_id  INT             NOT NULL,
  seller          varchar(255)    NOT NULL,
  price           numeric(18, 2)  NOT NULL,
  limit_min       numeric(18, 2)  NOT NULL,
  limit_max       numeric(18, 2)  NOT NULL,
  payments        jsonb           NOT NULL,
  load_id         BIGINT          NOT NULL,
  
  --CONSTRAINT data_bybit_load_fk FOREIGN KEY (load_id) REFERENCES raw_data.load_info(id), -- таблица секционирована
  CONSTRAINT data_bybit_dict_fk FOREIGN KEY (change_type_id) REFERENCES dict.change_type(id)
);
CREATE INDEX data_bybit_load_id_idx ON raw_data.data_bybit(load_id);

GRANT INSERT ON TABLE raw_data.data_bybit TO bybitparser;