import json
import os

class StudentManager:
    def __init__(self, data_file="data/students.json"):
        self.data_file = data_file
        self.students = []
        self.load_from_json()

    # Load data from JSON file
    def load_from_json(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                try:
                    self.students = json.load(f)
                except:
                    self.students = []
        else:
            self.students = []

    # Save data to JSON file
    def save_to_json(self):
        with open(self.data_file, "w") as f:
            json.dump(self.students, f, indent=4)

    # Add new student
    def add_student(self, student):
        self.students.append(student.to_dict())
        self.save_to_json()

    # List all students
    def list_students(self):
        return self.students

    # Delete student
    def delete_student(self, student_id):
        self.students = [s for s in self.students if s["id"] != student_id]
        self.save_to_json()

    # Update student
    def update_student(self, student_id, updated_data):
        for s in self.students:
            if s["id"] == student_id:
                s.update(updated_data)
                break
        self.save_to_json()

    # Search / Filter
    def search(self, keyword):
        return [s for s in self.students if keyword.lower() in s["name"].lower()]

    def filter_by_grade(self, grade):
        return [s for s in self.students if s["grade"] == grade]
