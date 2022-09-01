"""
A Sample Web-DB Application for DB-DESIGN lecture
Copyright (C) 2022 Yasuhiro Hayashi
"""
import os
import flaskdb.var as v

WTF_CSRF_SECRET_KEY = os.urandom(32)
SECRET_KEY = os.urandom(32)

SQLALCHEMY_DATABASE_URI = f"{v.DBTYPE}://{v.USERNAME}:{v.PASSWORD}@{v.HOSTNAME}:{v.PORT}/{v.DBNAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = v.SHOW_SQL
