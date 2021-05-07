from db import db
from flask import session

def __common_preliminaries():
    try:
        role = session["role"]
    except:
        return None
    return role

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

def check_topic_ownership(topic_id):
    if is_student():
        sql = "SELECT 1 FROM users U,topics T WHERE U.username=:username AND U.id=T.student_id AND T.id=:topic_id"
        result = db.session.execute(sql, {"username":session["username"], "topic_id":topic_id})
        return result.fetchone() != None
    elif is_member() or is_pi():
        sql = "SELECT 1 FROM users U,topics T WHERE U.username=:username AND U.id=T.responsible_user_id AND T.id=:topic_id"
        result = db.session.execute(sql, {"username":session["username"], "topic_id":topic_id})
        return result.fetchone() != None
    else: return False
    
def check_username(username):
    sql = "SELECT 1 FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone() != None

def csrf_check(form_csrf_token):
    return session["csrf_token"] == form_csrf_token

def is_pi():
    result = __common_preliminaries()
    return result == "pi"

def is_member():
    result = __common_preliminaries()
    return result == "member"

def is_student():
    result = __common_preliminaries()
    return result == "student"