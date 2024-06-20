from flask_app import app
from flask_app.models.user import User
from flask_app.models.product import Product
from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
import os
from datetime import datetime
from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS
# app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 5}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
from werkzeug.utils import secure_filename

bcrypt = Bcrypt(app)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/add/item", methods=["GET", "POST"])
def addItem():
    if "user_id" not in session:
        return redirect("/login")

    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)

    if loggeduser["role"] != "admin":
        return redirect("/")

    if request.method == "GET":
        return render_template("addItem.html", categories=Product.getCategories())

    if request.method == "POST":
        if not Product.validate_product(request.form):
            return redirect(request.referrer)

        if not request.files["image"]:
            flash("Show image is required!", "image")
            return redirect(request.referrer)

        image = request.files["image"]
        if not allowed_file(image.filename):
            flash("Image should be in png, jpg, jpeg format!", "image")
            return redirect(request.referrer)

        if image and allowed_file(image.filename):
            filename1 = secure_filename(image.filename)
            current_time = datetime.now().strftime("%d%m%Y%S%f")
            filename1 = current_time + filename1
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename1))

        data = {
            "product_name": request.form["product_name"],
            "description": request.form["description"],
            "price": request.form["price"],
            "stock_quantity": request.form["stock_quantity"],
            "image": filename1,
            "category_id": request.form["category_id"],
        }
        Product.create(data)
        return redirect("/all/products/")


@app.route("/update/item/<int:id>", methods=["GET", "POST"])
def UpdateItem(id):
    if "user_id" not in session:
        return redirect("/login")

    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)

    if loggeduser["role"] != "admin":
        return redirect("/")

    if request.method == "GET":
        data = {"product_id": id}
        product = Product.get_product_by_id(data)
        return render_template("UpdateItem.html", product=product)

    if request.method == "POST":
        # if not Product.validate_product(request.form):
        #     return redirect(request.referrer)

        # if not request.files["image"]:
        #     flash("Show image is required!", "image")
        #     return redirect(request.referrer)

        # image = request.files["image"]
        # if not allowed_file(image.filename):
        #     flash("Image should be in png, jpg, jpeg format!", "image")
        #     return redirect(request.referrer)

        # if image and allowed_file(image.filename):
        #     filename1 = secure_filename(image.filename)
        #     current_time = datetime.now().strftime("%d%m%Y%S%f")
        #     filename1 = current_time + filename1
        #     image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename1))
        data = {"product_id": id}
        product = Product.get_product_by_id(data)
        # current_image = product["image"]
        # image = request.files.get("image")
        # if image and allowed_file(image.filename):
        #     filename1 = secure_filename(image.filename)
        #     current_time = datetime.now().strftime("%d%m%Y%S%f")
        #     filename1 = current_time + filename1
        #     image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename1))
        # else:
        #     filename1 = current_image

        data = {
            "id":id,
            "description": request.form["description"],
            "price": request.form["price"],
            "stock_quantity": request.form["stock_quantity"]
            # "image": filename1,
        }
        Product.update_product(data)
        return redirect("/all/products/")


@app.route("/delete/item/<int:id>")
def deleteItem(id):
    if "user_id" not in session:
        return redirect("/login")

    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)

    if loggeduser["role"] != "admin":
        return redirect("/")
    if loggeduser["role"] == "admin":
        datad = {"product_id": id}
        Product.delete_product(datad)
        return redirect("/all/products/")

@app.route('/product/category/<int:id>')
def productbycat(id):
    data={
        "id":id
    }
    # products = Product.get_product_by_category(data)
    return render_template('ProductsbyCategory.html',products=Product.get_product_by_category(data))


@app.route('/all/products/')
def products():
    if "user_id" not in session:
        return redirect("/login")

    data = {"id": session["user_id"]}
    loggeduser = User.get_user_by_id(data)

    if loggeduser["role"] != "admin":
        return redirect("/")
    if loggeduser["role"] == "admin":
        return render_template('Products.html',products=Product.get_all_Products())