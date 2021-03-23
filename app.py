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
    #tarkistetaan oikeudet: PI voi muuttaa nimeä
    allow_pi = False
    if check_credentials.is_pi(db, session):
        allow_pi = True
    return render_template("index.html", name=name, introductory_text=introductory_text, \
                            allow_pi=allow_pi)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        #TODO: not user -> link to "/"
        pass
    else:
        #testing password w/o hashing
        #works!
        #if user[0] == password:
            #session["username"] = username
            #return redirect("/")
        if check_password_hash(user[0],password):
            session["username"] = username
            return redirect("/")
        else:
            #TODO: not password -> link to "/"
            pass
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/change_text", methods=["POST"])
def change_text():
    if "change_name" in request.form:
        allow_pi = check_credentials.is_pi(db, session)
        return render_template("change_text.html", allow_pi=allow_pi, form="change_name")
    elif "change_introduction" in request.form:
        allow_pi = check_credentials.is_pi(db, session)
        return render_template("change_text.html", allow_pi=allow_pi, form="change_introduction")

@app.route("/update", methods=["POST"])
def update():
    #TODO: credentials checking before updating
    if "changed_name" in request.form:
        new_title = request.form["changed_name"]
        sql = "UPDATE pages SET title=:new_title WHERE id=1"
        db.session.execute(sql, {"new_title":new_title})
        db.session.commit()
        return redirect("/")
    elif "changed_introduction" in request.form:
        new_introduction = request.form["changed_introduction"]
        sql = "UPDATE pages set introduction=:new_introduction WHERE id=1"
        db.session.execute(sql, {"new_introduction":new_introduction})
        db.session.commit()
        return redirect("/")
    elif "new_name" in request.form:
        new_name = request.form["new_name"]
        sql = "INSERT INTO pages (title) VALUES (:new_name)"
        db.session.execute(sql, {"new_name":new_name})
        db.session.commit()
        #TODO: redirect to newly created page instead of root
        return redirect("/")

@app.route("/new_page")
def new_page():
    #TODO: credentials checking before access
    #if personal page already exists, redirect there
    return render_template("new_page.html")