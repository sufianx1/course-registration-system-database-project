
import streamlit as st
import pandas as pd
from datetime import datetime
import database as db
from streamlit_option_menu import option_menu

# ==================== PAGE CONFIGURATION ====================

st.set_page_config(
    page_title="Course Registration System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM STYLING ====================

st.markdown("""
    <style>
    /* Main Application Styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 32px 24px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 24px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        margin: 8px 0 0 0;
        color: #94a3b8;
        font-size: 16px;
    }
    
    /* Metric Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;

        /* Force equal height & vertically center content */
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .metric-card:hover {
        border-color: #38bdf8;
        box-shadow: 0 8px 24px rgba(56, 189, 248, 0.15);
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(135deg, #38bdf8 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 8px 0;
    }
    
    .metric-label {
        font-size: 11px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        min-height: 32px; /* Reserves uniform space for 2 lines of text */
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Badge Styling */
    .badge-paid {
        background: rgba(34, 197, 94, 0.1);
        color: #4ade80;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid #22c55e;
    }
    
    .badge-pending {
        background: rgba(239, 68, 68, 0.1);
        color: #fca5a5;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid #ef4444;
    }
    
    .badge-success {
        background: rgba(34, 197, 94, 0.1);
        color: #4ade80;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .badge-warning {
        background: rgba(245, 158, 11, 0.1);
        color: #fbbf24;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    /* Table Styling */
    .dataframe {
        background: #1e293b;
        border-color: #334155;
    }
    
    /* Divider */
    hr {
        border-color: #334155;
        margin: 24px 0;
    }
    
    /* Form Elements */
    .stSelectbox > div > div {
        background-color: #1e293b;
        border-color: #334155;
        color: #f8fafc;
    }
    
    .stNumberInput > div > div {
        background-color: #1e293b;
        border-color: #334155;
    }
    
    .stTextInput > div > div {
        background-color: #1e293b;
        border-color: #334155;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #38bdf8 0%, #06b6d4 100%);
        color: #0f172a;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(56, 189, 248, 0.3);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background-color: rgba(34, 197, 94, 0.1);
        border-color: #22c55e;
        color: #4ade80;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1);
        border-color: #ef4444;
        color: #fca5a5;
    }
    
    .stInfo {
        background-color: rgba(56, 189, 248, 0.1);
        border-color: #38bdf8;
        color: #38bdf8;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1);
        border-color: #f59e0b;
        color: #fbbf24;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()

# ==================== PAGE: DASHBOARD ====================

def render_dashboard():
    """Render main dashboard with KPI metrics and overview."""
    st.markdown("""
        <div class="main-header">
            <h1>📊 Academic Dashboard</h1>
            <p>University-wide course registration and student management system</p>
        </div>
    """, unsafe_allow_html=True)
    
    try:
        # Fetch metrics
        metrics = db.get_overview_metrics()
        
        # Display KPI cards
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📚 Total Students</div>
                    <div class="metric-value">{metrics['students']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📖 Active Courses</div>
                    <div class="metric-value">{metrics['courses']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📝 Registrations</div>
                    <div class="metric-value">{metrics['enrollments']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">💳 Pending Fees</div>
                    <div class="metric-value" style="color: #fca5a5;">{metrics['pending_fees']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">🏢 Departments</div>
                    <div class="metric-value">{metrics['departments']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col6:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">👨‍🏫 Instructors</div>
                    <div class="metric-value">{metrics['instructors']}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Dashboard Overview
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.subheader("📋 Student Overview")
            df_students = db.get_student_dashboard()
            if not df_students.empty:
                # Select columns to display
                display_cols = ['studentName', 'DepartmentName', 'TotalCoursesRegistered', 'FeeStatus', 'DueAmount']
                if 'DueAmount' not in df_students.columns:
                    display_cols = ['studentName', 'DepartmentName', 'TotalCoursesRegistered', 'FeeStatus']
                
                st.dataframe(
                    df_students[display_cols],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No student data available")
        
        with col_right:
            st.subheader("🎯 Course Capacity")
            df_courses = db.get_course_stats()
            if not df_courses.empty:
                for idx, row in df_courses.iterrows():
                    st.write(f"**{row['CourseName'][:25]}**")
                    fill_pct = min(row['FillPercent'] / 100.0, 1.0)
                    st.progress(fill_pct)
                    st.caption(f"{int(row['EnrolledStudents'])}/{int(row['MaxCapacity'])} enrolled")
                    if idx < len(df_courses) - 1:
                        st.write("")
            else:
                st.info("No course data available")
        
        st.markdown("---")
        
        # Quick Stats
        st.subheader("📊 Quick Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            top_courses = db.get_top_courses(limit=1)
            if not top_courses.empty:
                st.metric("Most Popular Course", top_courses.iloc[0]['CourseName'][:20])
        
        with col2:
            grades = db.get_grade_statistics()
            if not grades.empty:
                st.metric("Grade Records", len(grades))
        
        with col3:
            enrollments = db.get_enrollment_by_semester()
            if not enrollments.empty:
                st.metric("Active Semesters", len(enrollments))
        
        with col4:
            pending = db.get_pending_fees()
            st.metric("Students with Due Fees", len(pending))
        
    except Exception as e:
        st.error(f"Dashboard Error: {str(e)}")

# ==================== PAGE: STUDENTS ====================

def render_students():
    """Render student management page."""
    st.header("👨‍🎓 Student Management")
    
    tab_list, tab_detail = st.tabs(["Student List", "Student Details"])
    
    with tab_list:
        st.subheader("All Students")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            search = st.text_input("🔍 Search by name or email")
        with col2:
            departments = db.get_departments()
            if not departments.empty:
                dept_list = ["All"] + departments['DepartmentName'].tolist()
                selected_dept = st.selectbox("📍 Department", dept_list)
        with col3:
            sort_by = st.selectbox("Sort by", ["Name", "Admission Year", "Fee Status"])
        
        # Fetch and filter students
        df_students = db.get_student_dashboard()
        
        if search:
            df_students = df_students[
                df_students['studentName'].str.contains(search, case=False, na=False) |
                df_students['Email'].str.contains(search, case=False, na=False)
            ]
        
        if col2 and selected_dept != "All":
            df_students = df_students[df_students['DepartmentName'] == selected_dept]
        
        if not df_students.empty:
            st.dataframe(df_students, use_container_width=True, hide_index=True)
            st.caption(f"Showing {len(df_students)} students")
        else:
            st.info("No students found")
    
    with tab_detail:
        st.subheader("Student Details")
        df_students = db.get_student_dashboard()
        if not df_students.empty:
            student_options = {row['studentName']: row['studentId'] for _, row in df_students.iterrows()}
            selected_student = st.selectbox("Select Student", list(student_options.keys()))
            student_id = student_options[selected_student]
            
            # Get student details
            df_details = db.get_student_details(student_id)
            if df_details is not None and not df_details.empty:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Name:** {df_details.iloc[0]['studentName']}")
                    st.write(f"**Email:** {df_details.iloc[0]['Email']}")
                with col2:
                    st.write(f"**Department:** {df_details.iloc[0]['DepartmentName']}")
                    st.write(f"**Admission Year:** {df_details.iloc[0]['admissionYear']}")
                with col3:
                    st.write(f"**Phone:** {df_details.iloc[0]['Phone']}")
                    if pd.notna(df_details.iloc[0]['DueAmount']):
                        due = int(df_details.iloc[0]['DueAmount'])
                        if due == 0:
                            st.write("**Fee Status:** ✓ Paid")
                        else:
                            st.write(f"**Fee Status:** ⚠ Due: {due:,} PKR")
                
                st.markdown("---")
                
                # Student's registered courses
                st.subheader("Registered Courses")
                df_courses = db.get_student_courses(student_id)
                if not df_courses.empty:
                    st.dataframe(df_courses, use_container_width=True, hide_index=True)
                else:
                    st.info("No courses registered")
        else:
            st.info("No students available")

# ==================== PAGE: COURSES ====================

def render_courses():
    """Render course management page."""
    st.header("📚 Course Management")
    
    tab_list, tab_detail = st.tabs(["Courses", "Course Details"])
    
    with tab_list:
        st.subheader("All Courses")
        
        df_courses = db.get_course_stats()
        if not df_courses.empty:
            # Display courses with capacity bars
            for idx, row in df_courses.iterrows():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{row['CourseName']}** ({row['CourseCode']})")
                    st.progress(min(row['FillPercent'] / 100.0, 1.0))
                with col2:
                    st.caption(f"{int(row['EnrolledStudents'])}/{int(row['MaxCapacity'])} enrolled")
                with col3:
                    st.caption(f"Dept: {row['DepartmentName']}")
        else:
            st.info("No courses available")
    
    with tab_detail:
        st.subheader("Course Details")
        df_courses = db.get_course_stats()
        if not df_courses.empty:
            course_options = {f"{row['CourseName']} ({row['CourseCode']})": row['CourseID'] 
                            for _, row in df_courses.iterrows()}
            selected_course = st.selectbox("Select Course", list(course_options.keys()))
            course_id = course_options[selected_course]
            
            # Course details
            course_info = df_courses[df_courses['CourseID'] == course_id].iloc[0]
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Credits", int(course_info['Credits']))
            with col2:
                st.metric("Capacity", int(course_info['MaxCapacity']))
            with col3:
                st.metric("Enrolled", int(course_info['EnrolledStudents']))
            with col4:
                st.metric("Available", int(course_info['AvailableSeats']))
            
            st.markdown("---")
            
            # Enrolled students
            st.subheader("Enrolled Students")
            df_enrolled = db.get_course_enrollments(course_id)
            if not df_enrolled.empty:
                st.dataframe(df_enrolled, use_container_width=True, hide_index=True)
            else:
                st.info("No students enrolled")
        else:
            st.info("No courses available")

# ==================== PAGE: REGISTRATIONS ====================

def render_registrations():
    """Render registration management page."""
    st.header("📝 Course Registration")
    
    tab_view, tab_add = st.tabs(["View Registrations", "New Registration"])
    
    with tab_view:
        st.subheader("All Course Registrations")
        
        # Search filter
        search = st.text_input("🔍 Search by student, course, or instructor")
        
        df_registrations = db.get_student_registrations()
        
        if search and not df_registrations.empty:
            df_registrations = df_registrations[
                df_registrations['studentName'].str.contains(search, case=False, na=False) |
                df_registrations['CourseName'].str.contains(search, case=False, na=False) |
                df_registrations['InstructorName'].str.contains(search, case=False, na=False, regex=False)
            ]
        
        if not df_registrations.empty:
            st.dataframe(df_registrations, use_container_width=True, hide_index=True)
            st.caption(f"Total: {len(df_registrations)} registrations")
        else:
            st.info("No registrations found")
    
    with tab_add:
        st.subheader("Register Student for Course")
        
        df_students = db.get_student_dashboard()
        df_courses = db.get_course_stats()
        
        if df_students.empty or df_courses.empty:
            st.error("Missing required data")
            return
        
        with st.form("registration_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                student_options = {f"{row['studentName']} (ID: {row['studentId']})": row['studentId'] 
                                 for _, row in df_students.iterrows()}
                selected_student = st.selectbox("Select Student", list(student_options.keys()))
                student_id = student_options[selected_student]
            
            with col2:
                course_options = {f"{row['CourseName']} ({row['CourseCode']})": row['CourseID'] 
                                for _, row in df_courses.iterrows()}
                selected_course = st.selectbox("Select Course", list(course_options.keys()))
                course_id = course_options[selected_course]
            
            semester = st.selectbox("Select Semester", ["Fall 2024", "Spring 2025", "Fall 2025", "Spring 2026"])
            
            submitted = st.form_submit_button("✓ Register Student", use_container_width=True)
            
            if submitted:
                success, message = db.register_student(student_id, course_id, semester)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

# ==================== PAGE: FEES ====================

def render_fees():
    """Render fee management page."""
    st.header("💳 Fee Management Portal")
    
    tab_view, tab_pay, tab_pending = st.tabs(["All Fees", "Process Payment", "Pending Fees"])
    
    with tab_view:
        st.subheader("Student Fee Status")
        
        status = st.radio("Filter", ["All", "Paid", "Pending"], horizontal=True)
        df_fees = db.get_fee_status_list(status)
        
        if not df_fees.empty:
            # Add status badge
            df_fees['Status Badge'] = df_fees['FeeStatus'].apply(
                lambda x: f'<span class="badge-paid">✓ {x}</span>' 
                if x == 'Paid' else f'<span class="badge-pending">⚠ {x}</span>'
            )
            
            display_cols = ['studentName', 'DepartmentName', 'TotalFee', 'PaidAmount', 'DueAmount', 'FeeStatus']
            if 'DepartmentName' in df_fees.columns:
                st.dataframe(df_fees[display_cols], use_container_width=True, hide_index=True)
            else:
                st.dataframe(df_fees, use_container_width=True, hide_index=True)
        else:
            st.info("No fee records found")
    
    with tab_pay:
        st.subheader("💰 Record Payment")
        
        pending = db.get_pending_fees()
        if not pending.empty:
            fee_options = {f"{row['studentName']} — Due: {row['DueAmount']:,} PKR": row['studentId'] 
                         for _, row in pending.iterrows()}
            
            with st.form("payment_form"):
                selected_student = st.selectbox("Select Student with Due Balance", list(fee_options.keys()))
                student_id = fee_options[selected_student]
                
                # Get remaining due amount
                student_data = pending[pending['studentId'] == student_id].iloc[0]
                max_payment = int(student_data['DueAmount'])
                
                amount = st.number_input("Payment Amount (PKR)", min_value=1000, max_value=max_payment, step=1000)
                
                submitted = st.form_submit_button("Record Payment", use_container_width=True)
                
                if submitted:
                    success, message = db.update_fee_payment(student_id, amount)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        else:
            st.success("✓ All fees are paid up!")
    
    with tab_pending:
        st.subheader("⚠️ Pending Fee Accounts")
        
        pending = db.get_pending_fees()
        if not pending.empty:
            st.dataframe(pending, use_container_width=True, hide_index=True)
            total_due = int(pending['DueAmount'].sum())
            st.metric("Total Outstanding", f"{total_due:,} PKR")
        else:
            st.success("✓ No pending fees")

# ==================== PAGE: ANALYTICS ====================

def render_analytics():
    """Render analytics page."""
    st.header("📊 Analytics & Insights")
    
    tab_grades, tab_enrollment, tab_gpa = st.tabs(["Grade Distribution", "Enrollment", "Student GPA"])
    
    with tab_grades:
        st.subheader("Grade Distribution")
        df_grades = db.get_grade_statistics()
        if not df_grades.empty:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.bar_chart(df_grades.set_index('Grade')['StudentCount'])
            with col2:
                for _, row in df_grades.iterrows():
                    st.write(f"**{row['Grade']}**: {int(row['StudentCount'])} students ({row['Percentage']}%)")
        else:
            st.info("No grade data available")
    
    with tab_enrollment:
        st.subheader("Enrollment by Semester")
        df_enrollment = db.get_enrollment_by_semester()
        if not df_enrollment.empty:
            st.dataframe(df_enrollment, use_container_width=True, hide_index=True)
        else:
            st.info("No enrollment data")
    
    with tab_gpa:
        st.subheader("Top Students by GPA")
        df_gpa = db.get_average_gpa_by_student()
        if not df_gpa.empty:
            st.dataframe(df_gpa, use_container_width=True, hide_index=True)
        else:
            st.info("No GPA data available")

# ==================== PAGE: SETTINGS ====================

def render_settings():
    """Render settings page."""
    st.header("⚙️ Settings & System Info")
    
    tab_info, tab_db, tab_about = st.tabs(["System Info", "Database", "About"])
    
    with tab_info:
        st.subheader("Application Information")
        st.write(f"**Application:** Course Registration System")
        st.write(f"**Version:** 1.0.0")
        st.write(f"**Last Updated:** {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**Framework:** Streamlit")
        st.write(f"**Backend:** Python + SQL Server")
    
    with tab_db:
        st.subheader("Database Connection")
        system_info = db.get_system_info()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Database", system_info['database'])
        with col2:
            st.metric("Driver", system_info['driver'])
        with col3:
            status_color = "green" if system_info['server'] == "Connected" else "red"
            st.metric("Connection", system_info['server'])
        
        if st.button("🔄 Test Connection"):
            if db.test_connection():
                st.success("✓ Database connection successful!")
            else:
                st.error("✗ Database connection failed!")
    
    with tab_about:
        st.subheader("About This System")
        st.write("""
        This is a professional Course Registration System designed for academic 
        institutions to manage:
        
        - **Student Management**: Enrollment, profiles, and tracking
        - **Course Management**: Course offerings and capacity management
        - **Registrations**: Student course registration and history
        - **Fee Management**: Payment tracking and reconciliation
        - **Analytics**: Performance metrics and insights
        
        Built with modern technologies for reliability and performance.
        """)

# ==================== MAIN APPLICATION ====================

def main():
    """Main application entry point."""
    
    # Sidebar Navigation using option_menu
    with st.sidebar:
        page = option_menu(
            menu_title="Navigation",
            options=["Dashboard", "Students", "Courses", "Registrations", "Fees", "Analytics", "Settings"],
            icons=["speedometer2", "person-badge", "journal-bookmark", "card-checklist", "credit-card", "graph-up", "gear"],
            menu_icon="cast",
            default_index=0
        )
    
    st.sidebar.markdown("---")
    
    # Display current metrics in sidebar
    try:
        metrics = db.get_overview_metrics()
        st.sidebar.write("### Quick Stats")
        st.sidebar.metric("Students", metrics['students'])
        st.sidebar.metric("Courses", metrics['courses'])
        st.sidebar.metric("Registrations", metrics['enrollments'])
        st.sidebar.metric("Pending Fees", metrics['pending_fees'])
    except:
        pass
    
    st.sidebar.markdown("---")
    st.sidebar.caption(f"Course Registration System v1.0\nLast update: {datetime.now().strftime('%H:%M:%S')}")
    
    # Route to selected page
    if page == "Dashboard":
        render_dashboard()
    elif page == "Students":
        render_students()
    elif page == "Courses":
        render_courses()
    elif page == "Registrations":
        render_registrations()
    elif page == "Fees":
        render_fees()
    elif page == "Analytics":
        render_analytics()
    elif page == "Settings":
        render_settings()

if __name__ == "__main__":
    main()