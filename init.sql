CREATE USER pyhr_api WITH PASSWORD 'pyhr123';
GRANT ALL PRIVILEGES ON DATABASE pyhr TO pyhr_api;
GRANT pg_read_all_data TO pyhr_api;
GRANT pg_write_all_data TO pyhr_api;
GRANT ALL ON SCHEMA public to "pyhr_api";