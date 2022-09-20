"""
A Sample Web-DB Application for DB-DESIGN lecture
Copyright (C) 2022 Yasuhiro Hayashi
"""
from flaskdb import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.id

class S_User(db.Model):
    __tablename__ = "s_users"
    s_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    management = db.Column(db.ARRAY(db.Integer))

    def __repr__(self):
        return "<S_User %r>" % self.s_id

class T_User(db.Model):
    __tablename__ = "t_users"
    t_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return "<T_User %r>" % self.t_id

class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    itemname = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return "<Item %r>" % self.id

class Classes(db.Model):
    __tablename__ = "classes"
    classes_id = db.Column(db.Integer, primary_key=True)
    classname = db.Column(db.String(128), nullable=False)
    t_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    url = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return "<Classes %r>" % self.classes_id

class qr_start(db.Model):
    __tablename__ = "qr_start"
    id = db.Column(db.Integer, primary_key=True)
    classes_id = db.Column(db.Integer, nullable=False)
    qr_start_time = db.Column(db.String(64), nullable=False)
    qr_start_date = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return "<qr_start %r>" % self.id

class qr_stop(db.Model):
    __tablename__ = "qr_stop"
    id = db.Column(db.Integer, primary_key=True)
    classes_id = db.Column(db.Integer, nullable=False)
    qr_end_time = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return "<qr_stop %r>" % self.id

class attend(db.Model):
    __tablename__ = "attend"
    id = db.Column(db.Integer, primary_key=True)
    students_id = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.String(64), nullable=False)
    classes_id = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return "<attend %r>" % self.id

class classes_date(db.Model):
    __tablename__ = "classes_date"
    id = db.Column(db.Integer, primary_key=True)
    classes_id = db.Column(db.Integer, nullable=False)
    classes_number = db.Column(db.Integer, nullable=False)
    date =  db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        return "<classes_date %r>" % self.id



