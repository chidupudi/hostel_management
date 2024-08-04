from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e9b1d85b4a6e4b31a88f8d3e682f1c57'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Hostel_Management'


mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'student.student_login'

from routes.student_routes import student_bp
from routes.admin_routes import admin_bp

app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)
