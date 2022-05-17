from flask_app import app
from flask_app.models.parent import Parent
from flask_app.models.chore import Chore
from flask_app.models.child import Child
from flask import render_template, request, session, redirect, get_flashed_messages, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/login/child")
def child_login():
    return render_template("c_login.html", messages = get_flashed_messages())

@app.route("/c_login", methods= ['POST'])
def c_login():
    child = Child.get_child_by_username({"username": request.form['username']})
    print(child)
    if child:
        session['username'] =  child.username
        return redirect("/c_dashboard")
    else:
        flash("Please login with a valid username and password!")
    return redirect("login/child")
    
@app.route("/c_dashboard")
def one_child():
    c = Child.get_child_with_chores(session['username'])
    print(c)
    if 'username' in session:
        return render_template("c_dashboard.html", cur_child = c)

@app.route("/c_logout")
def c_logout():
    session.pop('username')
    return redirect("/login/child")
