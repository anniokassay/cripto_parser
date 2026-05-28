CREATE SCHEMA dict      AUTHORIZATION anniokassay;
CREATE SCHEMA raw_data  AUTHORIZATION anniokassay;
 GRANT USAGE ON SCHEMA raw_data TO bybitparser;
CREATE SCHEMA fact      AUTHORIZATION anniokassay;
CREATE SCHEMA payment   AUTHORIZATION anniokassay;
CREATE SCHEMA user_data AUTHORIZATION anniokassay;