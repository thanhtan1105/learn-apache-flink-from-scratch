-- CREATE DATABASE  finance_db;
CREATE SCHEMA IF NOT EXISTS public;

create table stock_transaction
(
    event_time     timestamp      not null,
    ticker         varchar(10)    not null,
    price          numeric(10, 2) not null,
    volume         integer        not null,
    open_price     double precision,
    high           double precision,
    low            double precision,
    close_price    double precision,
    adjusted_close double precision
);
