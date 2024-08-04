import hmac
from flask_login import UserMixin
from app import mongo, bcrypt

class Student(UserMixin):
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.room = None
        self.feedback = None

    def save_to_db(self):
        mongo.db.students.insert_one(self.__dict__)

    @staticmethod
    def get_by_email(email):
        student_data = mongo.db.students.find_one({'email': email})
        if student_data:
            return Student(**student_data)
        return None

    @staticmethod
    def get_by_id(id):
        student_data = mongo.db.students.find_one({'_id': id})
        if student_data:
            return Student(**student_data)
        return None

class Admin(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def save_to_db(self):
        mongo.db.admins.insert_one(self.__dict__)

    @staticmethod
    def get_by_username(username):
        admin_data = mongo.db.admins.find_one({'username': username})
        if admin_data:
            return Admin(**admin_data)
        return None
