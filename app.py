from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
import os
from models import db, User, Task
from routes.auth_routes import auth_bp
from routes.task_routes import task_bp
from routes.admin_routes import admin_bp

# Create Flask application
app = Flask(__name__)

# Hardcoded secret key (intentionally insecure)
app.secret_key = os.environ.get('flask_secret_key')
app.config['DEBUG'] = True  # Debug mode enabled (intentionally insecure)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)
app.register_blueprint(admin_bp)


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('task_bp.dashboard'))
    return redirect(url_for('auth_bp.login'))


# Create database tables
@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()

        # Check if admin user exists, if not create one
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', password='admin123', is_admin=True)
            db.session.add(admin)
            db.session.commit()


if __name__ == '__main__':
    app.run(debug=False)  # Debug mode enabled (intentionally insecure)