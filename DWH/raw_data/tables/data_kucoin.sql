-- DROP TABLE raw_data.data_kucoin;

CREATE TABLE raw_data.data_kucoin (
  change_type_id  INT             NOT NULL,
  seller          varchar(255)    NOT NULL,
  price           numeric(18, 2)  NOT NULL,
  limit_min       numeric(18, 2)  NOT NULL,
  limit_max       numeric(18, 2)  NOT NULL,
  payments        jsonb           NOT NULL,
  load_id         BIGINT          NOT NULL,
  
  CONSTRAINT data_kucoin_load_fk FOREIGN KEY (load_id) REFERENCES raw_data.load_info(id),
  CONSTRAINT data_kucoin_dict_fk FOREIGN KEY (change_type_id) REFERENCES dict.change_type(id)
);

GRANT INSERT ON TABLE raw_data.data_kucoin TO bybitparser;