from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configure SQLite database file path
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'hello' 


# Define User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

# Create tables automatically inside an app context
with app.app_context():
    db.create_all()

# Landing Page
@app.route('/')
def landing():
    return render_template('homepage.html')


# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None  # To store messages

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            message = "Email and password are required"
            return render_template('register.html', message=message), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            message = "Email already registered! Please log in."
            return render_template('register.html', message=message), 409

        try:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(email=email, password=hashed_password)
            
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            message = f"Error: {str(e)}"
            return render_template('register.html', message=message), 500

    return render_template('register.html', message=message)


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            message = "Email and password are required"
            return render_template('login.html', message=message), 400

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['email'] = user.email
            print("✅ Login successful, redirecting to home...")  # Debug print
            return redirect(url_for("landing"))

        else:
            message = "Invalid credentials, please try again."
            print("❌ Login failed, showing login page again")  # Debug print
            return render_template('login.html', message=message)

    return render_template('login.html', message=message)



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
