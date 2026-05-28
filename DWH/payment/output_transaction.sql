CREATE TABLE payment.output_transaction (
    transaction_uuid    uuid        DEFAULT payment.create_uuid() NOT NULL,
    operation_status    varchar(32),
    source_system_id    BIGINT NOT NULL,
    change_type_id      INT NOT NULL,
    source_account_id   BIGINT NOT NULL,
    gateway_code        varchar NOT NULL,
    transaction_ts      timestamptz DEFAULT clock_timestamp() NOT NULL,
    description         varchar,
    is_verified         BOOLEAN     DEFAULT FALSE,
    oper_amount         NUMERIC(20,2),
    hold_amount         NUMERIC(20,2),
    
	CONSTRAINT output_transaction_pk PRIMARY KEY (transaction_uuid),  
  CONSTRAINT output_transaction_dict_fk FOREIGN KEY (change_type_id) REFERENCES dict.change_type(id)
);

  CREATE INDEX output_transaction_sys_ch_idx ON payment.output_transaction(source_system_id,change_type_id,transaction_uuid);