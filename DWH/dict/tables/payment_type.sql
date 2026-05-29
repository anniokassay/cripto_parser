CREATE TABLE dict.payment_type (
	id        		INT     NOT NULL,
  load_type_id  INT     NOT NULL,
  pt_int        INT,
  pt_text       TEXT,
  code          VARCHAR(16) NOT NULL,
  description   VARCHAR(256),
  
	CONSTRAINT payment_type_pk PRIMARY KEY (id),
  CONSTRAINT payment_type_load_fk FOREIGN KEY (load_type_id) REFERENCES dict.load_type(id)
);
CREATE INDEX payment_type_load_ptint_idx ON dict.payment_type (load_type_id, pt_int) WHERE pt_int IS NOT NULL;
CREATE INDEX payment_type_load_pttext_idx ON dict.payment_type (load_type_id, pt_text) WHERE pt_text IS NOT NULL;