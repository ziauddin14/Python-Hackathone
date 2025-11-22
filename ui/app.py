
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from models.student import Student
from services.manager import StudentManager

import re
import json
import datetime

# ----------------- Setup -----------------
st.set_page_config(page_title="Student Management System", layout="wide")
manager = StudentManager("data/students.json")
HISTORY_FILE = os.path.join("data", "history.json")

# ensure data folder and history file exist
os.makedirs("data", exist_ok=True)
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f, indent=4)

# ----------------- Helper: History Functions -----------------
def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def push_history(action_type, data, prev_data=None):
    """
    action_type: "add", "delete", "update"
    data: the student dict affected (for add/delete) or new_data (for update)
    prev_data: for update, the previous student dict
    """
    h = load_history()
    entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action_type,
        "data": data,
        "prev_data": prev_data
    }
    h.append(entry)
    save_history(h)

def undo_last_action():
    h = load_history()
    if not h:
        st.warning("History empty — nothing to undo.")
        return
    last = h.pop()  # remove last action
    save_history(h)

    action = last["action"]
    data = last["data"]
    prev_data = last.get("prev_data")

    # Undo logic
    if action == "add":
        # remove student with id == data["id"]
        manager.delete_student(data["id"])
        st.success(f"Undo: Added student (ID {data['id']}) removed.")
    elif action == "delete":
        # re-add the deleted student (data holds the full student dict)
        # append directly to manager.students and save (works with current manager implementation)
        manager.students.append(data)
        manager.save_to_json()
        st.success(f"Undo: Deleted student (ID {data['id']}) restored.")
    elif action == "update":
        # prev_data holds previous state — restore it
        manager.update_student(prev_data["id"], prev_data)
        st.success(f"Undo: Student (ID {prev_data['id']}) reverted to previous state.")
    else:
        st.error("Unknown action in history — cannot undo.")

# ----------------- Simple Admin Auth -----------------
# For hackathon: simple credentials (you can change these)
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def do_login(user, pwd):
    if user == ADMIN_USER and pwd == ADMIN_PASS:
        st.session_state.logged_in = True
        st.session_state.username = user
        st.success("Logged in as admin.")
    else:
        st.session_state.logged_in = False
        st.error("Invalid credentials.")

def do_logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out.")

# ----------------- Top bar: Login + Undo Button -----------------
colA, colB, colC = st.columns([3,1,1])
with colA:
    st.title("Student Management System")
with colB:
    if st.session_state.logged_in:
        st.write(f"👋 Admin: **{st.session_state.username}**")
        if st.button("Logout", key="logout_btn"):
            do_logout()
    else:
        with st.expander("Admin Login"):
            user = st.text_input("Username", key="login_user")
            pwd = st.text_input("Password", type="password", key="login_pwd")
            if st.button("Login", key="login_btn"):
                do_login(user, pwd)

with colC:
    if st.button("Undo Last Action", key="undo_btn"):
        undo_last_action()

st.markdown("---")

# ----------------- Tabs -----------------
tab1, tab2, tab3, tab4 = st.tabs([" Add Student", " View / Search Students", "Update / Delete Student", "📊 Dashboard"])

# ----------------- TAB 1: Add Student (admin only) -----------------
with tab1:
    st.header("Add New Student")
    if not st.session_state.logged_in:
        st.info("You must login as admin to Add students.")
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Name", key="name_add")
        age = st.number_input("Age", min_value=1, key="age_add")
        grade = st.selectbox("Grade", ["A","B","C","D","E","F"], key="grade_add")
        performance = st.slider("Performance", 1, 100, key="perf_add")
        email = st.text_input("Email", key="email_add")
        submitted = st.form_submit_button("Add Student")

        if submitted:
            if not st.session_state.logged_in:
                st.error("Only admin can add students. Please login.")
            else:
                errors = []
                if not name.strip():
                    errors.append("Name is required!")
                if not email.strip():
                    errors.append("Email is required!")
                elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                    errors.append("Invalid email format!")
                if age <= 0:
                    errors.append("Age must be > 0!")
                if not (1 <= performance <= 100):
                    errors.append("Performance must be 1-100!")
                if errors:
                    for e in errors:
                        st.error(e)
                else:
                    student = Student(name, age, grade, performance, email)
                    manager.add_student(student)
                    # push to history (store dict)
                    push_history("add", student.to_dict())
                    st.success(f"{name} added successfully!")

# ----------------- TAB 2: View / Search / Auto-suggest / Profile -----------------
with tab2:
    st.header("All Students — Search, Filters & Profiles")

    students = manager.list_students()  # list of dicts

    # ---------- Auto-suggest search input ----------
    st.subheader("Search & Smart Filters")
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        # user types here
        keyword = st.text_input("Search by name (type to see suggestions)", key="view_search")
        # show suggestions when typing
        suggestions = []
        if keyword and len(keyword.strip()) >= 1:
            lower = keyword.lower()
            for s in students:
                if lower in s["name"].lower():
                    suggestions.append(f"{s['name']} — {s['id']}")
        if suggestions:
            selected_suggestion = st.selectbox("Suggestions (select to autofill)", options=[""] + suggestions, key="suggest_box")
            if selected_suggestion:
                # extract name portion before ' — '
                suggested_name = selected_suggestion.split(" — ")[0]
                # override keyword in session so filter uses it
                st.session_state.view_search = suggested_name
                keyword = suggested_name

    with col2:
        filter_grade = st.selectbox("Grade", ["All","A","B","C","D","E","F"], key="view_grade_filter")
    with col3:
        # age range
        min_age = st.number_input("Min Age", min_value=0, value=0, key="view_min_age")
        max_age = st.number_input("Max Age", min_value=0, value=100, key="view_max_age")

    perf_col1, perf_col2 = st.columns(2)
    with perf_col1:
        min_perf = st.number_input("Min Performance", min_value=0, value=0, key="view_min_perf")
    with perf_col2:
        max_perf = st.number_input("Max Performance", min_value=0, value=100, key="view_max_perf")

    # ---------- Filtering logic ----------
    filtered_students = []
    for s in students:
        if keyword and keyword.lower() not in s["name"].lower():
            continue
        if filter_grade != "All" and s["grade"] != filter_grade:
            continue
        if not (min_age <= s["age"] <= max_age):
            continue
        if not (min_perf <= s["performance"] <= max_perf):
            continue
        filtered_students.append(s)

    # ---------- Display table (HTML) with highlights + view button ----------
    st.subheader("Students")
    if filtered_students:
        st.markdown("""
        <style>
        .top {background-color: ;}
        .low {background-color: red;}
        table, th, td {border:1px solid #ddd; border-collapse: collapse; padding:8px;}
        th {background: blue;}
        </style>
        """, unsafe_allow_html=True)

        # create a simple interactive layout: table + "View" selectbox to open profile
        table_html = "<table><tr><th>ID</th><th>Name</th><th>Age</th><th>Grade</th><th>Performance</th><th>Email</th></tr>"
        for s in filtered_students:
            row_class = "top" if s["performance"] > 90 else "low" if s["performance"] < 50 else ""
            table_html += f'<tr class="{row_class}">'
            table_html += f"<td>{s['id']}</td><td>{s['name']}</td><td>{s['age']}</td><td>{s['grade']}</td><td>{s['performance']}</td><td>{s['email']}</td></tr>"
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)

        # --------- Profile viewer: select student to view details ----------
        st.subheader("Student Profile")
        sel_options = [f"{s['name']} — {s['id']}" for s in filtered_students]
        selected = st.selectbox("Select a student to view profile", options=[""] + sel_options, key="profile_select")
        if selected:
            sel_id = selected.split(" — ")[1]
            student_obj = next((x for x in filtered_students if str(x["id"]) == str(sel_id)), None)
            if student_obj:
                # display profile card
                st.markdown(f"""
                <div style="background:blue;padding:16px;border-radius:8px;border:1px solid #eee;">
                    <h3 style="margin:0 0 8px 0;">{student_obj['name']} <span ">(ID: {student_obj['id']}) </span></h3>
                    <p style="margin:0;"><b>Age:</b> {student_obj['age']}</p>
                    <p style="margin:0;"><b>Grade:</b> {student_obj['grade']}</p>
                    <p style="margin:0;"><b>Performance:</b> {student_obj['performance']}</p>
                    <p style="margin:0;"><b>Email:</b> {student_obj['email']}</p>
                    <p style="margin-top:8px;color:;">Added on: {student_obj.get('created_at','-')}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No students match the criteria.")

# ----------------- TAB 3: Update / Delete (admin only) -----------------
with tab3:
    st.header("Update / Delete Student")
    if not st.session_state.logged_in:
        st.info("You must login as admin to Update or Delete students.")
    students = manager.list_students()
    if not students:
        st.info("No students to update.")
    else:
        # select student (searchable via selectbox)
        sel_map = {f"{s['name']} — {s['id']}": s["id"] for s in students}
        selected_key = st.selectbox("Select student to edit", options=[""] + list(sel_map.keys()), key="upd_select_box")
        if selected_key:
            sid = sel_map[selected_key]
            selected_student = next(s for s in students if s["id"] == sid)
            # show editable form
            name = st.text_input("Name", selected_student["name"], key="upd_name")
            age = st.number_input("Age", min_value=1, value=int(selected_student["age"]), key="upd_age")
            grade = st.selectbox("Grade", ["A","B","C","D","E","F"], index=["A","B","C","D","E","F"].index(selected_student["grade"]), key="upd_grade")
            performance = st.slider("Performance", 1, 100, value=int(selected_student["performance"]), key="upd_perf")
            email = st.text_input("Email", selected_student["email"], key="upd_email")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update Student", key="do_update"):
                    if not st.session_state.logged_in:
                        st.error("Only admin can update — please login.")
                    else:
                        errors = []
                        if not name.strip():
                            errors.append("Name required.")
                        if not email.strip():
                            errors.append("Email required.")
                        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                            errors.append("Invalid email.")
                        if age <= 0:
                            errors.append("Invalid age.")
                        if errors:
                            for e in errors:
                                st.error(e)
                        else:
                            prev = selected_student.copy()
                            new_data = {"name":name,"age":age,"grade":grade,"performance":performance,"email":email}
                            manager.update_student(sid, new_data)
                            push_history("update", new_data, prev_data=prev)
                            st.success("Student updated.")
            with col2:
                if st.button("Delete Student", key="do_delete"):
                    if not st.session_state.logged_in:
                        st.error("Only admin can delete — please login.")
                    else:
                        # save snapshot to history first
                        push_history("delete", selected_student)
                        manager.delete_student(sid)
                        st.error("Student deleted.")

# ----------------- TAB 4: Dashboard -----------------
with tab4:
    st.header("Quick Statistics / Dashboard")
    students = manager.list_students()
    total_students = len(students)
    if total_students:
        avg_perf = sum(s["performance"] for s in students)/total_students
        highest_perf = max(s["performance"] for s in students)
        lowest_perf = min(s["performance"] for s in students)
        grade_count = {}
        for s in students:
            grade_count[s["grade"]] = grade_count.get(s["grade"],0)+1

        st.subheader("Total Students"); st.info(f"{total_students}")
        st.subheader("Average Performance"); st.success(f"{avg_perf:.2f}")
        st.subheader("Highest Performer(s)")
        st.success(f"{', '.join([s['name'] for s in students if s['performance']==highest_perf])} → {highest_perf}")
        st.subheader("Lowest Performer(s)")
        st.error(f"{', '.join([s['name'] for s in students if s['performance']==lowest_perf])} → {lowest_perf}")

        st.subheader("Students per Grade")
        grade_table = "<table><tr><th>Grade</th><th>Count</th></tr>"
        for g,c in grade_count.items():
            grade_table += f"<tr><td>{g}</td><td>{c}</td></tr>"
        grade_table += "</table>"
        st.markdown(grade_table, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("Top 5 by Performance")
        top5 = sorted(students, key=lambda x: x["performance"], reverse=True)[:5]
        for s in top5:
            st.markdown(f"**{s['name']}** — {s['performance']}")

        st.subheader("Lowest 5 by Performance")
        low5 = sorted(students, key=lambda x: x["performance"])[:5]
        for s in low5:
            st.markdown(f"**{s['name']}** — {s['performance']}")
    else:
        st.info("No students available for statistics.")
