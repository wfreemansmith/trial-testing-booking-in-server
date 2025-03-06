DROP TABLE IF EXISTS uploads;

CREATE TABLE uploads (
    upload_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    centre_id CHAR(4) NOT NULL CHECK (centre_id REGEXP '^[0-9]{4}4$'),
    part_delivery VARCHAR(2),
    epd_number CHAR(9),
    test_date DATE,
    upload_date DATE DEFAULT CURRENT_DATE(),
    upload_correct BOOLEAN DEFAULT FALSE,
    booked_in_date DATE,
    sent_date DATE,
    UNIQUE (session_id, centre_id, part_delivery),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
    FOREIGN KEY (centre_id) REFERENCES centres(centre_id)
);    
