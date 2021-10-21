from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

def login(username, password):
    sql = "SELECT username, password, admin, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["username"]=user[0]
            session["userrole"]=user[2]
            session["user_id"]=user[3]
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False

def user_id():
    return session.get("user_id",0)


def logout():
    del session["user_id"]

def register(username, password, admin):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password, admin) VALUES (:username,:password, :admin)"
        db.session.execute(sql, {"username":username, "password":hash_value, "admin":admin})
        db.session.commit()
    except Exception as error:
        print(error)
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def get_username(id):
    try:
        sql = "SELECT username FROM users WHERE id=:id"
        result = db.session.execute(sql, {"id":id})
        name = result.fetchone()[0]
        return name
    except Exception as error:
        print(error)
        return False

def is_admin():
    sql = "SELECT admin FROM users WHERE id=:session_id"
    result = db.session.execute(sql, {"session_id":user_id()})
    return result.fetchone()