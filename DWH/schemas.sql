CREATE SCHEMA dict        AUTHORIZATION anniokassay;
CREATE SCHEMA raw_data    AUTHORIZATION anniokassay;
CREATE SCHEMA fact        AUTHORIZATION anniokassay;
CREATE SCHEMA acquiring   AUTHORIZATION anniokassay;
CREATE SCHEMA report      AUTHORIZATION anniokassay;
CREATE SCHEMA staged_data AUTHORIZATION anniokassay;
 GRANT USAGE ON SCHEMA raw_data TO bybitparser;
 GRANT USAGE ON SCHEMA dict TO tgbot_analitic;
 GRANT USAGE ON SCHEMA report TO tgbot_analitic;