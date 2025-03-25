from flask import Flask
from models import db
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    try:

        db.session.execute(text('ALTER TABLE user DROP COLUMN password'))
        db.session.commit()
        print("Plaintext password column removed successfully!")
    except Exception as e:
        print(f"Error removing column: {e}")