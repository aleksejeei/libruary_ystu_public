CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    rdr_name TEXT,
    rdr_id TEXT,
    info TEXT,
    privacy INTEGER,
    date_accept TIMESTAMP
);