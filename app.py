from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from database import db, User, init_db

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'

# Ensure the instance folder exists
if not os.path.exists(os.path.join(app.instance_path)):
    os.makedirs(os.path.join(app.instance_path))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'users.db')

# 데이터베이스 초기화
init_db(app)

def save_user_info(user):
    """사용자 정보를 파일에 저장하는 함수"""
    user_info = f"ID: {user.id}\nUsername: {user.username}\nEmail: {user.email}\nPassword: {user.password}\n\n"
    with open("user_info.txt", "a") as file:
        file.write(user_info)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already registered')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        # 사용자 정보를 파일에 저장
        save_user_info(user)
        
        flash('회원가입이 완료 되었습니다. 로그인 하세요.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return 'Welcome to your dashboard!'

@app.route('/admin')
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
