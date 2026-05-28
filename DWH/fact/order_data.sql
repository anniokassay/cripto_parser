CREATE TABLE fact.order_data (
  order_id          BIGINT        NOT NULL,
  transaction_uuid  UUID,
  price             NUMERIC(20,2) NOT NULL,
  fee_amount        NUMERIC(20,2),
  change_type       INT,

  
	CONSTRAINT order_data_pk PRIMARY KEY (order_id),  
  CONSTRAINT order_data_output_transaction_fk FOREIGN KEY (transaction_uuid) REFERENCES payment.output_transaction(transaction_uuid)
);