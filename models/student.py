import datetime
import uuid

class Student:
    def __init__(self, name, age, grade, performance, email):
        self.id = str(uuid.uuid4())   # unique student id
        self.name = name
        self.age = age
        self.grade = grade
        self.performance = performance
        self.email = email
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "performance": self.performance,
            "email": self.email,
            "created_at": self.created_at
        }
