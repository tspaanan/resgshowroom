from app import app
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

import os
import re

from db import db
import check_credentials
import sql_quories

#@app.route("/img_test")
#def img_test():
    #return sql_quories.fetch_images(db)
#toimii, mutta miten tämän saa sivun osaksi?

@app.route("/")
def index():
    name = sql_quories.fetch_title(1)
    introductory_text = sql_quories.fetch_introduction(1)
    
    #checking credentials: only PI can change everything, members can add their own personal pages
    allow_pi = check_credentials.is_pi()
    allow_member = check_credentials.is_member()
    allow_student = check_credentials.is_student()

    #fetching keywords and publications
    keywords = sql_quories.fetch_keywords(1)
    publications_all = sql_quories.fetch_publications(1)
    #removing None-values from publications
    publications = strip_None_values(publications_all)
    #fetching links to all member pages and member names
    member_pages = sql_quories.fetch_member_pages()
    #fetching images
    images = sql_quories.fetch_images()
    
    return render_template("index.html", name=name, introductory_text=introductory_text,
                            allow_pi=allow_pi, allow_member=allow_member, allow_student=allow_student,
                            keywords=keywords, publications=publications, member_pages=member_pages, images=images)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user_password = sql_quories.fetch_password(username)
    user_role = sql_quories.fetch_role(username)[0] #TODO: actually use this value stored in session below
    if user_password == None:
        return render_template("error.html", error="no_user")
    else:
        if check_password_hash(user_password[0],password):
            session["username"] = username
            session["role"] = user_role
            session["csrf_token"] = os.urandom(16).hex()
            return redirect("/")
        else:
            return render_template("error.html", error="wrong_password")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        #TODO: check that only students can register student accounts (extra password just for registering a student account, given by PI?)
        new_password = request.form["new_password"]
        repeat_password = request.form["repeat_password"]
        if new_password != repeat_password:
            return render_template("error.html", error="repeat_password does not match")
        if new_password == "":
            return render_template("error.html", error="no password set")
        new_username = request.form["new_username"]
        #regular expressions were hard to write into a single expression, so three different checks for password validity
        if re.search('[0-9]+', new_password) == None:
            return render_template("error.html", error="password has to contain at least one digit")
        if re.search('[a-z]+', new_password) == None:
            return render_template("error.html", error="password has to contain at least one lowercase letter")
        if re.search('[A-Z]+', new_password) == None:
            return render_template("error.html", error="password has to contain at least one uppercase letter")
        if new_username == "":
            return render_template("error.html", error="no username set")
        if check_credentials.check_username(new_username):
            return render_template("error.html", error="username exists already")
        hashed_password = generate_password_hash(new_password)
        sql_quories.insert_user(new_username, hashed_password, "student")
        session["username"] = new_username
        return redirect("/")

@app.route("/change_text", methods=["POST"])
def change_text():
    if not check_credentials.csrf_check(request.form["csrf_token"]):
        return render_template("error.html", error="detected csrf_vulnerability exploitation attempt")
    allow_pi = check_credentials.is_pi()
    allow_member = check_credentials.is_member()
    page_id = request.form["page_id"]
    old_text = request.form["old_text"]
    if "change_name" in request.form:
        return render_template("change_text.html", allow_pi=allow_pi, allow_member=allow_member, form="change_name", page_id=page_id, old_text=old_text)
    elif "change_introduction" in request.form:
        return render_template("change_text.html", allow_pi=allow_pi, allow_member=allow_member, form="change_introduction", page_id=page_id, old_text=old_text)

@app.route("/new_message", methods=["POST"])
def new_message():
    if "new_feedback" in request.form:
        content = request.form["new_feedback"]
        if len(content) > 10000:
            return render_template("error.html", error="content too long")
        sql_quories.insert_message(1, content)
    return redirect("/")

@app.route("/view_feedback", methods=["GET", "POST"]) #archive_message uudelleenohjaa tänne GET-metodilla
def view_feedback():
    #TODO: fix this for redirection with GET-method
    #if not check_credentials.csrf_check(request.form["csrf_token"]):
        #return render_template("error.html", error="detected csrf_vulnerability exploitation attempt")
    allow_pi = check_credentials.is_pi()
    archived = "view_archived_feedback" in request.form
    if allow_pi:
        messages = sql_quories.fetch_feedback(archived)
        return render_template("feedback.html", allow_pi=allow_pi, messages=messages,
                                archived=archived)
    else: return render_template("error.html", error="insufficient credentials")

@app.route("/archive_message", methods=["POST"])
def archive_message():
    if not check_credentials.csrf_check(request.form["csrf_token"]):
        return render_template("error.html", error="detected csrf_vulnerability exploitation attempt")
    if check_credentials.is_pi():
        message_id = request.form["message_id"]
        sql_quories.archive_message(message_id)
        return redirect("/view_feedback")
    else: return render_template("error", error="insufficient credentials")

@app.route("/update", methods=["POST"])
def update():
    if not check_credentials.csrf_check(request.form["csrf_token"]):
        return render_template("error.html", error="detected csrf_vulnerability exploitation attempt")
    if "changed_name" in request.form:
        new_title = request.form["changed_name"]
        page_id = request.form["page_id"]
        if check_credentials.check_page_ownership(page_id):
            if len(new_title) > 200:
                return render_template("error.html", error="new_title too long")
            sql_quories.update_title(new_title, page_id)
            if page_id == "1": return redirect("/")
            else: return redirect("member_page/" + str(page_id))
        else: return render_template("error.html", error="insufficient credentials")
    elif "changed_introduction" in request.form:
        new_introduction = request.form["changed_introduction"]
        page_id = request.form["page_id"]
        if check_credentials.check_page_ownership(page_id):
            if len(new_introduction) > 10000:
                return render_template("error.html", error="new_introduction too long")
            sql_quories.update_introduction(new_introduction, page_id)
            if page_id == "1": return redirect("/")
            else: return redirect("member_page/" + str(page_id))
        else: return render_template("error.html", error="insufficient credentials")
    elif "new_name" in request.form:
        if check_credentials.is_pi() or check_credentials.is_member():
            #TODO: check that member is not creating a duplicate personal page
            new_name = request.form["new_name"]
            new_introduction = request.form["new_introduction"]
            if len(new_name) > 200 or len(new_introduction) > 10000:
                return render_template("error.html", error="new_name or new_introduction too long")
            sql_quories.insert_page(new_name, new_introduction)
            #after page creation: adding credentials for PI (and whoever just created the page)
            new_page_id = sql_quories.insert_credentials(session, new_name)
            return redirect("member_page/" + str(new_page_id))
        else: return render_template("error.html", error="insufficient credentials")

@app.route("/new_page", methods=["POST"])
def new_page():
    if not check_credentials.csrf_check(request.form["csrf_token"]):
        return render_template("error.html", error="detected csrf_vulnerability exploitation attempt")
    if check_credentials.is_member() and check_credentials.check_page_ownership(0):
        return render_template("error.html", error="already has personal page")
        #TODO: if personal page already exists, redirect there
        #TODO: once role is save into session, add extra security here against unauthorized /new_page requests
    if check_credentials.is_pi() or check_credentials.is_member():
        return render_template("new_page.html")
    else: return render_template("error.html", error="insufficient credentials")

@app.route("/member_page/<int:page_id>")
def member_page(page_id):
    name = sql_quories.fetch_title(page_id)
    introductory_text = sql_quories.fetch_introduction(page_id)
    keywords = sql_quories.fetch_keywords(page_id)
    publications_all = sql_quories.fetch_publications(page_id)
    publications = strip_None_values(publications_all)
    allow_pi = check_credentials.is_pi()
    allow_member = check_credentials.check_page_ownership(page_id)
    return render_template("member_page.html", name=name, introductory_text=introductory_text, \
                            allow_pi=allow_pi, allow_member=allow_member, page_id=page_id, \
                            keywords=keywords, publications=publications)

@app.route("/student_topics")
def student_topics():
    allow_pi = check_credentials.is_pi()
    allow_member = check_credentials.is_member()
    allow_student = check_credentials.is_student()
    topics = sql_quories.fetch_topics()
    return render_template("student_topics.html", allow_pi=allow_pi,
                    allow_member=allow_member, allow_student=allow_student, topics=topics)

def strip_None_values(list_of_tuples):
    publications = []
    for tuple in list_of_tuples:
        tuple_replacement = []
        for data_field in tuple:
            if data_field: tuple_replacement.append(data_field)
        publications.append(tuple_replacement)
    return publications