import os
import pyodbc
import pandas as pd
from functools import lru_cache
from typing import Tuple, Optional, Dict, Any

# ==================== CONFIGURATION ====================

POSSIBLE_SERVERS = [
    r"localhost\SQLEXPRESS",
    r".\SQLEXPRESS",
    r"localhost",
    r".",
    r"127.0.0.1"
]

DB_NAME = os.getenv("DB_NAME", "Course_registration_system")
DB_DRIVER = os.getenv("DB_DRIVER", "{ODBC Driver 17 for SQL Server}")

# ==================== CONNECTION MANAGEMENT ====================

@lru_cache(maxsize=1)
def get_connection():
    """
    Establish and return a database connection with dynamic server fallback.
    Uses caching to optimize connection reuse.
    """
    last_error = None
    
    # If user explicitly provided DB_SERVER in env, try that first
    explicit_server = os.getenv("DB_SERVER")
    servers_to_test = [explicit_server] if explicit_server else POSSIBLE_SERVERS

    for server in servers_to_test:
        if not server:
            continue
        try:
            conn_str = (
                f"DRIVER={DB_DRIVER};"
                f"SERVER={server};"
                f"DATABASE={DB_NAME};"
                f"Trusted_Connection=yes;"
                f"TrustServerCertificate=yes;"
            )
            return pyodbc.connect(conn_str, timeout=3)
        except Exception as e:
            last_error = e
            continue

    raise ConnectionError(
        f"Could not reach SQL Server database '{DB_NAME}' on any attempted server. "
        f"Last error: {last_error}"
    )

def test_connection() -> bool:
    """Test if database connection is active."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            return True
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False

# ==================== QUERY EXECUTION ====================

def run_query(query: str, params: tuple = ()) -> pd.DataFrame:
    """Execute a SELECT query and return results as a Pandas DataFrame."""
    try:
        with get_connection() as conn:
            return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        print(f"Query Error: {e}\nQuery: {query}")
        return pd.DataFrame()

def execute_commit(query: str, params: tuple = ()) -> bool:
    """Execute INSERT, UPDATE, or DELETE statements safely."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return True
    except Exception as e:
        print(f"Execution Error: {e}\nQuery: {query}")
        return False

# ==================== DASHBOARD METRICS ====================

def get_overview_metrics() -> Dict[str, int]:
    """Fetch KPI counts matching the SQL database schema."""
    metrics = {
        "students": 0,
        "courses": 0,
        "pending_fees": 0,
        "enrollments": 0,
        "departments": 0,
        "instructors": 0
    }
    
    try:
        df_st = run_query("SELECT COUNT(*) AS total FROM students")
        df_co = run_query("SELECT COUNT(*) AS total FROM courses")
        df_fe = run_query("SELECT COUNT(*) AS total FROM Fees WHERE PaidAmount < TotalFee")
        df_en = run_query("SELECT COUNT(*) AS total FROM Registration")
        df_dp = run_query("SELECT COUNT(*) AS total FROM departments")
        df_in = run_query("SELECT COUNT(*) AS total FROM instructors")
        
        if not df_st.empty:
            metrics["students"] = int(df_st.iloc[0]["total"])
        if not df_co.empty:
            metrics["courses"] = int(df_co.iloc[0]["total"])
        if not df_fe.empty:
            metrics["pending_fees"] = int(df_fe.iloc[0]["total"])
        if not df_en.empty:
            metrics["enrollments"] = int(df_en.iloc[0]["total"])
        if not df_dp.empty:
            metrics["departments"] = int(df_dp.iloc[0]["total"])
        if not df_in.empty:
            metrics["instructors"] = int(df_in.iloc[0]["total"])
    except Exception as e:
        print(f"Metrics Error: {e}")
    
    return metrics

# ==================== STUDENT OPERATIONS ====================

def get_student_dashboard() -> pd.DataFrame:
    """Fetch all students utilizing the StudentDashboard view."""
    query = """
    SELECT 
        studentId,
        studentName,
        Email,
        DepartmentName,
        admissionYear,
        TotalCoursesRegistered,
        FeeStatus,
        TotalFee,
        PaidAmount,
        (TotalFee - PaidAmount) AS DueAmount
    FROM StudentDashboard 
    ORDER BY studentName
    """
    return run_query(query)

def get_students_by_department(department_name: str) -> pd.DataFrame:
    """Get all students in a specific department."""
    query = """
    SELECT s.studentId, s.studentName, s.Email, s.Phone, s.admissionYear, d.DepartmentName
    FROM students s
    JOIN departments d ON s.DepartmentID = d.DepartmentID
    WHERE d.DepartmentName = ?
    ORDER BY s.studentName
    """
    return run_query(query, (department_name,))

def get_student_details(student_id: int) -> Optional[pd.DataFrame]:
    """Get detailed profile information for a specific student."""
    query = """
    SELECT 
        s.studentId, s.studentName, s.Email, s.Phone, s.admissionYear, 
        d.DepartmentName, f.TotalFee, f.PaidAmount, 
        (f.TotalFee - f.PaidAmount) AS DueAmount,
        CASE WHEN f.PaidAmount >= f.TotalFee THEN 'Paid' ELSE 'Pending' END AS FeeStatus
    FROM students s
    LEFT JOIN departments d ON s.DepartmentID = d.DepartmentID
    LEFT JOIN Fees f ON s.studentId = f.StudentID
    WHERE s.studentId = ?
    """
    df = run_query(query, (student_id,))
    return df if not df.empty else None

def get_student_courses(student_id: int) -> pd.DataFrame:
    """Get all courses registered by a specific student."""
    query = """
    SELECT 
        c.CourseID, 
        c.CourseName, 
        c.CourseCode, 
        c.Credits, 
        ISNULL(i.InstructorName, 'Not Assigned') AS InstructorName, 
        r.Semester, 
        ISNULL(r.Grade, 'In Progress') AS Grade, 
        r.RegistrationDate
    FROM Registration r
    JOIN courses c ON r.CourseID = c.CourseID
    LEFT JOIN CourseInstructor ci ON c.CourseID = ci.CourseID AND r.Semester = ci.Semester
    LEFT JOIN instructors i ON ci.InstructorID = i.InstructorID
    WHERE r.StudentID = ?
    ORDER BY r.RegistrationDate DESC
    """
    return run_query(query, (student_id,))

# ==================== COURSE OPERATIONS ====================

def get_course_stats() -> pd.DataFrame:
    """Fetch course capacity statistics based on CourseStatistics view logic."""
    query = """
    SELECT 
        c.CourseID,
        c.CourseName,
        c.CourseCode,
        c.Credits,
        d.DepartmentName,
        c.MaxCapacity,
        COUNT(r.StudentID) AS EnrolledStudents,
        (c.MaxCapacity - COUNT(r.StudentID)) AS AvailableSeats,
        ROUND(CAST(COUNT(r.StudentID) * 100.0 / c.MaxCapacity AS FLOAT), 1) AS FillPercent,
        ISNULL(i.InstructorName, 'Not Assigned') AS InstructorName
    FROM courses c
    LEFT JOIN Registration r ON c.CourseID = r.CourseID
    JOIN departments d ON c.DepartmentID = d.DepartmentID
    LEFT JOIN CourseInstructor ci ON c.CourseID = ci.CourseID
    LEFT JOIN instructors i ON ci.InstructorID = i.InstructorID
    GROUP BY c.CourseID, c.CourseName, c.CourseCode, c.Credits, d.DepartmentName, c.MaxCapacity, i.InstructorName
    ORDER BY c.CourseName
    """
    return run_query(query)

def get_course_enrollments(course_id: int) -> pd.DataFrame:
    """Get all enrolled students for a given course."""
    query = """
    SELECT 
        s.studentId, 
        s.studentName, 
        s.Email, 
        d.DepartmentName,
        r.Semester, 
        ISNULL(r.Grade, 'In Progress') AS Grade, 
        r.RegistrationDate
    FROM Registration r
    JOIN students s ON r.StudentID = s.studentId
    JOIN departments d ON s.DepartmentID = d.DepartmentID
    WHERE r.CourseID = ?
    ORDER BY s.studentName
    """
    return run_query(query, (course_id,))

def get_top_courses(limit: int = 5) -> pd.DataFrame:
    """Get top courses by student enrollment."""
    query = f"""
    SELECT TOP {limit}
        c.CourseName, 
        c.CourseCode, 
        COUNT(r.StudentID) AS EnrolledStudents, 
        c.MaxCapacity
    FROM courses c
    LEFT JOIN Registration r ON c.CourseID = r.CourseID
    GROUP BY c.CourseID, c.CourseName, c.CourseCode, c.MaxCapacity
    ORDER BY EnrolledStudents DESC
    """
    return run_query(query)

# ==================== REGISTRATION OPERATIONS ====================

def get_student_registrations() -> pd.DataFrame:
    """Fetch complete registration roster with course and instructor details."""
    query = """
    SELECT 
        r.RegistrationID,
        s.studentId,
        s.studentName, 
        c.CourseID,
        c.CourseName, 
        c.CourseCode,
        ISNULL(i.InstructorName, 'Not Assigned') AS InstructorName, 
        r.Semester, 
        ISNULL(r.Grade, 'In Progress') AS Grade,
        r.RegistrationDate
    FROM Registration r
    JOIN students s ON r.StudentID = s.studentId
    JOIN courses c ON r.CourseID = c.CourseID
    LEFT JOIN CourseInstructor ci ON c.CourseID = ci.CourseID AND r.Semester = ci.Semester
    LEFT JOIN instructors i ON ci.InstructorID = i.InstructorID
    ORDER BY r.RegistrationDate DESC
    """
    return run_query(query)

def register_student(student_id: int, course_id: int, semester: str) -> Tuple[bool, str]:
    """Register a student for a course with capacity and unique constraint validation."""
    try:
        # Check for unique constraint (StudentID, CourseID, Semester)
        check_dup = """
        SELECT COUNT(*) AS total FROM Registration 
        WHERE StudentID = ? AND CourseID = ? AND Semester = ?
        """
        dup_df = run_query(check_dup, (student_id, course_id, semester))
        if not dup_df.empty and dup_df.iloc[0]["total"] > 0:
            return False, "Student is already registered for this course in the selected semester."

        # Check course capacity constraint
        cap_query = """
        SELECT c.MaxCapacity, COUNT(r.StudentID) AS CurrentEnrolled 
        FROM courses c
        LEFT JOIN Registration r ON c.CourseID = r.CourseID
        WHERE c.CourseID = ?
        GROUP BY c.MaxCapacity
        """
        cap_df = run_query(cap_query, (course_id,))
        if not cap_df.empty:
            max_cap = cap_df.iloc[0]["MaxCapacity"]
            curr_enrolled = cap_df.iloc[0]["CurrentEnrolled"] or 0
            if curr_enrolled >= max_cap:
                return False, f"Cannot register. Course has reached maximum capacity ({max_cap} seats)."

        # Insert registration record
        insert_query = """
        INSERT INTO Registration (StudentID, CourseID, Semester) 
        VALUES (?, ?, ?)
        """
        if execute_commit(insert_query, (student_id, course_id, semester)):
            return True, "✓ Registration completed successfully!"
        else:
            return False, "Failed to record registration in the database."
            
    except Exception as e:
        return False, f"Registration error: {str(e)}"

def cancel_registration(student_id: int, course_id: int, semester: str) -> Tuple[bool, str]:
    """Cancel a student's course registration."""
    try:
        query = "DELETE FROM Registration WHERE StudentID = ? AND CourseID = ? AND Semester = ?"
        if execute_commit(query, (student_id, course_id, semester)):
            return True, "✓ Registration cancelled successfully!"
        else:
            return False, "Failed to cancel registration record."
    except Exception as e:
        return False, f"Cancellation error: {str(e)}"

# ==================== FEE OPERATIONS ====================

def get_fee_status_list(status_filter: str = "All") -> pd.DataFrame:
    """Fetch fee status records using FeeStatusView schema."""
    query = """
    SELECT 
        s.studentId, 
        s.studentName, 
        s.Email,
        d.DepartmentName,
        f.TotalFee, 
        f.PaidAmount, 
        (f.TotalFee - f.PaidAmount) AS DueAmount,
        CASE WHEN f.PaidAmount >= f.TotalFee THEN 'Paid' ELSE 'Pending' END AS FeeStatus
    FROM students s
    JOIN departments d ON s.DepartmentID = d.DepartmentID
    JOIN Fees f ON s.studentId = f.StudentID
    """
    
    if status_filter == "Pending":
        query += " WHERE f.PaidAmount < f.TotalFee"
    elif status_filter == "Paid":
        query += " WHERE f.PaidAmount >= f.TotalFee"
    
    query += " ORDER BY (f.TotalFee - f.PaidAmount) DESC"
    return run_query(query)

def get_pending_fees() -> pd.DataFrame:
    """Get students with outstanding dues."""
    query = """
    SELECT 
        s.studentId,
        s.studentName,
        s.Email,
        f.TotalFee,
        f.PaidAmount,
        (f.TotalFee - f.PaidAmount) AS DueAmount
    FROM students s
    JOIN Fees f ON s.studentId = f.StudentID
    WHERE f.PaidAmount < f.TotalFee
    ORDER BY (f.TotalFee - f.PaidAmount) DESC
    """
    return run_query(query)

def update_fee_payment(student_id: int, add_amount: int) -> Tuple[bool, str]:
    """Record a fee payment, enforcing constraints (PaidAmount <= TotalFee)."""
    try:
        fee_df = run_query("SELECT TotalFee, PaidAmount FROM Fees WHERE StudentID = ?", (student_id,))
        if fee_df.empty:
            return False, "Fee record not found for this student."

        total_fee = int(fee_df.iloc[0]["TotalFee"])
        current_paid = int(fee_df.iloc[0]["PaidAmount"])
        new_paid = current_paid + add_amount

        if new_paid > total_fee:
            remaining = total_fee - current_paid
            return False, f"Payment exceeds due amount. Maximum remaining balance: {remaining:,} PKR"

        update_query = """
        UPDATE Fees 
        SET PaidAmount = ?, LastPaymentDate = GETDATE() 
        WHERE StudentID = ?
        """
        if execute_commit(update_query, (new_paid, student_id)):
            return True, f"✓ Payment of {add_amount:,} PKR recorded successfully!"
        else:
            return False, "Failed to update fee record."
            
    except Exception as e:
        return False, f"Payment processing error: {str(e)}"

# ==================== DEPARTMENT & INSTRUCTOR OPERATIONS ====================

def get_departments() -> pd.DataFrame:
    """Fetch all departments with aggregated statistics."""
    query = """
    SELECT 
        d.DepartmentID,
        d.DepartmentName,
        COUNT(DISTINCT s.studentId) AS StudentCount,
        COUNT(DISTINCT c.CourseID) AS CourseCount,
        COUNT(DISTINCT r.RegistrationID) AS TotalRegistrations
    FROM departments d
    LEFT JOIN students s ON d.DepartmentID = s.DepartmentID
    LEFT JOIN courses c ON d.DepartmentID = c.DepartmentID
    LEFT JOIN Registration r ON c.CourseID = r.CourseID
    GROUP BY d.DepartmentID, d.DepartmentName
    ORDER BY d.DepartmentName
    """
    return run_query(query)

def get_instructors() -> pd.DataFrame:
    """Fetch instructors and assigned course totals."""
    query = """
    SELECT 
        i.InstructorID,
        i.InstructorName,
        i.Email,
        d.DepartmentName,
        i.Qualification,
        COUNT(DISTINCT ci.CourseID) AS CoursesAssigned
    FROM instructors i
    LEFT JOIN departments d ON i.DepartmentID = d.DepartmentID
    LEFT JOIN CourseInstructor ci ON i.InstructorID = ci.InstructorID
    GROUP BY i.InstructorID, i.InstructorName, i.Email, d.DepartmentName, i.Qualification
    ORDER BY i.InstructorName
    """
    return run_query(query)

# ==================== ANALYTICS ====================

def get_grade_statistics() -> pd.DataFrame:
    """Fetch grade distributions across all courses."""
    query = """
    SELECT 
        ISNULL(Grade, 'In Progress') AS Grade,
        COUNT(*) AS StudentCount,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Registration), 1) AS Percentage
    FROM Registration
    GROUP BY Grade
    ORDER BY Grade ASC
    """
    return run_query(query)

def get_enrollment_by_semester() -> pd.DataFrame:
    """Fetch enrollment statistics per semester."""
    query = """
    SELECT 
        Semester,
        COUNT(DISTINCT StudentID) AS UniqueStudents,
        COUNT(DISTINCT CourseID) AS UniqueCourses,
        COUNT(*) AS TotalRegistrations
    FROM Registration
    GROUP BY Semester
    ORDER BY Semester DESC
    """
    return run_query(query)

def get_average_gpa_by_student() -> pd.DataFrame:
    """Calculate GPA estimates for students with completed grades."""
    query = """
    SELECT TOP 15
        s.studentId,
        s.studentName,
        ROUND(AVG(CASE 
            WHEN r.Grade = 'A+' THEN 4.0
            WHEN r.Grade = 'A' THEN 3.7
            WHEN r.Grade = 'B+' THEN 3.3
            WHEN r.Grade = 'B' THEN 3.0
            WHEN r.Grade = 'C+' THEN 2.3
            WHEN r.Grade = 'C' THEN 2.0
            WHEN r.Grade = 'D' THEN 1.0
            WHEN r.Grade = 'F' THEN 0.0
            ELSE NULL
        END), 2) AS AverageGPA,
        COUNT(CASE WHEN r.Grade IS NOT NULL THEN 1 END) AS CoursesCompleted
    FROM students s
    JOIN Registration r ON s.studentId = r.StudentID
    WHERE r.Grade IS NOT NULL
    GROUP BY s.studentId, s.studentName
    ORDER BY AverageGPA DESC
    """
    return run_query(query)

# ==================== SYSTEM METADATA ====================

def get_system_info() -> Dict[str, Any]:
    """Get system database information and status."""
    return {
        "database": DB_NAME,
        "driver": DB_DRIVER,
        "server": "Connected" if test_connection() else "Disconnected"
    }