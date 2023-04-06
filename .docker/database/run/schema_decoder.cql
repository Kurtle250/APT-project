-- noinspection SqlDialectInspectionForFile
DROP KEYSPACE IF EXISTS decoder;
DROP TABLE IF EXISTS decoder.capture;
CREATE KEYSPACE decoder WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'};

-- NOTE: lower case MUST be used for all database keyspace & row names

--     USAGE: location frozen<location>,
CREATE TYPE decoder.location (
    latitude double,
    longitude double,
    altitude double
);

CREATE TABLE decoder.capture (
    id uuid,
    utc_time text,
    location frozen<location>,
    description text,
    wave_location text,
    image_location text,
    PRIMARY KEY (id)
);
