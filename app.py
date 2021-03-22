from flask import Flask
from flask import render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

from werkzeug.utils import redirect

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute("SELECT title FROM pages WHERE id=1")
    name = result.fetchone()[0]
    result = db.session.execute("SELECT introduction FROM pages WHERE id=1")
    introductory_text = result.fetchone()[0]
    return render_template("index.html", name=name, introductory_text=introductory_text)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    #MISSING: username & password check
    session["username"] = username
    return redirect("/")