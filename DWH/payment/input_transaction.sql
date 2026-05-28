CREATE TABLE payment.input_transaction (
    transaction_uuid    uuid NOT NULL,
    source_system_id    BIGINT NOT NULL,
    transaction_ts      timestamptz DEFAULT clock_timestamp() NOT NULL,
    description         varchar,
    commited_amount     NUMERIC(20,2),
    
	CONSTRAINT input_transaction_pk PRIMARY KEY (transaction_uuid)
);

  CREATE INDEX input_transaction_uuid_idx ON payment.input_transaction(transaction_uuid);