PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL CHECK(role IN ('undergraduate','graduate','doctoral')),
    enrollment_year INTEGER NOT NULL CHECK(enrollment_year BETWEEN 2000 AND 2030),
    major TEXT
);

CREATE TABLE IF NOT EXISTS faculty (
    faculty_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department TEXT,
    title TEXT,
    office_location TEXT
);

CREATE TABLE IF NOT EXISTS staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department TEXT,
    position TEXT,
    office_location TEXT
);

CREATE TABLE IF NOT EXISTS venue (
    venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    building TEXT,
    capacity INTEGER NOT NULL CHECK(capacity > 0),
    equipment TEXT,
    setup_types TEXT,
    hourly_cost DECIMAL DEFAULT 0 CHECK(hourly_cost >= 0),
    requires_approval INTEGER NOT NULL DEFAULT 0 CHECK(requires_approval IN (0,1))
);

CREATE TABLE IF NOT EXISTS organization (
    org_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    founding_date DATE,
    membership_count INTEGER DEFAULT 0 CHECK(membership_count >= 0),
    budget DECIMAL DEFAULT 0 CHECK(budget >= 0),
    advisor_id INTEGER NOT NULL,
    FOREIGN KEY(advisor_id) REFERENCES faculty(faculty_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS event (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    event_type TEXT NOT NULL CHECK(event_type IN ('academic_conference','social_event','workshop','guest_lecture','athletic_competition','meeting')),
    organizer_org_id INTEGER,
    organizer_faculty_id INTEGER,
    organizer_staff_id INTEGER,
    venue_id INTEGER NOT NULL,
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL,
    expected_attendance INTEGER DEFAULT 0 CHECK(expected_attendance >= 0),
    requires_registration INTEGER NOT NULL DEFAULT 0 CHECK(requires_registration IN (0,1)),
    is_recurring INTEGER NOT NULL DEFAULT 0 CHECK(is_recurring IN (0,1)),
    status TEXT NOT NULL DEFAULT 'scheduled' CHECK(status IN ('scheduled','in_progress','completed','cancelled')),
    FOREIGN KEY(organizer_org_id) REFERENCES organization(org_id) ON DELETE SET NULL,
    FOREIGN KEY(organizer_faculty_id) REFERENCES faculty(faculty_id) ON DELETE SET NULL,
    FOREIGN KEY(organizer_staff_id) REFERENCES staff(staff_id) ON DELETE SET NULL,
    FOREIGN KEY(venue_id) REFERENCES venue(venue_id) ON DELETE RESTRICT,
    CHECK(end_datetime > start_datetime)
);

CREATE TABLE IF NOT EXISTS membership (
    membership_id INTEGER PRIMARY KEY AUTOINCREMENT,
    org_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    membership_level TEXT NOT NULL CHECK(membership_level IN ('member','officer','president','vice_president','treasurer','secretary')),
    date_joined DATE DEFAULT (DATE('now')),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN (0,1)),
    UNIQUE(org_id, student_id),
    FOREIGN KEY(org_id) REFERENCES organization(org_id) ON DELETE CASCADE,
    FOREIGN KEY(student_id) REFERENCES student(student_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS registration (
    registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    participant_id INTEGER NOT NULL,
    participant_type TEXT NOT NULL CHECK(participant_type IN ('student','faculty','staff')),
    registration_date TIMESTAMP DEFAULT (DATETIME('now')),
    attendance_status TEXT NOT NULL DEFAULT 'registered' CHECK(attendance_status IN ('registered','attended','no_show','cancelled')),
    special_requirements TEXT,
    registration_fee DECIMAL DEFAULT 0 CHECK(registration_fee >= 0),
    UNIQUE(event_id, participant_id, participant_type),
    FOREIGN KEY(event_id) REFERENCES event(event_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_student_email ON student(email);
CREATE INDEX IF NOT EXISTS idx_faculty_email ON faculty(email);
CREATE INDEX IF NOT EXISTS idx_staff_email ON staff(email);
CREATE INDEX IF NOT EXISTS idx_event_venue_time ON event(venue_id, start_datetime, end_datetime);

CREATE TABLE IF NOT EXISTS _all_emails (email TEXT PRIMARY KEY);

CREATE TRIGGER IF NOT EXISTS trg_student_email_insert AFTER INSERT ON student
BEGIN
    INSERT OR REPLACE INTO _all_emails(email) VALUES (NEW.email);
END;
CREATE TRIGGER IF NOT EXISTS trg_faculty_email_insert AFTER INSERT ON faculty
BEGIN
    INSERT OR REPLACE INTO _all_emails(email) VALUES (NEW.email);
END;
CREATE TRIGGER IF NOT EXISTS trg_staff_email_insert AFTER INSERT ON staff
BEGIN
    INSERT OR REPLACE INTO _all_emails(email) VALUES (NEW.email);
END;
CREATE TRIGGER IF NOT EXISTS trg_student_email_delete AFTER DELETE ON student
BEGIN
    DELETE FROM _all_emails WHERE email = OLD.email;
END;
CREATE TRIGGER IF NOT EXISTS trg_faculty_email_delete AFTER DELETE ON faculty
BEGIN
    DELETE FROM _all_emails WHERE email = OLD.email;
END;
CREATE TRIGGER IF NOT EXISTS trg_staff_email_delete AFTER DELETE ON staff
BEGIN
    DELETE FROM _all_emails WHERE email = OLD.email;
END;
-- ============================================================
-- MEMBERSHIP COUNT TRIGGERS
-- Keeps organization.membership_count in sync automatically
-- ============================================================

CREATE TRIGGER IF NOT EXISTS trg_membership_insert
AFTER INSERT ON membership
WHEN NEW.is_active = 1
BEGIN
    UPDATE organization
    SET membership_count = membership_count + 1
    WHERE org_id = NEW.org_id;
END;

CREATE TRIGGER IF NOT EXISTS trg_membership_delete
AFTER DELETE ON membership
WHEN OLD.is_active = 1
BEGIN
    UPDATE organization
    SET membership_count = membership_count - 1
    WHERE org_id = OLD.org_id;
END;

CREATE TRIGGER IF NOT EXISTS trg_membership_update
AFTER UPDATE OF is_active ON membership
BEGIN
    UPDATE organization
    SET membership_count = membership_count + (NEW.is_active - OLD.is_active)
    WHERE org_id = NEW.org_id;
END;