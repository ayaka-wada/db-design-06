#!/Users/ayaka/Development/ai-algo/.venv/bin/python3
"""
A Sample Web-DB Application for DB-DESIGN lecture
Copyright (C) 2022 Yasuhiro Hayashi
"""
from flask import Blueprint, request, session, render_template, redirect, flash, url_for
from sqlalchemy import between , and_, func, any_, case
import datetime
import pickle
import sys
from flaskdb import apps, db, da
from flaskdb.models import User, S_User, T_User, Classes, attend, qr_start, qr_stop,classes_date
from flaskdb.forms import LoginForm, AddItemForm, SearchItemForm, LoginForm2,QR_Form

app = Blueprint("app", __name__,static_folder='./static/image')

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("/index2.html")

@app.route("/initdb", methods=["GET", "POST"])
def initdb():
    db.drop_all()
    db.create_all()
    
    admin = User(username="admin", password="password")
    user = User(username="user", password="password")

    # 生徒のDB
    ayaka = S_User(username="2022040", password="password", management=[1,2,3])
    kanako = S_User(username="2022068", password="password", management=[2])
    ryosuke = S_User(username="2022035", password="password", management=[1,3])

    #先生のDB
    hayashi = T_User(username="hayashi", password="password")
    nakanishi = T_User(username="nakanishi", password="password")

    #授業のDB
    db_design = Classes(classname ="データベースデザイン", t_id =1, start_time = "09:00", end_time = "12:30",url ="index")
    mmkb = Classes(classname ="マルチメディア知識ベース", t_id =1, start_time = "08:50", end_time = "12:20",url ="index")
    ai_creation = Classes(classname ="専門コース演習II", t_id =2, start_time = "13:10", end_time = "16:40",url ="index")
    
    #授業の日付のDB
    db_1 =  classes_date(classes_id=1, classes_number=1,date="2022-09-19")
    db_2 =  classes_date(classes_id=1, classes_number=2,date="2022-09-20")
    db_3 =  classes_date(classes_id=1, classes_number=3,date="2022-09-21")
    
    #qrstart
    # a=qr_start(classes_id=1,qr_start_time="2022-09-19 05:55:35.171517",qr_start_date="2022-09-19")
    # b=qr_start(classes_id=1,qr_start_time="2022-09-19 05:57:35.171517",qr_start_date="2022-09-19")
    # c=qr_start(classes_id=1,qr_start_time="2022-09-20 05:55:35.171517",qr_start_date="2022-09-20")
    # d=qr_start(classes_id=1,qr_start_time="2022-09-20 05:57:35.171517",qr_start_date="2022-09-20")
    # e=qr_start(classes_id=1,qr_start_time="2022-09-20 06:57:35.171517",qr_start_date="2022-09-20")
    # f=qr_start(classes_id=1,qr_start_time="2022-09-21 06:57:35.171517",qr_start_date="2022-09-21")


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
    
    db.session.add(db_1)
    db.session.add(db_3)
    db.session.add(db_2)
    
    # db.session.add(a)
    # db.session.add(b)
    # db.session.add(c)
    # db.session.add(d)
    # db.session.add(e)
    # db.session.add(f)

    db.session.commit()
    return "initidb() method was executed. "

@app.route("/login_student", methods=["GET", "POST"])
def login_student():
    contents = request.args.get('id')

    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.password.data)

        user = S_User.query.filter_by(username=form.username.data, password=form.password.data).first()
        management = Classes.query.filter_by(classes_id=form.contents.data).first()

        if user is None or user.password != form.password.data:
            flash("Username or Password is incorrect.", "danger")
            return redirect(url_for("app.login_student"))

        session["username"] = user.username
        students = db.session.query(S_User.username).filter(
            S_User.management.any(form.contents.data)
        )

        session.permanent = True

        #もしs_usersのmanagementにmanagement.classes_idがあったら出席
        students_list=[]
        for i in students:
            students_list.append(i[0])
        if session["username"] in students_list:
            session["contents"] = management.classname
            attend_students = attend(students_id=session["username"], date_time=str(datetime.datetime.now()), classes_id=management.classes_id)

            db.session.add(attend_students)
            db.session.commit()
        else:
            flash("履修してないよん", "danger")
            return redirect(url_for("app.login_student"))

        return redirect(url_for("app.index2"))
    return render_template("login_student.html", form=form,contents=contents)

@app.route("/index2", methods=["GET", "POST"])
def index2():
    if not "username" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("app.login_student"))
    if not "contents" in session:
        flash("Log in is required.", "danger")
        return redirect(url_for("app.login_student"))

    return render_template("index2.html" ,contents=session["contents"])

@app.route("/login_teacher", methods=["GET", "POST"])
def login_teacher():
    form = LoginForm2()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.password.data)

        user = T_User.query.filter_by(username=form.username.data, password=form.password.data).first()

        if user is None or user.password != form.password.data:
            flash("Username or Password is incorrect.", "danger")
            return redirect(url_for("app.login_teacher"))

        session["username"] = user.username
        session["t_id"] = user.t_id
        all_staffs = db.session.query(T_User).all()
        count = db.session.query(func.count(T_User.t_id)).first()[0]
        # print("ここここここここここ",all_staffs)
        # print("ここここここここここ",count)
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
    teacher = classes_list.t_id
    classes_list = Classes.query.filter_by(t_id= teacher)
    
    return render_template("classes.html", classes_list=classes_list)

@app.route('/management',methods=['GET', 'POST'])
def get_request():
    global jackson, mikel
    jackson=0
    mikel=0
    contents = request.args.get('id')
    
    management_list = Classes.query.filter_by(classes_id=contents).first()
    
    students = db.session.query(S_User.username).filter(
        S_User.management.any(contents)
    )
    
    count_time = db.session.query(
        func.count(qr_start.classes_id==contents)
        ).first()[0]
    
    if count_time > 0:

        count_qr = db.session.query(
            func.count(qr_start.classes_id == contents)
            ).all()[0]

        check = db.session.query(
                qr_start.id,
                qr_start.classes_id,
                attend.students_id,
                attend.date_time,
                qr_start.qr_start_time,
                qr_stop.qr_end_time,
                qr_start.qr_start_date
            ).filter(
                qr_start.classes_id == attend.classes_id,
                qr_start.id == qr_stop.id,
                between(attend.date_time, qr_start.qr_start_time, qr_stop.qr_end_time)
            ).all()

        mikel = db.session.query(
                attend.students_id,
                qr_start.qr_start_date,
                func.count(qr_start.qr_start_date)
            ).filter(
                qr_start.classes_id == attend.classes_id,
                qr_start.id == qr_stop.id,
                between(attend.date_time, qr_start.qr_start_time, qr_stop.qr_end_time),
                qr_start.classes_id == contents
            ).group_by(attend.students_id,qr_start.qr_start_date).all()

        # qrコード押した回数知りたい
        jackson = db.session.query(
                classes_date.date,
                func.count(classes_date.date)
            ).filter(
                qr_start.classes_id == contents,
                classes_date.classes_id == contents,
                qr_start.qr_start_date == classes_date.date
            ).group_by(classes_date.date).all()

        class_count = db.session.query(
                classes_date.date
            ).order_by(classes_date.classes_number)
            
    else:
        count_qr = 0
    
    sky = []
    for p in range(len(mikel)):
        sky.append([mikel[p][0], mikel[p][1],mikel[p][2]])
    # print("sssssssss", sky)
    # print("jjjjjj", jackson)
    # print("cccccc", class_count)
    # print("mmmmmmmm", mikel)
    # print("student", students)

    marubatu_list = []
    for s in students:
        marubatu_list_one = []
        marubatu_list_one.append(s[0])
        for h in range(7):
            if (class_count.count() -1) >= h:
                list = [i for i, l in enumerate(sky) if set([int(s[0]), class_count[h][0]]).issubset(l)]
                # print("lllllllll", list)
                # print("lllllllll", int(s[0]))
                # print("lllllllll", class_count[h][0])
                if not list:
                    marubatu_list_one.append("×")
                elif jackson[h][1] == sky[list[0]][2]:
                    marubatu_list_one.append("○")
                elif jackson[h][1] > sky[list[0]][2]:
                    marubatu_list_one.append("△")
            else:
                marubatu_list_one.append("×")

                
        marubatu_list.append(marubatu_list_one)
        
    # print("mmmmmmmmmmmmmmmmm", marubatu_list)
    # print("mmmmmmmmmmmmmmmmm", mikel)
    # print("mmmmmmmmmmmmmmmmm", sky)
    
    return render_template("management.html", management_list=management_list, students=students, contents=contents, count_qr=count_qr,mikel=mikel,jackson=jackson,class_count=class_count,marubatu_list=marubatu_list)

@app.route('/QR_start',methods=['GET', 'POST'])
def qr_start_():
    contents = request.args.get('id')
    now = datetime.datetime.now()
    start = str(now)
    start_date = str(now.date())
    print(start_date)
    qr_start_time = qr_start(classes_id=contents, qr_start_time=start,qr_start_date=start_date)
    db.session.add(qr_start_time)
    db.session.commit()
    
    return render_template("QR_start.html", contents=contents)

@app.route('/QR_stop',methods=['GET', 'POST'])
def qr_stop_():
    contents = request.args.get('id')
    stop = str(datetime.datetime.now())
    qr_stop_time = qr_stop(classes_id=contents, qr_end_time=stop)
    db.session.add(qr_stop_time)
    db.session.commit()

    return render_template("QR_stop.html", contents=contents)
