import sqlite3

def connect():
    return sqlite3.connect("campus_events.db")

def show_students(limit=10):
    """Show all students."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT student_id, name, email, role, major FROM student LIMIT ?", (limit,))
    rows = cur.fetchall()
    print(f"\n{'ID':<5} {'Name':<25} {'Email':<35} {'Role':<15} {'Major'}")
    print("-" * 90)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<25} {row[2]:<35} {row[3]:<15} {row[4] or 'N/A'}")
    conn.close()

def show_events(limit=10):
    """Show upcoming or recent events with venue info."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.event_id, e.title, e.event_type, e.status,
               v.name AS venue, e.start_datetime, e.expected_attendance
        FROM event e
        JOIN venue v ON e.venue_id = v.venue_id
        ORDER BY e.start_datetime DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    print(f"\n{'ID':<5} {'Title':<30} {'Type':<20} {'Status':<12} {'Venue':<20} {'Start':<20} {'Expected'}")
    print("-" * 115)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<30} {row[2]:<20} {row[3]:<12} {row[4]:<20} {row[5]:<20} {row[6]}")
    conn.close()

def show_venue_availability(venue_id, start_dt, end_dt):
    """Check if a venue is available in a given time window."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.event_id, e.title, e.start_datetime, e.end_datetime
        FROM event e
        WHERE e.venue_id = ?
          AND NOT (e.end_datetime <= ? OR e.start_datetime >= ?)
          AND e.status NOT IN ('cancelled')
    """, (venue_id, start_dt, end_dt))
    rows = cur.fetchall()
    if rows:
        print(f"\n⚠️  Venue {venue_id} has conflicts:")
        for row in rows:
            print(f"  Event {row[0]}: {row[1]} ({row[2]} → {row[3]})")
    else:
        print(f"\n✅ Venue {venue_id} is available from {start_dt} to {end_dt}")
    conn.close()

def show_registration_summary(limit=10):
    """Show events ranked by number of registrations."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.event_id, e.title, COUNT(r.registration_id) AS registrations
        FROM event e
        LEFT JOIN registration r ON e.event_id = r.event_id
        GROUP BY e.event_id
        ORDER BY registrations DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    print(f"\n{'ID':<5} {'Title':<35} {'Registrations'}")
    print("-" * 55)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<35} {row[2]}")
    conn.close()

def show_org_members(org_id):
    """Show all active members of an organization."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.name, s.email, m.membership_level, m.date_joined
        FROM membership m
        JOIN student s ON m.student_id = s.student_id
        WHERE m.org_id = ? AND m.is_active = 1
        ORDER BY m.membership_level
    """, (org_id,))
    rows = cur.fetchall()
    print(f"\nActive members of organization {org_id}:")
    print(f"{'Name':<25} {'Email':<35} {'Level':<15} {'Joined'}")
    print("-" * 85)
    for row in rows:
        print(f"{row[0]:<25} {row[1]:<35} {row[2]:<15} {row[3]}")
    conn.close()


if __name__ == "__main__":
    print("=== Campus Event Management System Explorer ===")
    show_students()
    show_events()
    show_registration_summary()