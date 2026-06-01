CREATE SCHEMA dict        AUTHORIZATION anniokassay;
CREATE SCHEMA raw_data    AUTHORIZATION anniokassay;
 GRANT USAGE ON SCHEMA raw_data TO bybitparser;
CREATE SCHEMA fact        AUTHORIZATION anniokassay;
CREATE SCHEMA acquiring   AUTHORIZATION anniokassay;
CREATE SCHEMA report      AUTHORIZATION anniokassay;
CREATE SCHEMA staged_data AUTHORIZATION anniokassay;