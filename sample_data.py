"""
Sample Mock Data for Demo Mode in CodeMind AI
Provides structured, realistic AI responses when GEMINI_API_KEY is not configured.
"""

STUDENT_MANAGEMENT_REQUIREMENT = "Create a Python student management system where an administrator can add, update, delete and search student records."

STUDENT_MANAGEMENT_ANALYSIS = {
    "problem_statement": "Educational institutions need an efficient system for administrators to maintain student records, allowing operations like adding new enrollments, updating profile details, searching student entries by ID or name, and removing records.",
    "functional_requirements": [
        "System shall allow administrator to add a new student record (ID, Name, Grade, Major, Email).",
        "System shall allow administrator to search for a student by unique Student ID or full/partial Name.",
        "System shall allow updating existing student details (Grade, Major, Email).",
        "System shall support deleting a student record with confirmation prompt.",
        "System shall display a complete list of enrolled students in a formatted tabular format."
    ],
    "non_functional_requirements": [
        "Response time for record retrieval and searching must be under 1 second.",
        "Data validation must prevent duplicate Student IDs.",
        "Application should provide a clean user interface with robust input exception handling."
    ],
    "actors": [
        "Administrator (Primary User)",
        "System Auditor"
    ],
    "inputs": [
        "Student ID (Unique Integer/String)",
        "Student Name (String)",
        "Major / Course (String)",
        "GPA / Grade (Float)",
        "Contact Email (String)"
    ],
    "outputs": [
        "Operation Success/Failure Messages",
        "Detailed Student Profile Record",
        "Formatted Student Summary List",
        "Validation Warning Messages"
    ],
    "constraints": [
        "Must be implemented using Python 3.x.",
        "Must support persistent storage (SQLite or JSON file storage)."
    ],
    "assumptions": [
        "Only one administrator accesses the system at a time.",
        "Student IDs are alphanumeric and unique per student."
    ],
    "ambiguities": [
        "Requirement does not specify if persistent storage (SQLite database or JSON) is required.",
        "No mention of authentication/login security for administrators."
    ],
    "missing_information": [
        "Specific fields required for student profile (e.g. phone number, address, date of birth).",
        "Export capabilities (e.g., export student roster to CSV or PDF)."
    ],
    "suggestions": [
        "Include administrator authentication with password hashing.",
        "Integrate SQLite database for persistent storage instead of in-memory data structures.",
        "Add CSV export and search filtering by GPA or Major."
    ],
    "is_ambiguous": True
}

STUDENT_MANAGEMENT_CODE = '''"""
Student Management System
Language: Python 3
Author: CodeMind AI Assistant
Description: Object-Oriented Student Management System with SQLite database persistence.
"""

import sqlite3
import re

class StudentDatabase:
    """Handles all database operations for Student records."""
    
    def __init__(self, db_name="students.db"):
        self.db_name = db_name
        self.init_db()
        
    def get_connection(self):
        return sqlite3.connect(self.db_name)
        
    def init_db(self):
        """Initialize the database table if it doesn't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    major TEXT NOT NULL,
                    gpa REAL NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            """)
            conn.commit()

    def add_student(self, student_id, name, major, gpa, email):
        """Add a new student to the database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO students VALUES (?, ?, ?, ?, ?)",
                    (student_id, name, major, gpa, email)
                )
                conn.commit()
                return True, "Student record added successfully!"
        except sqlite3.IntegrityError:
            return False, "Error: Student ID or Email already exists."
        except Exception as e:
            return False, f"Database error: {str(e)}"

    def search_student(self, query):
        """Search student by ID or Name."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM students WHERE student_id = ? OR name LIKE ?",
                (query, f"%{query}%")
            )
            rows = cursor.fetchall()
            return rows

    def update_student(self, student_id, name=None, major=None, gpa=None, email=None):
        """Update existing student details."""
        updates = []
        params = []
        if name:
            updates.append("name = ?")
            params.append(name)
        if major:
            updates.append("major = ?")
            params.append(major)
        if gpa is not None:
            updates.append("gpa = ?")
            params.append(gpa)
        if email:
            updates.append("email = ?")
            params.append(email)
            
        if not updates:
            return False, "No fields to update."
            
        params.append(student_id)
        query = f"UPDATE students SET {', '.join(updates)} WHERE student_id = ?"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if cursor.rowcount > 0:
                conn.commit()
                return True, "Student updated successfully!"
            return False, "Student ID not found."

    def delete_student(self, student_id):
        """Delete a student record by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            if cursor.rowcount > 0:
                conn.commit()
                return True, "Student record deleted successfully!"
            return False, "Student ID not found."

    def get_all_students(self):
        """Fetch all records."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students ORDER BY student_id")
            return cursor.fetchall()

class StudentManagerCLI:
    """Command Line Interface for Administrator."""
    
    def __init__(self):
        self.db = StudentDatabase()

    @staticmethod
    def validate_email(email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None


    def display_menu(self):
        print("\\n=== STUDENT MANAGEMENT SYSTEM ===")
        print("1. Add New Student")
        print("2. Search Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. View All Students")
        print("6. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter choice (1-6): ").strip()
            
            if choice == '1':
                s_id = input("Enter Student ID: ").strip()
                name = input("Enter Name: ").strip()
                major = input("Enter Major: ").strip()
                try:
                    gpa = float(input("Enter GPA (0.0 - 4.0): ").strip())
                except ValueError:
                    print("Invalid GPA number.")
                    continue
                email = input("Enter Email: ").strip()
                if not self.validate_email(email):
                    print("Invalid Email Format!")
                    continue
                    
                success, msg = self.db.add_student(s_id, name, major, gpa, email)
                print(msg)
                
            elif choice == '2':
                query = input("Enter Student ID or Name to Search: ").strip()
                results = self.db.search_student(query)
                if results:
                    print("\\n--- Search Results ---")
                    for s in results:
                        print(f"ID: {s[0]} | Name: {s[1]} | Major: {s[2]} | GPA: {s[3]} | Email: {s[4]}")
                else:
                    print("No matching student records found.")
                    
            elif choice == '3':
                s_id = input("Enter Student ID to Update: ").strip()
                new_major = input("Enter New Major (Leave blank to keep current): ").strip() or None
                new_gpa_str = input("Enter New GPA (Leave blank to keep current): ").strip()
                new_gpa = float(new_gpa_str) if new_gpa_str else None
                new_email = input("Enter New Email (Leave blank to keep current): ").strip() or None
                
                success, msg = self.db.update_student(s_id, major=new_major, gpa=new_gpa, email=new_email)
                print(msg)
                
            elif choice == '4':
                s_id = input("Enter Student ID to Delete: ").strip()
                confirm = input(f"Are you sure you want to delete {s_id}? (y/n): ").strip().lower()
                if confirm == 'y':
                    success, msg = self.db.delete_student(s_id)
                    print(msg)
                    
            elif choice == '5':
                students = self.db.get_all_students()
                print("\\n--- All Enrolled Students ---")
                print(f"{'ID':<10} {'Name':<20} {'Major':<18} {'GPA':<6} {'Email':<25}")
                print("-" * 80)
                for s in students:
                    print(f"{s[0]:<10} {s[1]:<20} {s[2]:<18} {s[3]:<6.2f} {s[4]:<25}")
                    
            elif choice == '6':
                print("Exiting Student Management System. Goodbye!")
                break
            else:
                print("Invalid choice, please select between 1 and 6.")

if __name__ == "__main__":
    app = StudentManagerCLI()
    app.run()
'''

STUDENT_MANAGEMENT_CODE_EXPLANATION = {
    "summary": "This is a modular, Object-Oriented Python application that implements a complete CRUD (Create, Read, Update, Delete) Student Management System with persistent SQLite database storage and an interactive CLI interface.",
    "step_by_step": [
        "1. Initialization: The StudentDatabase class connects to 'students.db' and creates the 'students' table with primary key constraints if it doesn't already exist.",
        "2. Add Student: Validates input fields and uses parameterized SQL queries ('INSERT INTO students...') to prevent SQL injection.",
        "3. Search Student: Uses SQL 'LIKE' query to support flexible searching by exact Student ID or partial student name.",
        "4. Update Record: Dynamically builds an UPDATE SQL statement based on which fields the administrator modified.",
        "5. Delete Record: Removes student entry by ID after explicit user confirmation.",
        "6. CLI Loop: The StudentManagerCLI presents an intuitive menu interface with regular expression validation for email addresses."
    ],
    "key_components": [
        {"name": "StudentDatabase Class", "description": "Manages connection context managers and executes secure SQL queries."},
        {"name": "StudentManagerCLI Class", "description": "Handles user interaction, menu rendering, and input validation."},
        {"name": "validate_email Method", "description": "Uses RegEx pattern r'^[\w\.-]+@[\w\.-]+\.\w+$' to ensure valid email syntax."}
    ],
    "important_variables": [
        {"name": "db_name", "description": "String path for SQLite database file ('students.db')."},
        {"name": "student_id", "description": "Unique primary key identifier for each student record."},
        {"name": "cursor", "description": "SQLite cursor used for executing SQL statements safely."}
    ],
    "algorithm": "Relational Data Management using B-Tree Indexed Lookup (SQLite PK)",
    "time_complexity": "O(1) for Add/Search by ID; O(N) for partial name search or listing all students.",
    "space_complexity": "O(N) where N is the total number of student records stored in SQLite database."
}

STUDENT_MANAGEMENT_REVIEW = {
    "score": 92,
    "issues": [
        {
            "category": "Bugs / Potential Issues",
            "severity": "Low",
            "title": "Uncaught ValueError on GPA input during update",
            "description": "If user inputs non-numeric characters for GPA during update, ValueError will crash the prompt loop."
        },
        {
            "category": "Security Issues",
            "severity": "Good",
            "title": "SQL Injection Protection Active",
            "description": "All SQL commands use parameterized queries (?, ?), preventing SQL injection vulnerabilities."
        },
        {
            "category": "Performance Issues",
            "severity": "Low",
            "title": "Unindexed Full Name Search",
            "description": "Searching name using 'LIKE %query%' results in table scan for large datasets."
        },
        {
            "category": "Logical Issues",
            "severity": "Good",
            "title": "Clean Resource Cleanup",
            "description": "Database connections use context managers ('with') guaranteeing connection closure even on errors."
        }
    ],
    "suggestions": [
        "Wrap GPA conversion in try-except block inside the update workflow.",
        "Add SQLite INDEX on column 'name' to improve fuzzy search speed on large tables.",
        "Implement pagination when listing large numbers of student records."
    ],
    "improved_code": '''# Refactored update logic with robust GPA error handling
def safe_float_input(prompt, default=None):
    raw = input(prompt).strip()
    if not raw and default is not None:
        return default
    try:
        val = float(raw)
        if 0.0 <= val <= 4.0:
            return val
        print("GPA must be between 0.0 and 4.0")
        return None
    except ValueError:
        print("Invalid float format")
        return None
'''
}

STUDENT_MANAGEMENT_DOCS = """# Software Requirement Specification (SRS) & System Architecture
## Project: Student Management System (Python)
**Generated by CodeMind AI**

---

### 1. Project Overview & Objectives
The **Student Management System** is a lightweight, reliable desktop software assistant designed for academic administrators. It simplifies student record lifecycle management, eliminating manual spreadsheet overhead and providing real-time query capabilities.

### 2. Problem Statement
Educational institutions frequently suffer from fragmented student data, leading to record duplicate errors, inefficient record searching, and lack of data validation. This system solves these issues by enforcing unique ID constraints, automated database persistence, and rapid search indexing.

### 3. Functional Requirements
- **FR-1**: Add new student profile including ID, Name, Major, GPA, and Email.
- **FR-2**: Search profiles by ID or partial Name lookup.
- **FR-3**: Update Major, GPA, or Email attributes for existing records.
- **FR-4**: Delete obsolete student entries with administrative confirmation.
- **FR-5**: Display tabular report of all enrolled students sorted by ID.

### 4. Non-Functional Requirements
- **NFR-1 Integrity**: Enforce primary key uniqueness on Student ID and Email.
- **NFR-2 Performance**: Query latency < 100ms for single record lookups.
- **NFR-3 Usability**: Command line interface with clear navigation choices and error messaging.

### 5. System Requirements & Technology Stack
- **Programming Language**: Python 3.10+
- **Database**: SQLite 3
- **Libraries**: `sqlite3`, `re` (Standard Python Library)
- **OS Compatibility**: Windows, macOS, Linux

### 6. System Architecture & Modules
```
[ CLI User Interface ] <---> [ Input Validator ] <---> [ StudentDatabase Handler ] <---> [ SQLite Database ]
```
- **Module 1 (`StudentDatabase`)**: Enforces database schema, manages connection pooling & parameter binding.
- **Module 2 (`StudentManagerCLI`)**: Handles menu loops, user command routing, and formatted string output.

### 7. Algorithm & Data Flow
1. User selects menu option (1 to 6).
2. Input is validated against standard regex patterns and numeric ranges.
3. Parameterized query dispatched to SQLite engine.
4. Result set formatted into ASCII border tables for immediate user display.

### 8. Future Scope & System Enhancements
- **RAG-based Documentation Analysis**: Support querying college policies directly through LLM context retrieval.
- **GitHub & CI/CD Integration**: Automated deployment pipeline for multi-institution updates.
- **Automatic Unit Test Generation**: Automated pytest script creation for edge-case coverage.
- **UML Diagram Generation**: Auto-generating Class and Sequence diagrams.
- **Multi-Agent Software Workflow**: Delegating database optimization tasks to specialized sub-agents.
"""
