# course-registration-system-database-project

A full-stack Course Registration System built with Microsoft SQL Server, Python, and Streamlit, showcasing database design, SQL queries, CRUD operations, backend integration, and an interactive dashboard for managing academic records and analytics.

## 🎯 Overview

This project demonstrates practical implementation of Database Systems concepts through a real-world application. Although AI tools were used to speed up UI development and improve frontend design, the database integration, SQL implementation, backend logic, and project architecture were developed as part of the learning process.

**The objective**: Understand how relational databases communicate with real-world applications.

## ✨ Features

### ✅ Student Management
- View all students
- Search students
- Department filtering
- Student details

### ✅ Course Management
- Course catalog
- Enrollment details
- Popular courses
- Course information

### ✅ Registration System
- Register students to courses
- Cancel registrations
- Prevent duplicate registration
- View registration history

### ✅ Fee Management
- Fee status tracking
- Payment updates
- Pending fee tracking
- Payment records

### ✅ Analytics Dashboard
- Student statistics
- Course statistics
- GPA analytics
- Enrollment trends
- Visual data representation

### ✅ System Information
- Database connection status
- SQL Server integration details
- Performance metrics

## 🛠️ Technologies Used

### Backend
- **Python** - Core backend logic

### Frontend
- **Streamlit** - Interactive web interface

### Database
- **Microsoft SQL Server** - Database management system

### Python Libraries
- `streamlit` - Web framework
- `pandas` - Data manipulation and analysis
- `pyodbc` - SQL Server connectivity
- `numpy` - Numerical computations
- `plotly` - Interactive visualizations
- `functools` - LRU Cache for performance optimization

## 📊 Database Concepts Implemented

This project demonstrates practical implementation of key database concepts:

- Primary Keys
- Foreign Keys
- Table Relationships
- Constraints
- Normalized Tables
- Views
- Stored Queries
- Aggregate Functions
- GROUP BY & HAVING
- ORDER BY
- SQL Joins (INNER, LEFT)
- Transactions
- Error Handling

## 💾 SQL Features Used

The application contains **more than 30 SQL queries**, including:

### Basic Operations
- SELECT, INSERT, UPDATE, DELETE

### Filtering & Sorting
- WHERE clause
- ORDER BY
- GROUP BY
- HAVING

### Aggregate Functions
- COUNT()
- AVG()
- SUM()
- MAX()
- MIN()

### SQL Joins
- INNER JOIN - Combine students and courses
- LEFT JOIN - Include students without registrations
- Multiple joins across Students, Courses, Departments, Registration, Fees, and Instructor tables

## 🏗️ Project Architecture

```
┌─────────────────────────────────┐
│        Streamlit UI             │
│   (7 Application Pages)         │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│      Python Backend             │
│  (CRUD Operations, Logic)       │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│      SQL Queries                │
│    (30+ Queries)                │
└──────────────┬──────────────────┘
               │
┌──────────────▼──────────────────┐
│   Microsoft SQL Server          │
│  (Database Management)          │
└─────────────────────────────────┘
```

### Data Flow
```
SQL Server → pyodbc Connection → Python Functions → 
Pandas DataFrames → Streamlit Interface
```

## 📄 Application Pages

1. **Dashboard** - Overview and key metrics
2. **Students** - Student management and search
3. **Courses** - Course catalog and details
4. **Registrations** - Registration management
5. **Fee Management** - Fee tracking and payment updates
6. **Analytics** - Statistical analysis and trends
7. **Settings** - System configuration and database info

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Microsoft SQL Server (local or remote)
- pip package manager

### Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/course-registration-system.git
cd course-registration-system
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure database connection:
- Update your SQL Server connection details in `database.py`
- Run `Course_registration_system.sql` to set up the database

4. Run the application:
```bash
streamlit run app.py
```

5. Open your browser and navigate to:
```
http://localhost:8501
```

## 📋 Requirements

Create `requirements.txt`:
```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.23.0
pyodbc>=4.0.37
plotly>=5.14.0
```

Or generate from your environment:
```bash
pip freeze > requirements.txt
```

## 📁 Project Structure

```
Course-Registration-System/
│
├── README.md
├── requirements.txt
├── app.py                          # Main Streamlit application
├── database.py                     # Database connection & queries
├── Course_registration_system.sql  # Database schema & setup
├── assets/
│   ├── dashboard.png
│   ├── students.png
│   └── analytics.png
├── LICENSE
└── .gitignore
```

## 🎓 Learning Outcomes

Through this project, I learned:

✔️ Database Design and Normalization
✔️ SQL Query Writing and Optimization
✔️ SQL Server Connectivity with Python
✔️ CRUD Operations Implementation
✔️ Data Analytics using SQL
✔️ Streamlit Application Development
✔️ Backend Integration and Architecture
✔️ Error Handling and Debugging
✔️ Python Database Programming
✔️ Professional Code Structure

## 🔄 Database Workflow

1. **User Input** → Streamlit Frontend
2. **Process Request** → Python Backend
3. **Execute Query** → SQL Server
4. **Return Data** → Pandas DataFrame
5. **Display Results** → Streamlit UI

## 🔮 Future Improvements

- [ ] Authentication System
  - User login with role-based access
  - Password encryption
  
- [ ] Email Notifications
  - Course registration confirmations
  - Fee payment reminders
  
- [ ] Export Reports
  - PDF/Excel export functionality
  - Attendance reports
  
- [ ] Attendance Module
  - Mark attendance
  - Track attendance records
  
- [ ] REST API
  - Backend API endpoints
  - Mobile app integration
  
- [ ] Cloud Deployment
  - Deploy to AWS/Azure
  - Cloud database connectivity

## 📌 Academic Information

- **Course**: Database Systems
- **Semester**: 4th Semester BS Computer Science
- **University**: University of Management and Technology (UMT)
- **Academic Year**: [Your Year]

## 🤖 AI Assistance Transparency

This project was developed as part of my learning journey in the Database Systems course. I used AI tools to:
- Improve frontend design and UI refinement
- Assist with code suggestions and debugging
- Enhance code documentation

However, I personally completed:
- Database design and schema creation
- SQL query implementation
- SQL Server integration and connectivity
- CRUD operations development
- Backend logic and error handling
- Project structure and architecture
- Testing and debugging
- Overall project integration

This approach demonstrates how modern developers leverage AI-assisted tools while maintaining deep understanding of core concepts and ownership of the project.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 💬 Support

If you have any questions or need help with the project:
1. Check the documentation in this README
2. Review the SQL schema in `Course_registration_system.sql`
3. Examine the code comments in `database.py` and `app.py`

## 🎓 Getting Started

Ready to explore the system? Start with:
1. Install the required packages
2. Set up your SQL Server database
3. Run the Streamlit application
4. Explore the Dashboard page first to get an overview

---

**⭐ If you find this project helpful, please consider giving it a star on GitHub!**

Made with ❤️ as a Database Systems project
