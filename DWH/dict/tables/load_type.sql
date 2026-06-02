CREATE TABLE dict.load_type (
	id        		int           NOT NULL,
	codename  		varchar       NOT NULL,
	URL_adress    varchar(256)  NOT NULL,
	source_name		varchar(256)  NOT NULL,
	CONSTRAINT load_type_pk PRIMARY KEY (id)
);
GRANT SELECT ON ALL TABLES IN SCHEMA dict TO grafana;