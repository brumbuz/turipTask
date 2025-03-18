CREATE SCHEMA IF NOT EXISTS vasilev_goncharov;
CREATE TABLE IF NOT EXISTS  vasilev_goncharov.Cars (
  id  SERIAL PRIMARY KEY,
  number TEXT NOT NULL,
  stamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS vasilev_goncharov.Drivers (
  id  SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  birthday timestamp NOT NULL,
  balance float4 NOT NULL,
  passport TEXT
);

CREATE TABLE IF NOT EXISTS vasilev_goncharov.Customers (
  id  SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  birthday timestamp NOT NULL,
  balance float4 NOT NULL
);
CREATE TYPE  vasilev_goncharov.trip_status AS ENUM (
    'pending',
    'in_progress',
    'completed',
    'canceled'
);

CREATE TABLE IF NOT EXISTS vasilev_goncharov.Orders (
  id  SERIAL  PRIMARY KEY,
  start_address TEXT NOT NULL,
  final_address TEXT NOT NULL,
  cost float4 NOT NULL,
  order_time timestamp NOT NULL,
  end_time timestamp NOT NULL,
  car_id integer NOT NULL REFERENCES vasilev_goncharov.Cars(id),
  driver_id integer NOT NULL REFERENCES vasilev_goncharov.Drivers(id),
  customer_id integer NOT NULL REFERENCES vasilev_goncharov.Customers(id),
  status vasilev_goncharov.trip_status NOT NULL
);


