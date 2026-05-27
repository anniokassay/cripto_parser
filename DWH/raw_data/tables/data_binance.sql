-- DROP TABLE raw_data.data_binance;

CREATE TABLE raw_data.data_binance (
  change_type_id  INT             NOT NULL,
  seller          varchar(255)    NOT NULL,
  price           numeric(18, 2)  NOT NULL,
  limit_min       numeric(18, 2)  NOT NULL,
  limit_max       numeric(18, 2)  NOT NULL,
  payments        jsonb           NOT NULL,
  load_id         BIGINT          NOT NULL,
  
  CONSTRAINT data_binance_load_fk FOREIGN KEY (load_id) REFERENCES raw_data.load_info(id),
  CONSTRAINT data_binance_dict_fk FOREIGN KEY (change_type_id) REFERENCES dict.change_type(id)
);

GRANT INSERT ON TABLE raw_data.data_binance TO bybitparser;