from flask_app import app
from flask_app.models.user import User
from flask_app.models.product import Product
from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/")
def dashboard():
    if "user_id" in session:
        data = {"id": session["user_id"]}
        loggeduser = User.get_user_by_id(data)
        return render_template("Home.html", loggeduser=loggeduser, allproducts=Product.get_all_Products())
    return render_template("Home.html",allproducts=Product.get_all_Products())


@app.route("/login", methods=["POST", "GET"])
def loginUser():
    if "user_id" in session:
        return redirect("/")
    if request.method == "GET":
        return render_template("login.html")
    user = User.get_user_by_email(request.form)
    if not user:
        flash("This user does not exist! Check your email.", "emailLogin")
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user["password"], request.form["password"]):
        # if we get False after checking the password
        flash("Invalid Password", "passwordLogin")
        return redirect(request.referrer)
    session["user_id"] = user["id"]
    return redirect("/")


@app.route("/register", methods=["POST", "GET"])
def register():
    if "user_id" in session:
        return redirect("/")
    if request.method == "GET":
        return render_template("register.html")
    if not User.validate_user(request.form):
        return redirect(request.referrer)
    user = User.get_user_by_email(request.form)
    if user:
        flash("This user already exists! Try another email.", "emailRegister")
        return redirect(request.referrer)

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    user_id = User.create(data)
    session["user_id"] = user_id
    return redirect("/")


@app.route("/admin/panel")
def admin():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)
    if loggeduser["role"] == "admin":
        return render_template(
            "adminPanel.html", loggeduser=loggeduser, allusers=User.get_all(), allproducts=Product.get_all_Products(), categories=Product.getCategories()
        )
        # return render_template(
        #     "adminPanel1.html", loggeduser=loggeduser, allusers=User.get_all(), allproducts=Product.get_all_Products(), categories=Product.getCategories()
        # )
    return redirect(request.referrer)


@app.route("/delete/user/<int:id>")
def delete(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    datad = {"id": id}
    loggeduser = User.get_user_by_id(data)
    if loggeduser["role"] == "admin" or loggeduser["id"] == id:
        User.delete_user(datad)
        flash("User Deleted.", "deleteUser")
        if loggeduser["id"] == id:
            session.clear()
            return redirect("/")
    return redirect("/all/users")


@app.route('/all/users/')
def userss():
    if "user_id" not in session:
        return redirect("/login")

    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)

    if loggeduser["role"] != "admin":
        return redirect("/")
    if loggeduser["role"] == "admin":
        return render_template('Users.html',users=User.get_all())

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
