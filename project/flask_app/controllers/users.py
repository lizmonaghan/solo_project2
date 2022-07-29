from flask_app import app
from flask import render_template,redirect,request,flash, session
from flask_app.models.user import User
from flask_app.models.cat import Cat
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register',methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/cats')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_user_email(request.form)

    if not user:
        flash("Invalid Email")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/cats')

@app.route('/cats')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html",users=User.get_by_id(data),cats=Cat.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')