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

@app.route("/")
def index():
    result = db.session.execute("SELECT title FROM pages WHERE id=1")
    name = result.fetchone()[0]
    result = db.session.execute("SELECT introduction FROM pages WHERE id=1")
    introductory_text = result.fetchone()[0]
    #tarkistetaan oikeudet: PI voi muuttaa nimeä
    #if is_pi():
        #print("is pi")
    return render_template("index.html", name=name, introductory_text=introductory_text)

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