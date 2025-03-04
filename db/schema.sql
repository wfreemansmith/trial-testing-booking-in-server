DROP TABLE IF EXISTS uploads;

CREATE TABLE uploads (
    upload_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    centre_id INTEGER NOT NULL,
    part_delivery TEXT DEFAULT 'A',
    epd_number TEXT,
    test_date TEXT,
    upload_date TEXT CURRENT_TIMESTAMP,
    upload_correct BOOL,
    booked_in_date TEXT,
    sent_date TEXT
);    
