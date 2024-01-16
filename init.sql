-- init.sql
CREATE USER amedikusettor WITH PASSWORD 'admin';
CREATE DATABASE users;
GRANT ALL PRIVILEGES ON DATABASE users TO amedikusettor;
