-- Create a new table with the desired schema
BEGIN TRANSACTION;

CREATE TABLE ALERTS_NEW (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_email BOOLEAN NOT NULL,
    is_phone_number BOOLEAN NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    location VARCHAR(255) NOT NULL,
    operator VARCHAR(3),
    threshold REAL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 2. Copy all existing data over
INSERT INTO ALERTS_NEW SELECT * FROM ALERTS;

-- 3. Drop the old table
DROP TABLE ALERTS;

-- 4. Rename the new table
ALTER TABLE ALERTS_NEW RENAME TO ALERTS;

COMMIT;