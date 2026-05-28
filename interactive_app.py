import sqlite3
import os
from datetime import datetime
from pathlib import Path
import sys
import customtkinter as ctk
from tkinter import scrolledtext, messagebox
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class EventManagementGUI:
    """Campus Event Management System"""
    
    def __init__(self, root, db_path='campus_events.db'):
        self.root = root
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
        self.root.title("Campus Event Management System")
        self.root.geometry("1400x800")
        self.root.resizable(True, True)
        
        self.connect_database()
        self.create_ui()
    
    def connect_database(self):
        """Connect to database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error connecting to database: {e}")
            sys.exit(1)
    
    def close_database(self):
        """Close connection"""
        if self.conn:
            self.conn.close()
    
    def create_ui(self):
        """Create modern UI"""
        # Main container
        main_frame = ctk.CTkFrame(self.root, fg_color="#1a1a1a")
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Header with title
        header_frame = ctk.CTkFrame(main_frame, fg_color="#0d1b2a", height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header_frame, 
            text="🎓 Campus Event Management System",
            font=("Segoe UI", 24, "bold"),
            text_color="#00a8ff"
        )
        title.pack(pady=20)
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Manage events, organizations, students, and venues",
            font=("Segoe UI", 12),
            text_color="#a0a0a0"
        )
        subtitle.pack(pady=(0, 10))
        
        # Content frame with notebook tabs
        content_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create custom tab buttons
        self.create_tab_navigation(content_frame)
    
    def create_tab_navigation(self, parent):
        """Create tab navigation system"""
        nav_frame = ctk.CTkFrame(parent, fg_color="#252525", corner_radius=10)
        nav_frame.pack(fill="x", padx=0, pady=(0, 20))
        
        self.tab_buttons = {}
        self.tab_contents = {}
        
        tabs = [
            ("Students", self.create_students_tab),
            ("Events", self.create_events_tab),
            ("Organizations", self.create_organizations_tab),
            ("Venues", self.create_venues_tab),
            ("Statistics", self.create_statistics_tab),
            ("Faculty & Staff", self.create_faculty_tab)
        ]
        
        for i, (tab_name, tab_creator) in enumerate(tabs):
            btn = ctk.CTkButton(
                nav_frame,
                text=tab_name,
                font=("Segoe UI", 12, "bold"),
                fg_color="#0066cc" if i == 0 else "#3a3a3a",
                text_color="white",
                hover_color="#0052a3",
                command=lambda name=tab_name, creator=tab_creator: self.switch_tab(name, creator)
            )
            btn.pack(side="left", padx=8, pady=12)
            self.tab_buttons[tab_name] = btn
        
        # Content area
        self.content_area = ctk.CTkFrame(parent, fg_color="#252525", corner_radius=10)
        self.content_area.pack(fill="both", expand=True, padx=0, pady=0)
        
        self.current_tab = None
        self.switch_tab("Students", self.create_students_tab)
    
    def switch_tab(self, tab_name, tab_creator):
        """Switch between tabs"""
        # Update button colors
        for btn_name, btn in self.tab_buttons.items():
            if btn_name == tab_name:
                btn.configure(fg_color="#0066cc")
            else:
                btn.configure(fg_color="#3a3a3a")
        
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        self.current_tab = tab_name
        tab_creator(self.content_area)
    
    # ==================== STUDENTS TAB ====================
    def create_students_tab(self, parent):
        """Create students tab"""
        # Main container with two sections
        main_container = ctk.CTkFrame(parent, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # TOP SECTION: Search and Add (smaller)
        top_section = ctk.CTkFrame(main_container, fg_color="#1a1a1a", corner_radius=8)
        top_section.pack(fill="x", padx=0, pady=(0, 10), ipady=10)
        
        # Search section
        search_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(search_frame, text="Search Student:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=5, pady=5)
        
        self.student_search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.student_search_var,
            placeholder_text="Enter email...",
            width=200,
            height=32
        )
        search_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            search_frame,
            text="🔍 Search",
            command=self.search_student_gui,
            width=90,
            height=32,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=3)
        
        ctk.CTkButton(
            search_frame,
            text="📋 List All",
            command=self.list_students_gui,
            width=90,
            height=32,
            font=("Segoe UI", 10, "bold"),
            fg_color="#00a850"
        ).pack(side="left", padx=3)
        
        # Add student section (compact)
        add_frame = ctk.CTkFrame(top_section, fg_color="transparent")
        add_frame.pack(fill="x", padx=15, pady=(5, 10))
        
        title_label = ctk.CTkLabel(add_frame, text="Add New Student:", font=("Segoe UI", 11, "bold"))
        title_label.pack(side="left", padx=5, pady=5)
        
        # Form in horizontal layout
        self.add_student_name = ctk.CTkEntry(add_frame, placeholder_text="Name", width=120, height=32)
        self.add_student_name.pack(side="left", padx=3)
        
        self.add_student_email = ctk.CTkEntry(add_frame, placeholder_text="Email", width=140, height=32)
        self.add_student_email.pack(side="left", padx=3)
        
        self.add_student_role = ctk.CTkComboBox(
            add_frame,
            values=["undergraduate", "graduate", "doctoral"],
            width=120,
            height=32
        )
        self.add_student_role.set("undergraduate")
        self.add_student_role.pack(side="left", padx=3)
        
        self.add_student_year = ctk.CTkEntry(add_frame, placeholder_text="Year", width=80, height=32)
        self.add_student_year.pack(side="left", padx=3)
        
        self.add_student_major = ctk.CTkEntry(add_frame, placeholder_text="Major", width=120, height=32)
        self.add_student_major.pack(side="left", padx=3)
        
        ctk.CTkButton(
            add_frame,
            text="✅ Add",
            command=self.add_student_gui,
            width=80,
            height=32,
            font=("Segoe UI", 10, "bold"),
            fg_color="#00a850"
        ).pack(side="left", padx=3)
        
        # BOTTOM SECTION: Results table (much larger)
        table_frame = ctk.CTkFrame(main_container, fg_color="#1a1a1a", corner_radius=8)
        table_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        ctk.CTkLabel(table_frame, text="Students List", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Create treeview for students
        from tkinter import ttk
        
        tree_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        columns = ("ID", "Name", "Email", "Role", "Year", "Major")
        self.students_tree = ttk.Treeview(tree_frame, columns=columns, height=30, show="headings", style="Custom.Treeview")
        
        # Configure custom treeview style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview", background="#2a2a2a", foreground="#ffffff", fieldbackground="#2a2a2a", borderwidth=0, rowheight=32)
        style.configure("Custom.Treeview.Heading", background="#0066cc", foreground="#ffffff", borderwidth=1, font=("Segoe UI", 11, "bold"))
        style.map('Custom.Treeview', background=[('selected', '#0066cc')], foreground=[('selected', '#ffffff')])
        
        for col in columns:
            self.students_tree.column(col, width=210, anchor="w")
            self.students_tree.heading(col, text=col)
        
        # Add both vertical and horizontal scrollbars
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.students_tree.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.students_tree.xview)
        self.students_tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)
        
        self.students_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def list_students_gui(self):
        """List all students"""
        self.students_tree.delete(*self.students_tree.get_children())
        try:
            self.cursor.execute("SELECT * FROM student ORDER BY student_id")
            students = self.cursor.fetchall()
            
            for i, s in enumerate(students):
                # Alternate row colors for better readability
                tag = "oddrow" if i % 2 == 0 else "evenrow"
                self.students_tree.insert("", "end", values=(s[0], s[1], s[2], s[3], s[4], s[5] or ""), tags=(tag,))
            
            # Configure tag colors
            self.students_tree.tag_configure("oddrow", background="#2a2a2a")
            self.students_tree.tag_configure("evenrow", background="#1f1f1f")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error listing students: {e}")
    
    def search_student_gui(self):
        """Search student by email"""
        email = self.student_search_var.get().strip()
        if not email:
            messagebox.showwarning("Warning", "Enter an email to search")
            return
        
        self.students_tree.delete(*self.students_tree.get_children())
        try:
            self.cursor.execute("SELECT * FROM student WHERE email LIKE ?", (f"%{email}%",))
            students = self.cursor.fetchall()
            
            if not students:
                messagebox.showinfo("Info", "No students found")
                return
            
            for i, s in enumerate(students):
                tag = "oddrow" if i % 2 == 0 else "evenrow"
                self.students_tree.insert("", "end", values=(s[0], s[1], s[2], s[3], s[4], s[5] or ""), tags=(tag,))
            
            self.students_tree.tag_configure("oddrow", background="#2a2a2a", foreground="#ffffff")
            self.students_tree.tag_configure("evenrow", background="#1f1f1f", foreground="#ffffff")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Search error: {e}")
    
    def add_student_gui(self):
        """Add new student"""
        name = self.add_student_name.get().strip()
        email = self.add_student_email.get().strip()
        role = self.add_student_role.get()
        year = self.add_student_year.get().strip()
        major = self.add_student_major.get().strip() or None
        
        if not all([name, email, role, year]):
            messagebox.showwarning("Warning", "Fill all required fields")
            return
        
        try:
            self.cursor.execute("""
                INSERT INTO student (name, email, role, enrollment_year, major)
                VALUES (?, ?, ?, ?, ?)
            """, (name, email, role, int(year), major))
            
            self.conn.commit()
            messagebox.showinfo("Success", f"Student '{name}' added successfully!")
            
            # Clear form
            self.add_student_name.delete(0, "end")
            self.add_student_email.delete(0, "end")
            self.add_student_role.set("")
            self.add_student_year.delete(0, "end")
            self.add_student_major.delete(0, "end")
            
            self.list_students_gui()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists or invalid data")
        except ValueError:
            messagebox.showerror("Error", "Year must be a number")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error adding student: {e}")
    
    # ==================== EVENTS TAB ====================
    def create_events_tab(self, parent):
        """Create events tab"""
        # Action buttons
        action_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=8)
        action_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkButton(
            action_frame,
            text="📅 List All Events",
            command=self.list_events_gui,
            width=150,
            height=40,
            font=("Segoe UI", 11, "bold")
        ).pack(side="left", padx=5, pady=10)
        
        ctk.CTkButton(
            action_frame,
            text="🔄 Refresh",
            command=self.refresh_events,
            width=100,
            height=40,
            font=("Segoe UI", 11, "bold"),
            fg_color="#00a850"
        ).pack(side="left", padx=5, pady=10)
        
        # Events table
        table_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=8)
        table_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(table_frame, text="Events", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        from tkinter import ttk
        
        tree_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        columns = ("ID", "Title", "Type", "Date", "Status", "Venue", "Registrations")
        self.events_tree = ttk.Treeview(tree_frame, columns=columns, height=20, show="headings")
        
        for col in columns:
            self.events_tree.column(col, width=150)
            self.events_tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.events_tree.yview)
        self.events_tree.configure(yscroll=scrollbar.set)
        
        self.events_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.events_tree.bind("<Double-1>", self.show_event_details)
    
    def list_events_gui(self):
        """List all events"""
        self.events_tree.delete(*self.events_tree.get_children())
        try:
            self.cursor.execute("""
                SELECT e.event_id, e.title, e.event_type, e.start_datetime, 
                       e.status, v.name, COUNT(r.registration_id) as reg_count
                FROM event e
                JOIN venue v ON e.venue_id = v.venue_id
                LEFT JOIN registration r ON e.event_id = r.event_id
                GROUP BY e.event_id
                ORDER BY e.start_datetime
            """)
            events = self.cursor.fetchall()
            
            for i, e in enumerate(events):
                tag = "oddrow" if i % 2 == 0 else "evenrow"
                self.events_tree.insert("", "end", values=(e[0], e[1], e[2], e[3], e[4], e[5], e[6]), tags=(tag,))
            
            self.events_tree.tag_configure("oddrow", background="#2a2a2a", foreground="#ffffff")
            self.events_tree.tag_configure("evenrow", background="#1f1f1f", foreground="#ffffff")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error listing events: {e}")
    
    def refresh_events(self):
        """Refresh events"""
        self.list_events_gui()
        messagebox.showinfo("Success", "Events refreshed!")
    
    def show_event_details(self, event):
        """Show event details on double click"""
        selection = self.events_tree.selection()
        if not selection:
            return
        
        values = self.events_tree.item(selection[0])['values']
        event_id = values[0]
        
        try:
            self.cursor.execute("""
                SELECT e.*, v.name, v.capacity, v.hourly_cost
                FROM event e
                JOIN venue v ON e.venue_id = v.venue_id
                WHERE e.event_id = ?
            """, (event_id,))
            event = self.cursor.fetchone()
            
            if event:
                details = f"""Event ID: {event[0]}
Title: {event[1]}
Type: {event[2]}
Description: {event[3] or "N/A"}
Start: {event[7]}
End: {event[8]}
Venue: {event['name']} (Capacity: {event['capacity']})
Expected Attendance: {event[9]}
Status: {event[11]}
Requires Registration: {'Yes' if event[10] else 'No'}
Recurring: {'Yes' if event[12] else 'No'}"""
                
                messagebox.showinfo("Event Details", details)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error getting event details: {e}")
    
    # ==================== ORGANIZATIONS TAB ====================
    def create_organizations_tab(self, parent):
        """Create organizations tab"""
        main_container = ctk.CTkFrame(parent, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Left side - Organizations
        left_frame = ctk.CTkFrame(main_container, fg_color="#1a1a1a", corner_radius=8)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(left_frame, text="Organizations", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        ctk.CTkButton(
            left_frame,
            text="📊 List All",
            command=self.list_orgs_gui,
            width=150,
            height=35,
            font=("Segoe UI", 11, "bold")
        ).pack(padx=15, pady=(0, 10))
        
        from tkinter import ttk
        
        tree_frame1 = ctk.CTkFrame(left_frame, fg_color="transparent")
        tree_frame1.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        columns1 = ("ID", "Name", "Members", "Budget", "Advisor")
        self.orgs_tree = ttk.Treeview(tree_frame1, columns=columns1, height=20, show="headings")
        
        for col in columns1:
            self.orgs_tree.column(col, width=140)
            self.orgs_tree.heading(col, text=col)
        
        scrollbar1 = ttk.Scrollbar(tree_frame1, orient="vertical", command=self.orgs_tree.yview)
        self.orgs_tree.configure(yscroll=scrollbar1.set)
        
        self.orgs_tree.pack(side="left", fill="both", expand=True)
        scrollbar1.pack(side="right", fill="y")
        
        self.orgs_tree.bind("<<TreeviewSelect>>", self.show_org_members)
        
        # Right side - Members
        right_frame = ctk.CTkFrame(main_container, fg_color="#1a1a1a", corner_radius=8)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(right_frame, text="Organization Members", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        tree_frame2 = ctk.CTkFrame(right_frame, fg_color="transparent")
        tree_frame2.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        columns2 = ("Name", "Level", "Joined", "Active")
        self.members_tree = ttk.Treeview(tree_frame2, columns=columns2, height=20, show="headings")
        
        for col in columns2:
            self.members_tree.column(col, width=140)
            self.members_tree.heading(col, text=col)
        
        scrollbar2 = ttk.Scrollbar(tree_frame2, orient="vertical", command=self.members_tree.yview)
        self.members_tree.configure(yscroll=scrollbar2.set)
        
        self.members_tree.pack(side="left", fill="both", expand=True)
        scrollbar2.pack(side="right", fill="y")
    
    def list_orgs_gui(self):
        """List all organizations"""
        self.orgs_tree.delete(*self.orgs_tree.get_children())
        try:
            self.cursor.execute("""
                SELECT o.org_id, o.name, o.membership_count, o.budget, f.name
                FROM organization o
                JOIN faculty f ON o.advisor_id = f.faculty_id
                ORDER BY o.org_id
            """)
            orgs = self.cursor.fetchall()
            
            for i, o in enumerate(orgs):
                tag = "oddrow" if i % 2 == 0 else "evenrow"
                self.orgs_tree.insert("", "end", values=(o[0], o[1], o[2], f"${o[3]:.2f}", o[4]), tags=(tag,))
            
            self.orgs_tree.tag_configure("oddrow", background="#2a2a2a", foreground="#ffffff")
            self.orgs_tree.tag_configure("evenrow", background="#1f1f1f", foreground="#ffffff")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error listing organizations: {e}")
    
    def show_org_members(self, event):
        """Show members of selected organization"""
        selection = self.orgs_tree.selection()
        if not selection:
            return
        
        values = self.orgs_tree.item(selection[0])['values']
        org_id = values[0]
        
        self.members_tree.delete(*self.members_tree.get_children())
        try:
            self.cursor.execute("""
                SELECT s.name, m.membership_level, m.date_joined, m.is_active
                FROM membership m
                JOIN student s ON m.student_id = s.student_id
                WHERE m.org_id = ?
                ORDER BY m.date_joined DESC
            """, (org_id,))
            members = self.cursor.fetchall()
            
            for m in members:
                active = "Yes" if m[3] else "No"
                self.members_tree.insert("", "end", values=(m[0], m[1], m[2], active))
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error listing members: {e}")
    
    # ==================== VENUES TAB ====================
    def create_venues_tab(self, parent):
        """Create venues tab"""
        action_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=8)
        action_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkButton(
            action_frame,
            text="📍 List All Venues",
            command=self.list_venues_gui,
            width=150,
            height=40,
            font=("Segoe UI", 11, "bold")
        ).pack(side="left", padx=5, pady=10)
        
        table_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=8)
        table_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(table_frame, text="Venues", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        from tkinter import ttk
        
        tree_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        columns = ("ID", "Name", "Building", "Capacity", "Cost/Hour", "Requires Approval")
        self.venues_tree = ttk.Treeview(tree_frame, columns=columns, height=20, show="headings")
        
        for col in columns:
            self.venues_tree.column(col, width=180)
            self.venues_tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.venues_tree.yview)
        self.venues_tree.configure(yscroll=scrollbar.set)
        
        self.venues_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def list_venues_gui(self):
        """List all venues"""
        self.venues_tree.delete(*self.venues_tree.get_children())
        try:
            self.cursor.execute("SELECT * FROM venue ORDER BY venue_id")
            venues = self.cursor.fetchall()
            
            for i, v in enumerate(venues):
                approval = "Yes" if v[7] else "No"
                tag = "oddrow" if i % 2 == 0 else "evenrow"
                self.venues_tree.insert("", "end", values=(v[0], v[1], v[2] or "N/A", v[3], f"${v[6]:.2f}", approval), tags=(tag,))
            
            self.venues_tree.tag_configure("oddrow", background="#2a2a2a", foreground="#ffffff")
            self.venues_tree.tag_configure("evenrow", background="#1f1f1f", foreground="#ffffff")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error listing venues: {e}")
    
    # ==================== FACULTY TAB ====================
    def create_faculty_tab(self, parent):
        """Create faculty and staff tab"""
        main_container = ctk.CTkFrame(parent, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Faculty section
        faculty_frame = ctk.CTkFrame(main_container, fg_color="#1a1a1a", corner_radius=8)
        faculty_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(faculty_frame, text="Faculty Members", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        ctk.CTkButton(
            faculty_frame,
            text="👨‍🏫 List Faculty",
            command=self.list_faculty_gui,
            width=150,
            height=35,
            font=("Segoe UI", 11, "bold")
        ).pack(padx=15, pady=(0, 10))
        
        from tkinter import ttk
        
        tree_frame1 = ctk.CTkFrame(faculty_frame, fg_color="transparent")
        tree_frame1.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        columns1 = ("ID", "Name", "Email", "Department", "Title")
        self.faculty_tree = ttk.Treeview(tree_frame1, columns=columns1, height=20, show="headings")
        
        for col in columns1:
            self.faculty_tree.column(col, width=140)
            self.faculty_tree.heading(col, text=col)
        
        scrollbar1 = ttk.Scrollbar(tree_frame1, orient="vertical", command=self.faculty_tree.yview)
        self.faculty_tree.configure(yscroll=scrollbar1.set)
        
        self.faculty_tree.pack(side="left", fill="both", expand=True)
        scrollbar1.pack(side="right", fill="y")
        
        # Staff section
        staff_frame = ctk.CTkFrame(main_container, fg_color="#1a1a1a", corner_radius=8)
        staff_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(staff_frame, text="Staff Members", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        ctk.CTkButton(
            staff_frame,
            text="👥 List Staff",
            command=self.list_staff_gui,
            width=150,
            height=35,
            font=("Segoe UI", 11, "bold")
        ).pack(padx=15, pady=(0, 10))
        
        tree_frame2 = ctk.CTkFrame(staff_frame, fg_color="transparent")
        tree_frame2.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        columns2 = ("ID", "Name", "Email", "Department", "Position")
        self.staff_tree = ttk.Treeview(tree_frame2, columns=columns2, height=20, show="headings")
        
        for col in columns2:
            self.staff_tree.column(col, width=140)
            self.staff_tree.heading(col, text=col)
        
        scrollbar2 = ttk.Scrollbar(tree_frame2, orient="vertical", command=self.staff_tree.yview)
        self.staff_tree.configure(yscroll=scrollbar2.set)
        
        self.staff_tree.pack(side="left", fill="both", expand=True)
        scrollbar2.pack(side="right", fill="y")
    
    def list_faculty_gui(self):
        """List all faculty"""
        self.faculty_tree.delete(*self.faculty_tree.get_children())
        try:
            self.cursor.execute("SELECT * FROM faculty ORDER BY faculty_id")
            faculty = self.cursor.fetchall()
            
            for i, f in enumerate(faculty):
                tag = "oddrow" if i % 2 == 0 else "evenrow"
                self.faculty_tree.insert("", "end", values=(f[0], f[1], f[2], f[3] or "N/A", f[4] or "N/A"), tags=(tag,))
            
            self.faculty_tree.tag_configure("oddrow", background="#2a2a2a", foreground="#ffffff")
            self.faculty_tree.tag_configure("evenrow", background="#1f1f1f", foreground="#ffffff")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error listing faculty: {e}")
    
    def list_staff_gui(self):
        """List all staff"""
        self.staff_tree.delete(*self.staff_tree.get_children())
        try:
            self.cursor.execute("SELECT * FROM staff ORDER BY staff_id")
            staff = self.cursor.fetchall()
            
            for i, s in enumerate(staff):
                tag = "oddrow" if i % 2 == 0 else "evenrow"
                self.staff_tree.insert("", "end", values=(s[0], s[1], s[2], s[3] or "N/A", s[4] or "N/A"), tags=(tag,))
            
            self.staff_tree.tag_configure("oddrow", background="#2a2a2a", foreground="#ffffff")
            self.staff_tree.tag_configure("evenrow", background="#1f1f1f", foreground="#ffffff")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error listing staff: {e}")
    
    # ==================== STATISTICS TAB ====================
    def create_statistics_tab(self, parent):
        """Create statistics tab"""
        action_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=8)
        action_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkButton(
            action_frame,
            text="📊 Refresh Statistics",
            command=self.show_statistics,
            width=200,
            height=40,
            font=("Segoe UI", 11, "bold"),
            fg_color="#00a850"
        ).pack(side="left", padx=5, pady=10)
        
        # Statistics content
        stats_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=8)
        stats_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.stats_text = scrolledtext.ScrolledText(
            stats_frame,
            height=30,
            width=100,
            wrap=tk.WORD,
            bg="#252525",
            fg="#00a8ff",
            insertbackground="#00a8ff",
            font=("Consolas", 11)
        )
        self.stats_text.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.show_statistics()
    
    def show_statistics(self):
        """Show statistics"""
        self.stats_text.delete("1.0", tk.END)
        try:
            self.cursor.execute("SELECT COUNT(*) FROM student")
            student_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM event")
            event_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM organization")
            org_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM registration")
            reg_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM venue")
            venue_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM faculty")
            faculty_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM staff")
            staff_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT SUM(budget) FROM organization")
            total_budget = self.cursor.fetchone()[0] or 0
            
            self.cursor.execute("SELECT AVG(membership_count) FROM organization")
            avg_members = self.cursor.fetchone()[0] or 0
            
            self.cursor.execute("SELECT AVG(expected_attendance) FROM event")
            avg_attendance = self.cursor.fetchone()[0] or 0
            
            stats = f"""
╔═══════════════════════════════════════════════════════════════╗
║         CAMPUS EVENT MANAGEMENT SYSTEM STATISTICS             ║
╚═══════════════════════════════════════════════════════════════╝

👥 USERS:
   • Students:        {student_count}
   • Faculty:         {faculty_count}
   • Staff:           {staff_count}

📅 EVENTS & REGISTRATIONS:
   • Total Events:                {event_count}
   • Total Registrations:         {reg_count}
   • Average Attendance per Event: {avg_attendance:.1f} participants

📊 ORGANIZATIONS:
   • Total Organizations:        {org_count}
   • Average Members per Org:     {avg_members:.1f}
   • Total Budget:                ${total_budget:,.2f}

📍 RESOURCES:
   • Total Venues:                {venue_count}

═══════════════════════════════════════════════════════════════
Last Updated: {datetime.now().strftime("%d/%m/%Y at %H:%M:%S")}
═══════════════════════════════════════════════════════════════
            """
            
            self.stats_text.insert("1.0", stats)
            self.stats_text.config(state="disabled")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error generating statistics: {e}")


def main():
    root = ctk.CTk()
    app = EventManagementGUI(root)
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, app))
    root.mainloop()


def on_close(root, app):
    """Handle window close"""
    app.close_database()
    root.destroy()


if __name__ == "__main__":
    main()
