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
    condition VARCHAR(3),
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO ALERTS_NEW (
    id,
    created_at,
    is_email,
    is_phone_number,
    latitude,
    longitude,
    location,
    operator,
    threshold,
    condition,
    user_id
) 
SELECT 
    id,
    created_at,
    is_email,
    is_phone_number,
    latitude,
    longitude,
    location,
    operator,
    threshold,
    NULL,
    user_id
FROM ALERTS;

DROP TABLE ALERTS;

ALTER TABLE ALERTS_NEW RENAME TO ALERTS;

COMMIT;