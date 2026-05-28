# Data Dictionary - Campus Event Management System

## Student
| Column | Type | Description |
|--------|------|-------------|
| student_id | INTEGER PK | Unique identifier |
| name | TEXT | Full name |
| email | TEXT UNIQUE | University email |
| role | TEXT | undergraduate, graduate, doctoral |
| enrollment_year | INTEGER | Year of enrollment (2000–2030) |
| major | TEXT | Academic major |

## Faculty
| Column | Type | Description |
|--------|------|-------------|
| faculty_id | INTEGER PK | Unique identifier |
| name | TEXT | Full name |
| email | TEXT UNIQUE | University email |
| department | TEXT | Academic department |
| title | TEXT | Professor, Associate Professor, etc. |
| office_location | TEXT | Office building and room |

## Staff
| Column | Type | Description |
|--------|------|-------------|
| staff_id | INTEGER PK | Unique identifier |
| name | TEXT | Full name |
| email | TEXT UNIQUE | University email |
| department | TEXT | Department |
| position | TEXT | Job position |
| office_location | TEXT | Office location |

## Organization
| Column | Type | Description |
|--------|------|-------------|
| org_id | INTEGER PK | Unique identifier |
| name | TEXT UNIQUE | Organization name |
| description | TEXT | Description |
| founding_date | DATE | Date founded |
| membership_count | INTEGER | Auto-maintained by triggers (trg_membership_insert/delete/update) |
| budget | DECIMAL | Organization budget |
| advisor_id | INTEGER FK | Faculty advisor (references faculty) |

## Venue
| Column | Type | Description |
|--------|------|-------------|
| venue_id | INTEGER PK | Unique identifier |
| name | TEXT UNIQUE | Venue name |
| building | TEXT | Building name |
| capacity | INTEGER | Maximum capacity |
| equipment | TEXT | Available equipment |
| setup_types | TEXT | Available setup configurations |
| hourly_cost | DECIMAL | Cost per hour |
| requires_approval | INTEGER | 1 if booking requires approval |

## Event
| Column | Type | Description |
|--------|------|-------------|
| event_id | INTEGER PK | Unique identifier |
| title | TEXT | Event title |
| description | TEXT | Description |
| event_type | TEXT | academic_conference, workshop, social_event, guest_lecture, athletic_competition, meeting |
| organizer_org_id | INTEGER FK | Organizing student organization (optional) |
| organizer_faculty_id | INTEGER FK | Organizing faculty member (optional) |
| organizer_staff_id | INTEGER FK | Organizing staff member (optional) |
| venue_id | INTEGER FK | Event venue |
| start_datetime | TIMESTAMP | Start time |
| end_datetime | TIMESTAMP | End time (must be after start) |
| expected_attendance | INTEGER | Expected number of attendees |
| requires_registration | INTEGER | 1 if registration is required |
| is_recurring | INTEGER | 1 if event repeats |
| status | TEXT | scheduled, in_progress, completed, cancelled |

## Membership
| Column | Type | Description |
|--------|------|-------------|
| membership_id | INTEGER PK | Unique identifier |
| org_id | INTEGER FK | Organization |
| student_id | INTEGER FK | Student |
| membership_level | TEXT | member, officer, president, vice_president, treasurer, secretary |
| date_joined | DATE | Date of joining |
| is_active | INTEGER | 1 if currently active |

## Registration
| Column | Type | Description |
|--------|------|-------------|
| registration_id | INTEGER PK | Unique identifier |
| event_id | INTEGER FK | Event being registered for |
| participant_id | INTEGER | ID of the participant (student_id, faculty_id, or staff_id) |
| participant_type | TEXT | student, faculty, or staff — determines which table participant_id refers to |
| registration_date | TIMESTAMP | When the registration was made |
| attendance_status | TEXT | registered, attended, no_show, cancelled |
| special_requirements | TEXT | Dietary or accessibility needs |
| registration_fee | DECIMAL | Fee paid for registration |

> **Design note:** `participant_id` does not have a foreign key constraint because participants
> can be students, faculty, or staff — three separate tables. This is a deliberate polymorphic
> association pattern. The `participant_type` column must always be checked alongside
> `participant_id` to resolve the correct table. A future improvement would be a unified
> `person` table to simplify this relationship.