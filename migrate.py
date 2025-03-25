from flask import Flask
from models import db, User
from flask_bcrypt import Bcrypt
from sqlalchemy import text, inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
bcrypt = Bcrypt(app)

def migrate_passwords():
    with app.app_context():
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('user')]
        
        # If the password_hash column does not exist, add it
        if 'password_hash' not in columns:
            print("password_hash column not found. Adding it...")
            # Add the password_hash column to the user table
            db.session.execute(text('ALTER TABLE user ADD COLUMN password_hash TEXT'))
            db.session.commit()
            print("Added password_hash column to user table.")
        
        # If the password column exists, migrate the passwords
        if 'password' in columns:
            # Fetch all users with their existing passwords
            users = db.session.execute(text('SELECT id, username, password FROM user')).fetchall()
            
            print(f"Found {len(users)} users to migrate...")

            for user_data in users:
                # Find the user in the ORM
                user = User.query.get(user_data.id)

                if user and user_data.password:  # Make sure the user has a password
                    # Hash the existing password
                    password_hash = bcrypt.generate_password_hash(user_data.password).decode('utf-8')
                    
                    # Update the user with the hashed password
                    user.password_hash = password_hash
                    print(f"Migrated password for user: {user.username}")

            # Commit the changes to the database
            db.session.commit()
            print("Password migration completed successfully!")
        else:
            print("No password column found to migrate.")

if __name__ == '__main__':
    migrate_passwords()
