import os
import sys
import cv2
import tensorflow as tf
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Flask,render_template,request,redirect,session,jsonify,flash,url_for
from flask_bcrypt import Bcrypt
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from database import db
from database.models import User
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model_interface import predict_image
import pymysql

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY
db.init_app(app)
bcrypt = Bcrypt(app)
model=tf.keras.models.load_model("../model/best_model.keras")

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('detect'))
        else:
            flash("Invalid login credentials", "danger")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out.", "info")
    return redirect(url_for('login'))
    
@app.route('/detect', methods=['GET', 'POST'])
@login_required
def detect():
    detected_pokemon = None
    if request.method == 'POST':
        file = request.files['file']
        if not file or file.filename == '':
            flash("No file selected", "danger")
            return redirect(request.url)

        # Detect Pokémon in real-time without storing
        detected_pokemon = predict_image(file)

    return render_template('detect.html', detected_pokemon=detected_pokemon)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True,port=5000)