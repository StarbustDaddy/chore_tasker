from flask_app import app
from flask_app.models.parent import Parent
from flask_app.models.child import Child
from flask_app.models.chore import Chore
from flask import render_template, request, session, redirect, get_flashed_messages, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("registration.html", messages = get_flashed_messages())

@app.route("/registration", methods = ["POST"])
def register_parent():
    if not Parent.validate_parent(request.form):
        return redirect("/")
    data = {
        "f_name": request.form["f_name"],
        "l_name": request.form["l_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"])
    }
    flash("You have completed registration.")
    return redirect("/")

@app.route("/login/parent")
def parent_login():
    return render_template("p_login.html", messages = get_flashed_messages())

@app.route("/p_login", methods = ['POST'])
def p_login():
    parent = Parent.get_parent_by_email({"email": request.form['email']})
    if parent:
        if bcrypt.check_password_hash(parent.password, request.form["password"]):
            session['user_id'] = parent.id
            return redirect("/p_dashboard")
    else:
        flash("Please login with a valid email and password!")
    return redirect("/")


@app.route("/p_dashboard")
def parent_dashboard():
    if 'user_id' in session:
        return render_template("p_dashboard.html", cur_parent = Parent.get_all_children_with_parent({"id": session['user_id']}), cur_chores = Parent.get_all_chores_with_parent({"id": session['user_id']}))

@app.route("/child/create", methods = ["POST"])
def save_child():
    data = {
        "f_name": request.form["f_name"],
        "l_name": request.form["l_name"],
        "username": request.form["username"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
        "parent_id": session["user_id"]
    }
    Child.save(data)
    print(data)
    return redirect("/p_dashboard")

@app.route("/child/new")
def add_child():
    return render_template("add_child.html" )

@app.route("/child/update", methods = ["POST"])
def update_child():
    change = {"id": request.form['id'],
        "f_name": request.form["f_name"],
        "l_name": request.form["l_name"],
        "username": request.form["username"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
        "parent_id": session["user_id"]
    }
    Child.edit(change)
    session['username'] = {"username": request.form["username"]}
    return redirect("/p_dashboard")

@app.route("/child/edit/<int:id>")
def child_edit(id):
    kid = Child.get_one({"id": id})
    print(kid)
    return render_template("edit_child.html", kid = kid)

@app.route("/child/delete/<int:id>")
def delete_child(id):
    Child.delete({"id": id})
    return redirect("/p_dashboard")

@app.route("/chore/new")
def add_chore():
    cur_parent = Parent.get_all_children_with_parent({"id": session['user_id']})
    return render_template("new_chore.html", kid = cur_parent)

@app.route("/chore/create", methods = ["POST"])
def save_chore():
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "point": request.form["point"],
        "day": request.form["day"],
        "child_id": 1,
        "parent_id": session["user_id"]
    }
    Chore.save(data)
    print(data)
    return redirect("/p_dashboard")

@app.route("/chore/update", methods = ["POST"])
def update_chore():
    change = {"id": request.form['id'],
            "name": request.form['name'],
            "description": request.form['description'],
            "point": request.form['point'],
            "day": request.form['day']}
    Chore.edit(change)
    return redirect("/p_dashboard")

@app.route("/chore/edit/<int:id>")
def chore_edit(id):
    cur_parent = Parent.get_all_children_with_parent({"id": session['user_id']})
    ch = Chore.get_one({"id": id})
    print(ch)
    return render_template("edit_chore.html", c = ch, kid = cur_parent, cur_child = Child.get_one({"id": id}))

@app.route("/chore/delete/<int:id>")
def delete_chore(id):
    Chore.delete({"id": id})
    return redirect("/p_dashboard")


@app.route("/logout")
def logout():
    session.clear
    return redirect("/login/parent")