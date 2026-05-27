CREATE TABLE dict.change_type (
	id        		int     NOT NULL,
	codename  		varchar NOT NULL,
	currency_out	varchar(6) NOT NULL,
	currency_gain	varchar(6) NOT NULL,

	CONSTRAINT change_type_pk PRIMARY KEY (id)
);
