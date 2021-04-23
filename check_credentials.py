from db import db
from flask import session

def is_pi():
    result = common_preliminaries()
    if result == None: return False
    return result.fetchone()[0] == "pi"

def is_member():
    result = common_preliminaries()
    if result == None: return False
    return result.fetchone()[0] == "member"

def is_student():
    result = common_preliminaries()
    if result == None: return False
    return result.fetchone()[0] == "student"

def common_preliminaries():
    try:
        username = session["username"]
    except:
        return None
        #TODO: jos yllä palauttaisi False niin olisi elegantimpaa?
    sql = "SELECT role FROM users WHERE username=:username"
    return db.session.execute(sql, {"username":username})

def check_page_ownership(page_id):
    try:
        username = session["username"]
    except:
        return False
    if page_id == 0: #check if username has page ownership of any pages
        sql = "SELECT 1 FROM users U,page_ownership P WHERE U.username=:username AND U.id=P.user_id"
        result = db.session.execute(sql, {"username":username})
    else: #otherwise check if username has page ownership of a particular page
        sql = "SELECT 1 FROM users U,page_ownership P WHERE U.username=:username AND U.id=P.user_id AND P.page_id=:page_id"
        result = db.session.execute(sql, {"username":username, "page_id":page_id})
    return result.fetchone() != None

def check_username(username):
    sql = "SELECT 1 FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone() != None

def csrf_check(form_csrf_token):
    return session["csrf_token"] == form_csrf_token