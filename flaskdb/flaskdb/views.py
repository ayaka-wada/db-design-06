"""
A Sample Web-DB Application for DB-DESIGN lecture
Copyright (C) 2022 Yasuhiro Hayashi
"""
from flask import Blueprint, request, session, render_template, redirect, flash, url_for
import datetime
import pickle

from flaskdb import apps, db, da
from flaskdb.models import User, Item, S_User, T_User, Classes
from flaskdb.forms import LoginForm, AddItemForm, SearchItemForm

app = Blueprint("app", __name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("/index.html")

@app.route("/now", methods=["GET", "POST"])
def now():
    return str(datetime.datetime.now())

# This is a very danger method
@app.route("/receive", methods=["GET", "POST"])
def receive():
    if request.method == "GET":
        username = request.args.get("username")
        password = request.args.get("password")
    else:
        username = request.form["username"]
        password = request.form["password"]

    return render_template("receive.html", username=username, password=password)

@app.route("/initdb", methods=["GET", "POST"])
def initdb():
    db.drop_all()
    db.create_all()
    
    admin = User(username="admin", password="password")
    user = User(username="user", password="password")

    # 生徒のDB
    ayaka = S_User(username="2022040", password="password")
    kanako = S_User(username="2022068", password="password")
    ryosuke = S_User(username="2022035", password="password")

    #先生のDB
    hayashi = T_User(username="hayashi", password="password")
    nakanishi = T_User(username="nakanishi", password="password")

    #授業のDB
    db_design = Classes(classname ="データベースデザイン", t_id =1, start_time = "09:00", end_time = "12:30",url ="index")
    mmkb = Classes(classname ="マルチメディア知識ベース", t_id =1, start_time = "08:50", end_time = "12:20",url ="index")
    ai_creation = Classes(classname ="専門コース演習II", t_id =2, start_time = "13:10", end_time = "16:40",url ="index")



    db.session.add(admin)
    db.session.add(user)

    db.session.add(ayaka)
    db.session.add(kanako)
    db.session.add(ryosuke)

    db.session.add(hayashi)
    db.session.add(nakanishi)

    db.session.add(db_design)
    db.session.add(ai_creation)
    db.session.add(mmkb)

    db.session.commit()
    return "initidb() method was executed. "

@app.route("/login_student", methods=["GET", "POST"])
def login_student():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.password.data)

        user = S_User.query.filter_by(username=form.username.data, password=form.password.data).first()

        if user is None or user.password != form.password.data:
            flash("Username or Password is incorrect.", "danger")
            return redirect(url_for("app.login_student"))

        session["username"] = user.username
        return redirect(url_for("app.index"))

    return render_template("login_student.html", form=form)

@app.route("/login_teacher", methods=["GET", "POST"])
def login_teacher():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.password.data)

        user = T_User.query.filter_by(username=form.username.data, password=form.password.data).first()

        if user is None or user.password != form.password.data:
            flash("Username or Password is incorrect.", "danger")
            return redirect(url_for("app.login_teacher"))

        session["username"] = user.username
        session["t_id"] = user.t_id
        return redirect(url_for("app.classes"))

    return render_template("login_teacher.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("app.index"))

@app.route("/classes", methods=["GET", "POST"])
def classes():
    if not "username" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("app.login_teacher"))

    classes_list = T_User.query.filter_by(username=session["username"]).first()
    teacher =  classes_list.t_id
    classes_list = Classes.query.filter_by(t_id= teacher)

    return render_template("classes.html", classes_list=classes_list)

@app.route("/additem", methods=["GET", "POST"])
def additem():
    if not "username" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("app.login"))

    form = AddItemForm()

    if form.validate_on_submit():
        item = Item()
        form.copy_to(item)
        user = User.query.filter_by(username=session["username"]).first()
        item.user_id = user.id
        db.session.add(item)
        db.session.commit()

        flash("An item was added.", "info")
        return redirect(url_for("app.additem"))

    itemlist = Item.query.all()
    return render_template("additem.html", form=form, itemlist=itemlist)

@app.route("/searchitem", methods=["GET", "POST"])
def searchitem():
    if not "username" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("app.login_teacher"))

    form = SearchItemForm()

    if form.validate_on_submit():
        itemlist = Item.query.filter(Item.itemname.like("%" + form.itemname.data + "%")).all()        
        return render_template("search.html", form=form, itemlist=itemlist)

        # For change to PRG
        # itemlist = pickle.dumps(itemlist)
        # session["itemlist"] = itemlist
        # return redirect(url_for("app.searchitem"))

    # if "itemlist" in session:
    #     itemlist = session["itemlist"]
    #     itemlist = pickle.loads(itemlist)
    #     session.pop("itemlist", None)
    # else:
    #     itemlist = None
    # 
    # return render_template("search.html", form=form, itemlist=itemlist)

    return render_template("search.html", form=form)

@app.route("/nativesql", methods=["GET", "POST"])
def nativesql():
    if not "username" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("app.login"))

    form = AddItemForm()

    if form.validate_on_submit():
        item = Item()
        form.copy_to(item)
        user = User.query.filter_by(username=session["username"]).first()
        item.user_id = user.id
        da.add_item(item)

        flash("An item was added.", "info")
        return redirect(url_for("app.additem"))

    itemlist = da.search_items()
    return render_template("additem.html", form=form, itemlist=itemlist)
