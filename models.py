from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    #password = db.Column(db.String(80), nullable=False)  # Plain text password (intentionally insecure)
    password_hash = db.Column(db.String(128), nullable=False)
    def set_password(self,password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    def verify_password(self, password):
        if self.password_hash:
            return bcrypt.check_password_hash(self.password_hash, password)
        return False
    is_admin = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', backref='assigned_user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.title}>'