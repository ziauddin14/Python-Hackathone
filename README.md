# 🎓 Student Management System

A modern, full-featured Student Management System built with Python, Streamlit, and Object-Oriented Programming principles. This web application provides an intuitive interface for managing student records with comprehensive CRUD operations, advanced search, and filtering capabilities.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ Features

### 🔹 Core Functionality
- **Add Students**: Create new student records with validation
- **View Students**: Display all students in a clean table format
- **Update Students**: Modify existing student information
- **Delete Students**: Remove student records from the system

### 🔹 Advanced Features
- **Smart Search**: Real-time search by student name
- **Multi-Filter System**: 
  - Filter by Grade (A-F)
  - Filter by Age Range (slider-based)
  - Filter by Performance Range (1-100)
- **Input Validation**: 
  - Email format validation using regex
  - Required field validation
  - Range validation for age and performance
- **Auto-Generated IDs**: Unique UUID for each student
- **Timestamp Tracking**: Automatic creation timestamp for each record
- **Form Auto-Clear**: Forms automatically clear after successful submission

### 🔹 User Experience
- **Modern UI**: Clean, responsive design with Streamlit
- **Tabbed Interface**: Organized into intuitive sections
- **Real-time Feedback**: Success/error messages for all operations
- **Data Persistence**: JSON-based storage for easy data management

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.7+
- **Architecture**: Object-Oriented Programming (OOP)
- **Data Storage**: JSON (file-based)
- **Libraries**:
  - `streamlit` - Web framework
  - `uuid` - Unique ID generation
  - `datetime` - Timestamp management
  - `json` - Data serialization
  - `re` - Email validation

---

## 📁 Project Structure

```
student_managment/
│
├── models/
│   └── student.py          # Student class with OOP implementation
│
├── services/
│   └── manager.py          # StudentManager class for business logic
│
├── ui/
│   └── app.py              # Streamlit web application
│
├── data/
│   └── students.json       # JSON database for student records
│
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

### Architecture Overview

- **Models Layer** (`models/student.py`): Defines the `Student` class with attributes and methods
- **Services Layer** (`services/manager.py`): Handles business logic, CRUD operations, and data persistence
- **UI Layer** (`ui/app.py`): Streamlit-based user interface with forms and interactive components
- **Data Layer** (`data/students.json`): JSON file for persistent storage

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd student_managment
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run ui/app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Adding a Student
1. Navigate to the **"Add Student"** tab
2. Fill in the required fields:
   - **Name**: Student's full name (required)
   - **Age**: Student's age (minimum: 1)
   - **Grade**: Select from A, B, C, D, E, or F
   - **Performance**: Slide to set performance score (1-100)
   - **Email**: Valid email address (required, validated)
3. Click **"Add Student"** button
4. Form will automatically clear upon successful submission

### Viewing & Searching Students
1. Go to the **"View / Search Students"** tab
2. Use the search bar to find students by name (case-insensitive)
3. Apply filters:
   - **Grade Filter**: Select specific grade or "All"
   - **Age Range**: Use slider to set min/max age
   - **Performance Range**: Use slider to set min/max performance
4. View filtered results in the table below

### Updating a Student
1. Open the **"Update Student"** tab
2. Select a student from the dropdown
3. Modify any fields as needed
4. Click **"Update Student"** to save changes
5. Validation ensures data integrity

### Deleting a Student
1. Go to the **"Update Student"** tab
2. Select the student to delete
3. Click **"Delete Student"** button
4. Confirm the deletion (student will be permanently removed)

---

## 🎯 Key Features Explained

### Input Validation
- **Email Validation**: Uses regex pattern `^[\w\.-]+@[\w\.-]+\.\w+$` to ensure valid email format
- **Required Fields**: Name and Email are mandatory
- **Range Validation**: Age must be > 0, Performance must be between 1-100

### Data Management
- **Unique IDs**: Each student gets a UUID4 identifier
- **Automatic Timestamps**: Creation date/time recorded automatically
- **JSON Storage**: Lightweight, human-readable data format
- **Persistent Storage**: Data survives application restarts

### Search & Filter
- **Real-time Search**: Instant filtering as you type
- **Case-Insensitive**: Search works regardless of letter case
- **Combined Filters**: Multiple filters can be applied simultaneously
- **Dynamic Results**: Table updates immediately based on filters

---

## 🔧 Configuration

### Data File Location
The default data file is located at `data/students.json`. To change this, modify the path in `ui/app.py`:

```python
manager = StudentManager("data/students.json")  # Change path here
```

### Customization
- **Grade Options**: Modify the grade list in `ui/app.py` (line 26, 76, 121)
- **Performance Range**: Adjust min/max values in slider components
- **Age Range**: Modify age constraints in number inputs

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'models'`
- **Solution**: Ensure you're running the app from the project root directory, or the path configuration in `app.py` is correct

**Issue**: Data not persisting
- **Solution**: Check file permissions for `data/students.json`. Ensure the `data/` directory exists.

**Issue**: Form not clearing after submission
- **Solution**: The form uses `clear_on_submit=True` parameter. If issues persist, check Streamlit version compatibility.

---

## 🚀 Future Enhancements

Potential features for future development:

- [ ] Export data to CSV/Excel
- [ ] Import students from CSV
- [ ] Student statistics dashboard (charts/graphs)
- [ ] Multi-user authentication
- [ ] Database integration (PostgreSQL, MySQL)
- [ ] Email notifications
- [ ] Student photo upload
- [ ] Attendance tracking
- [ ] Grade analytics and reports
- [ ] Dark mode theme

---

## 🤝 Contributing

This project is open for contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Hackathon Contributions
- Bug fixes and improvements
- New feature implementations
- UI/UX enhancements
- Documentation improvements
- Performance optimizations

---

## 📝 Code Quality

- **OOP Principles**: Clean separation of concerns with Models, Services, and UI layers
- **Error Handling**: Try-except blocks for file operations
- **Code Organization**: Modular structure for easy maintenance
- **Validation**: Comprehensive input validation
- **User Feedback**: Clear success/error messages

---

## 📊 Sample Data Structure

Each student record contains:
```json
{
    "id": "unique-uuid-here",
    "name": "Student Name",
    "age": 20,
    "grade": "A",
    "performance": 85,
    "email": "student@example.com",
    "created_at": "2025-11-22 22:25:06"
}
```

---

## 🎓 Learning Outcomes

This project demonstrates:
- Object-Oriented Programming concepts
- Web application development with Streamlit
- File-based data persistence
- Form handling and validation
- Search and filter implementation
- Modern UI/UX design principles

---

## 📄 License

This project is licensed under the MIT License - feel free to use it for learning, hackathons, or personal projects!

---

## 👨‍💻 Author

**Student Management System**
- Built with ❤️ using Python and Streamlit
- Perfect for educational institutions and hackathons

---

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Python community for excellent documentation
- All contributors and testers

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the code comments for implementation details

---

**⭐ If you find this project helpful, please give it a star!**

---

*Built for hackathons, optimized for learning, designed for efficiency.* 🚀

