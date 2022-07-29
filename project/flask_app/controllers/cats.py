from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.cat import Cat
from flask_app.models.user import User

@app.route('/new/cat')
def new_cat():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_cat.html',users=User.get_by_id(data))


@app.route('/create/cat',methods=['POST'])
def create_cat():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Cat.validate_cat(request.form):
        return redirect('/new/cat')
    data = {
        "name": request.form["name"],
        "age": request.form["age"],
        "descr": request.form["descr"],
        "color": request.form["color"],
        "user_id": session["user_id"]
    }
    Cat.save(data)
    return redirect('/cats')

@app.route('/edit/cat/<int:id>')
def edit_cat(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_cat.html",edit=Cat.get_one(data),users=User.get_by_id(user_data))

@app.route('/update/cat',methods=['POST'])
def update_cat():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Cat.validate_cat(request.form):
        return redirect('/new/cat')
    data = {
        "name": request.form["name"],
        "age": request.form["age"],
        "descr": request.form["descr"],
        "color": request.form["color"],
        "user_id": session["user_id"]
    }
    Cat.update(data)
    return redirect('/cats')

@app.route('/cat/<int:id>')
def show_cat(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("view_cat.html",cats=Cat.get_one(data),users=User.get_by_id(user_data))

@app.route('/delete/cat/<int:id>')
def delete_cat(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Cat.delete(data)
    return redirect('/cats')