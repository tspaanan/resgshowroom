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

@app.route("/")
def index():
    result = db.session.execute("SELECT title FROM pages WHERE id=1")
    name = result.fetchone()[0]
    result = db.session.execute("SELECT introduction FROM pages WHERE id=1")
    introductory_text = result.fetchone()[0]
    
    #checking credentials: only PI can change everything, members can add their own personal pages
    allow_pi = check_credentials.is_pi(db, session)
    allow_member = check_credentials.is_member(db, session)

    #fetching links to all the member pages
    result = db.session.execute("SELECT id FROM pages WHERE id>2")
    subpages_id = result.fetchall()
    
    return render_template("index.html", name=name, introductory_text=introductory_text,
                            allow_pi=allow_pi, allow_member=allow_member, subpages_id=subpages_id)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    #TODO: jos tässä asettaa esim. role-kenttään oikean roolin
    #sitä ei tarvitse hakea erikseen tietokannasta check_credentials-vaiheessa
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user_password = result.fetchone()
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
        sql = "INSERT INTO messages (message,time,archived,page_id) VALUES" \
            "(:content,NOW(),FALSE,1)"
        db.session.execute(sql, {"content":content})
        db.session.commit()
    return redirect("/")

@app.route("/view_feedback", methods=["GET", "POST"]) #archive_message uudelleenohjaa tänne GET-metodilla
def view_feedback():
    allow_pi = check_credentials.is_pi(db, session)
    archived = "view_archived_feedback" in request.form
    if allow_pi:
        sql = "SELECT id,message,time FROM messages WHERE archived=:archived"
        result = db.session.execute(sql, {"archived":archived})
        messages = result.fetchall()
        return render_template("feedback.html", allow_pi=allow_pi, messages=messages,
                                archived=archived)
    else: return render_template("error.html", error="insufficient credentials")

@app.route("/archive_message", methods=["POST"])
def archive_message():
    if check_credentials.is_pi(db, session):
        message_id = request.form["message_id"]
        sql = "UPDATE messages SET archived=TRUE WHERE id=:message_id"
        db.session.execute(sql, {"message_id":message_id})
        db.session.commit()
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
            sql = "UPDATE pages SET title=:new_title WHERE id=:page_id"
            db.session.execute(sql, {"new_title":new_title, "page_id":page_id})
            db.session.commit()
            if page_id == "1": return redirect("/")
            else: return redirect("member_page/" + str(page_id))
        else: return render_template("error.html", error="insufficient credentials")
    elif "changed_introduction" in request.form:
        new_introduction = request.form["changed_introduction"]
        page_id = request.form["page_id"]
        if check_credentials.check_page_ownership(db, session, page_id):
            if len(new_introduction) > 10000:
                return render_template("error.html", error="new_introduction too long")
            sql = "UPDATE pages SET introduction=:new_introduction WHERE id=:page_id"
            db.session.execute(sql, {"new_introduction":new_introduction, "page_id":page_id})
            db.session.commit()
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
            sql = "INSERT INTO pages (title,introduction) VALUES (:new_name,:new_introduction)"
            db.session.execute(sql, {"new_name":new_name, "new_introduction":new_introduction})
            db.session.commit()
            
            #after page creation: adding credentials for PI (and whoever just created the page)
            username = session["username"]
            result = db.session.execute("SELECT id FROM users WHERE username=:username", {"username":username})
            new_user_id = result.fetchone()[0]
            result = db.session.execute("SELECT id FROM pages WHERE title=:new_name", {"new_name":new_name})
            new_page_id = result.fetchone()[0]
            sql = "INSERT INTO page_ownership (user_id,page_id) VALUES (:new_user_id,:new_page_id)"
            db.session.execute(sql, {"new_user_id":new_user_id, "new_page_id":new_page_id})
            db.session.commit()
            if new_user_id != 1:
                db.session.execute(sql, {"new_user_id":"1", "new_page_id":new_page_id})
                db.session.commit()
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
    sql = "SELECT title FROM pages WHERE id=:page_id"
    result = db.session.execute(sql, {"page_id":page_id})
    name = result.fetchone()[0]
    sql = "SELECT introduction FROM pages WHERE id=:page_id"
    result = db.session.execute(sql, {"page_id":page_id})
    introductory_text = result.fetchone()[0]
    
    #checking credentials: PI can change everything, members only their own page
    allow_pi = check_credentials.is_pi(db, session)
    allow_member = check_credentials.check_page_ownership(db, session, page_id)
    return render_template("member_page.html", name=name, introductory_text=introductory_text, \
                            allow_pi=allow_pi, allow_member=allow_member, page_id=page_id)