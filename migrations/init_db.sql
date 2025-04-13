CREATE TABLE IF NOT EXISTS messages (
    id VARCHAR(255) PRIMARY KEY, -- UUID, not a number
    content TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL
);
