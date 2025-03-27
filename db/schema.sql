-- Drop tables in reverse order of creation
DROP TABLE IF EXISTS file_uploads;
DROP TABLE IF EXISTS candidates;
DROP TABLE IF EXISTS uploads;
DROP TABLE IF EXISTS common_wrong_answers;
DROP TABLE IF EXISTS answer_keys;
DROP TABLE IF EXISTS versions;
DROP TABLE IF EXISTS examiner_availability;
DROP TABLE IF EXISTS examiners;
DROP TABLE IF EXISTS examiner_roles;
DROP TABLE IF EXISTS centre_contacts;
DROP TABLE IF EXISTS centres;
DROP TABLE IF EXISTS languages;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS language_families;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS examiner_payment_rates
DROP TABLE IF EXISTS candidate_feedback;

-- Create tables
CREATE TABLE IF NOT EXISTS candidate_feedback (
    bandscore TEXT PRIMARY KEY,
    listening_feedback TEXT,
    reading_feedback TEXT,
    writing_feedback TEXT
);

CREATE TABLE IF NOT EXISTS examiner_payment_rates ( -- NEED TO FIX THIS
    rate_id INT PRIMARY KEY,
    location TEXT,
    currency CHAR(3),
    component CHAR(2),
    item TEXT,
    rate NUMERIC(10,2),
    unit TEXT,
    holiday_rate DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS sessions (
    session_id INT NOT NULL,
    session_name VARCHAR(50) NOT NULL,
    session_start DATE NOT NULL,
    session_end DATE NOT NULL,
    session_upload_destination TEXT,
    PRIMARY KEY (session_id)
);

CREATE TABLE IF NOT EXISTS language_families (
    language_fam_id INT NOT NULL,
    language_family TEXT NOT NULL,
    PRIMARY KEY (language_fam_id)
);

CREATE TABLE IF NOT EXISTS countries (
    country_id INT NOT NULL,
    country TEXT NOT NULL,
    language_fam_id INT NOT NULL,
    PRIMARY KEY (country_id),
    FOREIGN KEY (language_fam_id) REFERENCES language_families(language_fam_id)
);

CREATE TABLE IF NOT EXISTS languages (
    language_id INT NOT NULL, -- get L1 codes from faq
    language TEXT NOT NULL,
    language_fam_id INT NOT NULL,
    PRIMARY KEY (language_id),
    FOREIGN KEY (language_fam_id) REFERENCES language_families(language_fam_id)
);

CREATE TABLE IF NOT EXISTS centres (
    centre_id CHAR(4) NOT NULL CHECK (centre_id ~ '^[0-9]{4}$'),
    live_centre_number VARCHAR(7),
    centre_name TEXT NOT NULL,
    address_1 TEXT,
    address_2 TEXT,
    address_3 TEXT,
    address_4 TEXT,
    address_5 TEXT,
    country_id INT NOT NULL,
    phone_number TEXT,
    PRIMARY KEY (centre_id),
    FOREIGN KEY (country_id) REFERENCES countries(country_id)
);

CREATE TABLE IF NOT EXISTS centre_contacts (
    centre_contact_id SERIAL PRIMARY KEY,
    centre_id TEXT NOT NULL,
    contact_name TEXT NOT NULL,
    contact_email TEXT NOT NULL,
    primary_contact BOOLEAN,
    FOREIGN KEY centre_id REFERENCES centres(centre_id)
)

CREATE TABLE IF NOT EXISTS examiner_roles (
    examiner_role_id SERIAL PRIMARY KEY,
    examiner_role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS examiners (
    examiner_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    contact_email TEXT NOT NULL,
    as_id INT NOT NULL,
    country TEXT,
    currency TEXT,
    examiner_role_id INT NOT NULL,
    contract_signed TEXT,
    active BOOLEAN,
    FOREIGN KEY (examiner_role_id) REFERENCES examiner_roles(examiner_role_id)
);

CREATE TABLE IF NOT EXISTS examiner_availability (
    week_id SERIAL PRIMARY KEY,
    examiner_id INT NOT NULL,
    week_beginning DATE NOT NULL,
    week_ending DATE NOT NULL,
    scripts_per_week INT DEFAULT 0,
    remaining_scripts INT DEFAULT 0,
    FOREIGN KEY (examiner_id) REFERENCES examiners(examiner_id)
);

CREATE TABLE IF NOT EXISTS versions (
    version_id TEXT GENERATED ALWAYS AS (paper || LEFT(component, 1) || version_name) STORED,
    paper VARCHAR(2) DEFAULT '', -- AC or GT
    component TEXT NOT NULL, -- 'Reading', 'Listening' or 'Writing'
    version_name TEXT NOT NULL,
    report_writer_1 INT,
    report_writer_2 INT,
    back_up_examiner_1 INT,
    back_up_examiner_2 INT,
    PRIMARY KEY (version_id),
    FOREIGN KEY (report_writer_1) REFERENCES examiners(examiner_id),
    FOREIGN KEY (report_writer_2) REFERENCES examiners(examiner_id),
    FOREIGN KEY (back_up_examiner_1) REFERENCES examiners(examiner_id),
    FOREIGN KEY (back_up_examiner_2) REFERENCES examiners(examiner_id)
);

CREATE TABLE IF NOT EXISTS answer_keys (
    answer_id TEXT GENERATED ALWAYS AS (version_id || '-' || CAST(question_number AS TEXT)) STORED,
    version_id TEXT NOT NULL,
    question_number INT NOT NULL,
    answer TEXT NOT NULL,
    productive_answer BOOLEAN,
    anchor_question BOOLEAN NOT NULL,
    ccf_code CHAR(1) NOT NULL,
    PRIMARY KEY (answer_id),
    FOREIGN KEY (version_id) REFERENCES versions(version_id)
);

CREATE TABLE IF NOT EXISTS common_wrong_answers (
    cwa_id SERIAL PRIMARY KEY,
    version_id TEXT NOT NULL,
    answer_id TEXT NOT NULL,
    wrong_answer TEXT NOT NULL,
    FOREIGN KEY (version_id) REFERENCES versions(version_id),
    FOREIGN KEY (answer_id) REFERENCES answer_keys(answer_id)
);

CREATE TABLE IF NOT EXISTS uploads (
    upload_id TEXT GENERATED ALWAYS AS (session_id || '-' || centre_id || '-' || part_delivery) STORED,
    session_id INT NOT NULL,
    centre_id CHAR(4) NOT NULL CHECK (centre_id ~ '^[0-9]{4}$'),
    part_delivery VARCHAR(2) NOT NULL,
    epd_number CHAR(9),
    test_date DATE,
    upload_date DATE DEFAULT CURRENT_DATE,
    upload_correct BOOLEAN DEFAULT FALSE,
    booked_in_date DATE,
    sent_date DATE,
    PRIMARY KEY (upload_id),
    UNIQUE (session_id, centre_id, part_delivery),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (centre_id) REFERENCES centres(centre_id)
);

CREATE TABLE IF NOT EXISTS candidates (
    candidate_id TEXT GENERATED ALWAYS AS (upload_id || '-' || LPAD(candidate_number::TEXT, 4, '0')) STORED,
    upload_id TEXT NOT NULL,
    candidate_number INT NOT NULL,
    candidate_name TEXT NOT NULL,
    paper_sat CHAR(2), -- 'AC' or 'GT'
    language_id INT,
    writing_version_id TEXT, -- construct with paper_sat, 'W', version_name
    reading_version_id TEXT, -- construct with paper_sat, 'R', version_name
    listening_version_id TEXT, -- 'L', version_name
    examiner_id INT,
    reading_responses TEXT,
    listening_responses TEXT,
    writing_t1_ta INT,
    writing_t1_cc INT,
    writing_t1_lr INT,
    writing_t1_gra INT,
    writing_t2_ta INT,
    writing_t2_cc INT,
    writing_t2_lr INT,
    writing_t2_gra INT,
    PRIMARY KEY (candidate_id),
    FOREIGN KEY (upload_id) REFERENCES uploads(upload_id),
    FOREIGN KEY (language_id) REFERENCES languages(language_id),
    FOREIGN KEY (writing_version_id) REFERENCES versions(version_id),
    FOREIGN KEY (reading_version_id) REFERENCES versions(version_id),
    FOREIGN KEY (listening_version_id) REFERENCES versions(version_id),
    FOREIGN KEY (examiner_id) REFERENCES examiners(examiner_id)
);

CREATE TABLE IF NOT EXISTS file_uploads (
    file_upload_id SERIAL PRIMARY KEY,
    upload_id TEXT NOT NULL,
    version_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    is_rescan BOOLEAN,
    FOREIGN KEY (upload_id) REFERENCES uploads(upload_id),
    FOREIGN KEY (version_id) REFERENCES versions(version_id)
);
