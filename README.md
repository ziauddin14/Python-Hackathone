# Student Management System

A web-based student management application built with Python and Streamlit. Implements CRUD operations, authentication, history tracking, and analytics dashboard.

## Project Overview

This application provides a complete solution for managing student records with an intuitive web interface. It follows object-oriented design principles with clear separation between models, business logic, and presentation layers. Data persistence is handled through JSON files, making it lightweight and easy to deploy.

Key features include admin authentication, undo functionality, real-time search with auto-suggestions, multi-criteria filtering, student profiles, and a statistics dashboard.

## Project Structure

```
student_managment/
├── models/
│   └── student.py          # Student class definition
├── services/
│   └── manager.py          # Business logic and data operations
├── ui/
│   └── app.py              # Streamlit application entry point
├── data/
│   ├── students.json       # Student records database
│   └── history.json        # Action history for undo functionality
├── requirements.txt        # Python dependencies
└── README.md
```

## Tech Stack

- **Python 3.14**
- **Streamlit** - Web framework for UI
- **JSON** - File-based data storage
- **UUID** - Unique identifier generation
- **Regex** - Email validation

## Functionality

### Core Operations
- **Add Student**: Create new student records with validation (admin only)
- **View Students**: Browse all students with search and filter capabilities
- **Update Student**: Modify existing student information (admin only)
- **Delete Student**: Remove student records (admin only)

### Advanced Features
- **Admin Authentication**: Login system to protect sensitive operations
- **History & Undo**: Track all actions and undo last operation
- **Smart Search**: Real-time name search with auto-suggestions
- **Multi-Filter**: Filter by grade, age range, and performance range
- **Student Profiles**: Detailed view of individual student information
- **Dashboard**: Statistics including average performance, top/lowest performers, grade distribution

### Validation
- Email format validation using regex
- Required field checks
- Age and performance range validation
- Input sanitization

## How to Run

### Prerequisites
- Python 3.14
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd student_managment
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run ui/app.py
```

The application will start on `http://localhost:8501`

### Default Credentials
- Username: `admin`
- Password: `admin123`

---

Made by Zia Uddin
