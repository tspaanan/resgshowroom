from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

import check_credentials
import sql_quories

@app.route("/")
def index():
    name = sql_quories.fetch_title(db, 1)
    introductory_text = sql_quories.fetch_introduction(db, 1)
    
    #checking credentials: only PI can change everything, members can add their own personal pages
    allow_pi = check_credentials.is_pi(db, session)
    allow_member = check_credentials.is_member(db, session)

    #fetching keywords and publications
    keywords = sql_quories.fetch_keywords(db, 1)
    publications_all = sql_quories.fetch_publications(db, 1)
    #removing None-values from publications
    publications = strip_None_values(publications_all)
    #fetching links to all member pages
    subpages_id = sql_quories.fetch_member_pages(db)
    
    return render_template("index.html", name=name, introductory_text=introductory_text,
                            allow_pi=allow_pi, allow_member=allow_member, keywords=keywords,
                            publications=publications, subpages_id=subpages_id)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    #TODO: jos tässä asettaa esim. role-kenttään oikean roolin
    #sitä ei tarvitse hakea erikseen tietokannasta check_credentials-vaiheessa
    user_password = sql_quories.fetch_password(db, username)
    if user_password == None:
        return render_template("error.html", error="no_user")
    else:
        if check_password_hash(user_password[0],password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("error.html", error="wrong_password")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/change_text", methods=["POST"])
def change_text():
    allow_pi = check_credentials.is_pi(db, session)
    allow_member = check_credentials.is_member(db, session)
    page_id = request.form["page_id"]
    if "change_name" in request.form:
        return render_template("change_text.html", allow_pi=allow_pi, allow_member=allow_member, form="change_name", page_id=page_id)
    elif "change_introduction" in request.form:
        return render_template("change_text.html", allow_pi=allow_pi, allow_member=allow_member, form="change_introduction", page_id=page_id)

@app.route("/new_message", methods=["POST"])
def new_message():
    if "new_feedback" in request.form:
        content = request.form["new_feedback"]
        #page_id = request.form["page_id"] #prob. remove this line?
        if len(content) > 10000:
            return render_template("error.html", error="content too long")
        sql_quories.insert_message(db, 1, content)
    return redirect("/")

@app.route("/view_feedback", methods=["GET", "POST"]) #archive_message uudelleenohjaa tänne GET-metodilla
def view_feedback():
    allow_pi = check_credentials.is_pi(db, session)
    archived = "view_archived_feedback" in request.form
    if allow_pi:
        messages = sql_quories.fetch_feedback(db, archived)
        return render_template("feedback.html", allow_pi=allow_pi, messages=messages,
                                archived=archived)
    else: return render_template("error.html", error="insufficient credentials")

@app.route("/archive_message", methods=["POST"])
def archive_message():
    if check_credentials.is_pi(db, session):
        message_id = request.form["message_id"]
        sql_quories.archive_message(db, message_id)
        return redirect("/view_feedback")
    else: return render_template("error", error="insufficient credentials")

@app.route("/update", methods=["POST"])
def update():
    if "changed_name" in request.form:
        new_title = request.form["changed_name"]
        page_id = request.form["page_id"]
        if check_credentials.check_page_ownership(db, session, page_id):
            if len(new_title) > 200:
                return render_template("error.html", error="new_title too long")
            sql_quories.update_title(db, new_title, page_id)
            if page_id == "1": return redirect("/")
            else: return redirect("member_page/" + str(page_id))
        else: return render_template("error.html", error="insufficient credentials")
    elif "changed_introduction" in request.form:
        new_introduction = request.form["changed_introduction"]
        page_id = request.form["page_id"]
        if check_credentials.check_page_ownership(db, session, page_id):
            if len(new_introduction) > 10000:
                return render_template("error.html", error="new_introduction too long")
            sql_quories.update_introduction(db, new_introduction, page_id)
            if page_id == "1": return redirect("/")
            else: return redirect("member_page/" + str(page_id))
        else: return redirect("error.html", error="insufficient credentials")
    elif "new_name" in request.form:
        if check_credentials.is_pi(db, session) or check_credentials.is_member(db, session):
            #TODO: check that member is not creating a duplicate personal page
            new_name = request.form["new_name"]
            new_introduction = request.form["new_introduction"]
            if len(new_name) > 200 or len(new_introduction) > 10000:
                return render_template("error.html", error="new_name or new_introduction too long")
            sql_quories.insert_page(db, new_name, new_introduction)
            #after page creation: adding credentials for PI (and whoever just created the page)
            new_page_id = sql_quories.insert_credentials(db, session, new_name)
            return redirect("member_page/" + str(new_page_id))
        else: return redirect("error.html", error="insufficient credentials")

@app.route("/new_page")
def new_page():
    if check_credentials.is_member(db, session) and check_credentials.check_page_ownership(db, session, 0):
        return render_template("error.html", error="already has personal page")
        #TODO: if personal page already exists, redirect there
    if check_credentials.is_pi(db, session) or check_credentials.is_member(db, session):
        return render_template("new_page.html")
    else: return render_template("error.html", error="insufficient credentials")

@app.route("/member_page/<int:page_id>")
def member_page(page_id):
    name = sql_quories.fetch_title(db, page_id)
    introductory_text = sql_quories.fetch_introduction(db, page_id)
    keywords = sql_quories.fetch_keywords(db, page_id)
    publications_all = sql_quories.fetch_publications(db, page_id)
    publications = strip_None_values(publications_all)
    allow_pi = check_credentials.is_pi(db, session)
    allow_member = check_credentials.check_page_ownership(db, session, page_id)
    return render_template("member_page.html", name=name, introductory_text=introductory_text, \
                            allow_pi=allow_pi, allow_member=allow_member, page_id=page_id, \
                            keywords=keywords, publications=publications)

def strip_None_values(list_of_tuples):
    publications = []
    for tuple in list_of_tuples:
        tuple_replacement = []
        for data_field in tuple:
            if data_field: tuple_replacement.append(data_field)
        publications.append(tuple_replacement)
    return publications
