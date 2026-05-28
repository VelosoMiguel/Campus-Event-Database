
-- Basic queries and required coursework queries (examples)
SELECT * FROM student LIMIT 10;
SELECT name, capacity, hourly_cost FROM venue ORDER BY capacity DESC LIMIT 10;
-- Events for organization (replace :org_id)
SELECT * FROM event WHERE organizer_org_id = :org_id ORDER BY start_datetime;
-- Venue availability check (replace :venue_id, :start_dt, :end_dt)
SELECT e.* FROM event e WHERE e.venue_id = :venue_id AND NOT (e.end_datetime <= :start_dt OR e.start_datetime >= :end_dt);
-- Registration summary for popular events
SELECT e.event_id, e.title, COUNT(r.registration_id) AS regs FROM event e LEFT JOIN registration r ON e.event_id = r.event_id GROUP BY e.event_id ORDER BY regs DESC LIMIT 10;
-- Scheduling conflicts per venue
SELECT a.event_id, b.event_id, a.venue_id FROM event a JOIN event b ON a.venue_id = b.venue_id AND a.event_id < b.event_id WHERE NOT (a.end_datetime <= b.start_datetime OR a.start_datetime >= b.end_datetime);
