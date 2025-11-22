import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from models.student import Student
from services.manager import StudentManager

st.set_page_config(page_title="Student Management System", layout="wide")

manager = StudentManager("data/students.json")

st.title("Student Management System ")

# ----------------- Tabs -----------------
tab1, tab2, tab3 = st.tabs([" Add Student", " View / Search Students", " Update Student"])

# ========== TAB 1 – ADD STUDENT ==========
import re  # regex for email validation

with tab1:
    st.header("Add New Student")

    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Name", key="name_add")
        age = st.number_input("Age", min_value=1, key="age_add")
        grade = st.selectbox("Grade", ["A", "B", "C", "D", "E", "F"], key="grade_add")
        performance = st.slider("Performance", 1, 100, key="perf_add")
        email = st.text_input("Email", key="email_add")

        submitted = st.form_submit_button("Add Student")

        if submitted:
            # ========== Input Validation ==========
            errors = []

            if not name.strip():
                errors.append("Name is required!")
            if not email.strip():
                errors.append("Email is required!")
            else:
                # basic email regex check
                email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_regex, email):
                    errors.append("Invalid email format!")

            if age <= 0:
                errors.append("Age must be greater than 0!")
            if performance < 1 or performance > 100:
                errors.append("Performance must be between 1 and 100!")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                student = Student(name, age, grade, performance, email)
                manager.add_student(student)
                st.success(f"{name} added successfully!")


# ========== TAB 2 – VIEW + SEARCH + FILTER ==========
with tab2:
    st.header("All Students")

    # Fetch all students
    students = manager.list_students()

    # ---------- Search ----------
    search_keyword = st.text_input("Search by name:", "", key="view_search_name")
    if search_keyword:
        students = [s for s in students if search_keyword.lower() in s["name"].lower()]

    # ---------- Filters ----------
    st.subheader("Filter Students")

    # Grade Filter
    filter_grade = st.selectbox("Select Grade", ["All", "A", "B", "C", "D", "E", "F"], key="view_filter_grade")

    # Age Filter
    min_age, max_age = st.slider("Select Age Range", 0, 100, (0, 100), key="view_filter_age")

    # Performance Filter
    min_perf, max_perf = st.slider("Select Performance Range", 1, 100, (1, 100), key="view_filter_perf")

    # Apply filters
    filtered_students = []
    for s in students:
        if (filter_grade == "All" or s["grade"] == filter_grade) and \
           (min_age <= s["age"] <= max_age) and \
           (min_perf <= s["performance"] <= max_perf):
            filtered_students.append(s)

    students = filtered_students

    # ---------- Display ----------
    st.write(f"Total Students: {len(students)}")
    if students:
        st.table(students)
    else:
        st.info("No students found matching the criteria.")


# ========== TAB 3 – UPDATE / DELETE ==========
import re  # email validation regex

with tab3:
    st.header("Update / Delete Student")

    students = manager.list_students()

    if len(students) == 0:
        st.info("No students to update.")
    else:
        student_names = {s["name"]: s["id"] for s in students}
        selected_name = st.selectbox("Select Student", list(student_names.keys()), key="update_select")
        selected_id = student_names[selected_name]

        selected_student = next(s for s in students if s["id"] == selected_id)

        name = st.text_input("Name", selected_student["name"], key="name_upd")
        age = st.number_input("Age", min_value=1, value=int(selected_student["age"]), key="age_upd")
        grade = st.selectbox("Grade", ["A", "B", "C", "D", "E", "F"], index=["A","B","C","D","E","F"].index(selected_student["grade"]), key="grade_upd")
        performance = st.slider("Performance", 1, 100, value=int(selected_student["performance"]), key="perf_upd")
        email = st.text_input("Email", selected_student["email"], key="email_upd")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Update Student", key="update_btn"):
                # ========== Input Validation ==========
                errors = []

                if not name.strip():
                    errors.append("Name is required!")
                if not email.strip():
                    errors.append("Email is required!")
                else:
                    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                    if not re.match(email_regex, email):
                        errors.append("Invalid email format!")

                if age <= 0:
                    errors.append("Age must be greater than 0!")
                if performance < 1 or performance > 100:
                    errors.append("Performance must be between 1 and 100!")

                if errors:
                    for err in errors:
                        st.error(err)
                else:
                    updated_data = {
                        "name": name,
                        "age": age,
                        "grade": grade,
                        "performance": performance,
                        "email": email
                    }
                    manager.update_student(selected_id, updated_data)
                    st.success("Student updated successfully!")

        with col2:
            if st.button("Delete Student", key="delete_btn"):
                manager.delete_student(selected_id)
                st.error("Student deleted!")
