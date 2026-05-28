# Business Rules - Campus Event Management System

## Student
- Each student must have a unique email address.
- Role must be one of: undergraduate, graduate, doctoral.
- Enrollment year must be a valid integer.
- A student can belong to multiple organizations but only one membership per organization.

## Faculty
- Each faculty member must have a unique email address.
- Can act as advisor for multiple organizations.

## Staff
- Each staff member must have a unique email address.

## Organization
- Each organization must have exactly one faculty advisor.
- Membership count must match the number of active members.
- Budget must be a non-negative decimal number.

## Venue
- Capacity must be a positive integer.
- Hourly cost must be a positive decimal number.
- Some venues require approval for booking.
- Available equipment and setup types must be defined.

## Event
- End time must be after start time.
- Expected attendance must not exceed venue capacity.
- Event type must be from a predefined list (academic_conference, workshop, social_event, etc.).
- Event status must be one of: scheduled, in_progress, completed, cancelled.
- Recurring events should be handled consistently.

## Membership
- Membership level must be one of: member, officer, president.
- Active membership must reflect whether the student currently participates.

## Registration
- A participant can only register once per event.
- Attendance status must be: registered, attended, no_show, cancelled.
- Participant type must be one of: student, faculty, staff.
- Registration count cannot exceed venue capacity.
- Special requirements (dietary, accessibility) must be documented if needed.
