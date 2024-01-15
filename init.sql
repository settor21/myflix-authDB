-- init.sql
CREATE USER amedikusettor WITH PASSWORD 'admin';
CREATE DATABASE myflix-access;
GRANT ALL PRIVILEGES ON DATABASE myflix-access TO amedikusettor;
