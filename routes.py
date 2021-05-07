from app import app
from flask import make_response, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

import base64
import os
import re

import check_credentials
import sql_quories

def __strip_None_values(list_of_tuples):
    publications = []
    for tuple in list_of_tuples:
        tuple_replacement = []
        for data_field in tuple:
            if data_field: tuple_replacement.append(data_field)
        publications.append(tuple_replacement)
    return publications

@app.route("/")
def index():
    name = sql_quories.fetch_title(1)
    introductory_text = sql_quories.fetch_introduction(1)
    
    #checking credentials: only PI can change everything, members can add and modify their own personal pages
    allow_pi = check_credentials.is_pi()
    allow_member = check_credentials.is_member()
    allow_student = check_credentials.is_student()

    keywords = sql_quories.fetch_keywords(1)
    publications_all = sql_quories.fetch_publications(1)
    publications = __strip_None_values(publications_all) #removing None-values from publications for easy displaying
    member_pages = sql_quories.fetch_member_pages()
    images = sql_quories.fetch_images()

    # circumventing the design conflict between redirecting to "/" after user leaves feedback and wanting to work with Boostrap wo/ Javascript
    feedback_left = False
    if "feedback_left" in session:
        feedback_left = session["feedback_left"]
        session["feedback_left"] = False
    
    return render_template("index.html", name=name, introductory_text=introductory_text,
                            allow_pi=allow_pi, allow_member=allow_member, allow_student=allow_student,
                            keywords=keywords, publications=publications, member_pages=member_pages, images=images,
                            feedback_left=feedback_left)

@app.route("/archive_message", methods=["POST"])
def archive_message():
    if not check_credentials.csrf_check(request.form["csrf_token"]):
        return render_template("error.html", error="detected csrf_vulnerability exploitation attempt")
    if check_credentials.is_pi():
        message_id = request.form["message_id"]
        sql_quories.archive_message(message_id)
        return redirect("/view_feedback")
    else: return render_template("error", error="insufficient credentials")

@app.route("/change_text", methods=["POST"])
def change_text():
    if not check_credentials.csrf_check(request.form["csrf_token"]):
        return render_template("error.html", error="detected csrf_vulnerability exploitation attempt")
    allow_pi = check_credentials.is_pi()
    allow_member = check_credentials.is_member()
    page_id = request.form["page_id"]
    if "old_text" in request.form:
        old_text = request.form["old_text"]
    if "change_name" in request.form:
        return render_template("change_text.html", allow_pi=allow_pi, allow_member=allow_member, form="change_name", page_id=page_id, old_text=old_text)
    elif "change_introduction" in request.form:
        return render_template("change_text.html", allow_pi=allow_pi, allow_member=allow_member, form="change_introduction", page_id=page_id, old_text=old_text)
    elif "add_new_keyword" in request.form:
        return render_template("change_text.html", allow_pi=allow_pi, allow_member=allow_member, form="add_new_keyword", page_id=page_id)
    elif "add_new_publication" in request.form:
        return render_template("change_text.html", allow_pi=allow_pi, allow_member=allow_member, form="add_new_publication", page_id=page_id)

@app.route("/delete_logo", methods=["POST"])
def delete_logo():
    if not check_credentials.csrf_check(request.form["csrf_token"]):
        return render_template("error.html", error="detected csrf_vulnerability exploitation attempt")
    if not check_credentials.check_page_ownership(1):
        return render_template("error.html", error="insufficient credentials")
    allow_pi = check_credentials.is_pi()
    logo_ids = sql_quories.fetch_image_ids()
    logos = sql_quories.fetch_images()
    combined_logo_info = zip(logo_ids, logos)
    return render_template("delete_text.html", allow_pi=allow_pi, form="delete_logo", combined_logo_info=combined_logo_info)

@app.route("/delete_text", methods=["POST"])
def delete_text():
    if not check_credentials.csrf_check(request.form["csrf_token"]):
        return render_template("error.html", error="detected csrf_vulnerability exploitation attempt")
    page_id = request.form["page_id"]
    if not check_credentials.check_page_ownership(page_id):
        return render_template("error.html", error="insufficient credentials")
    allow_pi = check_credentials.is_pi()
    allow_member = check_credentials.is_member()
    if "delete_publication" in request.form:
        publications_all = sql_quories.fetch_publications(page_id)
        publications = __strip_None_values(publications_all)
        return render_template("delete_text.html", publications=publications, allow_pi=allow_pi, allow_member=allow_member,
                                form="delete_publication", page_id=page_id)
    elif "delete_keyword" in request.form:
        keywords = sql_quories.fetch_keywords(page_id)
        return render_template("delete_text.html", keywords=keywords, allow_pi=allow_pi, allow_member=allow_member,
                                form="delete_keyword", page_id=page_id)

@app.route("/download", methods=["POST"])
def download():
    if not check_credentials.csrf_check(request.form["csrf_token"]):
        return render_template("error.html", error="detected csrf_vulnerability exploitation attempt")
    topic_id = request.form["topic_id"]
    if check_credentials.check_topic_ownership(topic_id):
        document_id = request.form["document_id"]
        fetched_document = sql_quories.fetch_document(document_id)
        response = make_response(bytes(fetched_document[0][1]))
        response.headers.set("Content-Type","application/msword")
        response.headers.set("Content-Disposition","attachment; filename=" + fetched_document[0][0])
        return response
    else: return render_template("error.html", error="insufficient credentials")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user_password = sql_quories.fetch_password(username)
    if user_password == None:
        return render_template("error.html", error="no_user")
    else:
        if check_password_hash(user_password[0],password):
            session["username"] = username
            session["role"] = sql_quories.fetch_role(username)[0]
            session["csrf_token"] = os.urandom(16).hex()
            return redirect("/")
        else:
            return render_template("error.html", error="wrong_password")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/member_page/<int:page_id>")
def member_page(page_id):
    name = sql_quories.fetch_title(page_id)
    introductory_text = sql_quories.fetch_introduction(page_id)
    keywords = sql_quories.fetch_keywords(page_id)
    publications_all = sql_quories.fetch_publications(page_id)
    publications = __strip_None_values(publications_all)
    allow_pi = check_credentials.is_pi()
    allow_member = check_credentials.check_page_ownership(page_id)
    allow_student = check_credentials.is_student()
    return render_template("member_page.html", name=name, introductory_text=introductory_text, \
                            allow_pi=allow_pi, allow_member=allow_member, allow_student=allow_student, page_id=page_id, \
                            keywords=keywords, publications=publications)

@app.route("/new_message", methods=["POST"])
def new_message():
    if "new_feedback" in request.form:
        content = request.form["new_feedback"]
        if len(content) > 10000:
            return render_template("error.html", error="content too long")
        sql_quories.insert_message(1, content, 0, session)
        session["feedback_left"] = True
        return redirect("/")
    elif "new_comment" in request.form:
        content = request.form["new_comment"]
        topic_id = request.form["topic_id"]
        if len(content) > 10000:
            return render_template("error.html", error="content too long")
        sql_quories.insert_message(0, content, topic_id, session)
        return redirect("/student_topics/" + str(topic_id))
        
@app.route("/new_page", methods=["POST"])
def new_page():
    if not check_credentials.csrf_check(request.form["csrf_token"]):
        return render_template("error.html", error="detected csrf_vulnerability exploitation attempt")
    if check_credentials.is_member() and check_credentials.check_page_ownership(0):
        return render_template("error.html", error="already has personal page")
    if check_credentials.is_pi() or check_credentials.is_member():
        return render_template("new_page.html")
    else: return render_template("error.html", error="insufficient credentials")

@app.route("/new_topic", methods=["POST"])
def new_topic():
    if not check_credentials.csrf_check(request.form["csrf_token"]):
        return render_template("error.html", error="detected csrf_vulnerability exploitation attempt")
    if check_credentials.is_pi() or check_credentials.is_member():
        return render_template("new_topic.html")
    else: return render_template("error.html", error="insufficient credentials")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        new_password = request.form["new_password"]
        repeat_password = request.form["repeat_password"]
        if new_password != repeat_password:
            return render_template("error.html", error="repeat_password does not match")
        if new_password == "":
            return render_template("error.html", error="no password set")
        new_username = request.form["new_username"]

        #these regular expressions were hard to write into a single expression, so three different checks for password validity
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
        session["role"] = "student"
        session["csrf_token"] = os.urandom(16).hex()
        return redirect("/")

@app.route("/reserve_topic", methods=["POST"])
def reserve_topic():
    if not check_credentials.csrf_check(request.form["csrf_token"]):
        return render_template("error.html", error="detected csrf_vulnerability exploitation attempt")
    if check_credentials.is_student():
        sql_quories.reserve_topic(session, request.form["topic_id"])
        return redirect("/student_topics/" + request.form["topic_id"])
    else: return render_template("error.html", error="insufficient credentials")

@app.route("/student_topics/<int:page_id>")
def student_topics(page_id):
    allow_pi = check_credentials.is_pi()
    allow_member = check_credentials.is_member()
    allow_student = check_credentials.is_student()
    topic_ids = sql_quories.fetch_topic_ids()
    topic_content = ()
    own_topic = False
    messages = ()
    latest_document_id = None
    if page_id != 0:
        topic_content = sql_quories.fetch_topic_content(page_id)
        if check_credentials.check_topic_ownership(page_id):
            own_topic = True
            messages = sql_quories.fetch_messages(page_id)
            latest_document_id = sql_quories.fetch_latest_document_id(page_id)
            if latest_document_id != None:
                latest_document_id = latest_document_id[0]
            print(latest_document_id)
    return render_template("student_topics.html", allow_pi=allow_pi,
                        allow_member=allow_member, allow_student=allow_student, topic_ids=topic_ids, page_id=page_id, \
                        topic_content=topic_content, own_topic=own_topic, messages=messages, latest_document_id=latest_document_id)

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
            new_name = request.form["new_name"]
            new_introduction = request.form["new_introduction"]
            if len(new_name) > 200 or len(new_introduction) > 10000:
                return render_template("error.html", error="new_name or new_introduction too long")
            sql_quories.insert_page(new_name, new_introduction)
            #after page creation: adding credentials for PI (and whomever just created the page)
            new_page_id = sql_quories.insert_credentials(session, new_name)
            return redirect("member_page/" + str(new_page_id))
        else: return render_template("error.html", error="insufficient credentials")
    elif "new_topic" in request.form:
        if check_credentials.is_pi() or check_credentials.is_member():
            new_topic = request.form["new_topic"]
            new_description = request.form["new_description"]
            if len(new_topic) > 200 or len(new_description) > 10000:
                return render_template("error.html", error="new_topic or new_description too long")
            new_topic_id = sql_quories.insert_topic(new_topic, new_description, session["username"])
            return redirect("student_topics/" + str(new_topic_id))
        else: return render_template("error.html", error="insufficient credentials")
    elif "new_keyword" in request.form:
        new_keyword = request.form["new_keyword"]
        page_id = request.form["page_id"]
        if check_credentials.check_page_ownership(page_id):
            if len(new_keyword) > 200:
                return render_template("error.html", error="new_keyword too long")
            sql_quories.add_keyword(new_keyword, page_id)
            if page_id == "1": return redirect("/")
            else: return redirect("member_page/" + str(page_id))
        else: return render_template("error.html", error="insufficient credentials")
    elif "publication_title" in request.form:
        page_id = request.form["page_id"]
        data_fields = []
        if check_credentials.check_page_ownership(page_id):
            for k in request.form.keys():
                if len(request.form[k]) > 200:
                    return render_template("error.html", error="maximum field length is 200 characters")
                data_fields.append(request.form[k])
            if len(request.form["publication_volume"]) != 0:
                if re.search('^[0-9]+$', request.form["publication_volume"]) == None:
                    return render_template("error.html", error="publication volume has to be numbers")
            if len(request.form["publication_year"]) != 0:
                if re.search('^[0-9]+$', request.form["publication_year"]) == None:
                    return render_template("error.html", error="publication year has to be numbers")
            sql_quories.add_publication([data_fields[0]] + data_fields[3:], page_id)
            if page_id == "1": return redirect("/")
            else: return redirect("member_page/" + str(page_id))
        else: return render_template("error.html", error="insufficient credentials")
    elif "delete_publication" in request.form:
        page_id = request.form["page_id"]
        publications = sql_quories.fetch_publications(page_id)
        for publication in publications:
            if publication[0] in request.form:
                sql_quories.remove_publication(publication[0])
        return redirect("/")
    elif "delete_keyword" in request.form:
        page_id = request.form["page_id"]
        keywords = sql_quories.fetch_keywords(page_id)
        for keyword in keywords:
            if keyword[0] in request.form:
                sql_quories.remove_keyword(keyword[0])
        return redirect("/")
    elif "delete_logo" in request.form:
        logo_ids = sql_quories.fetch_image_ids()
        for logo_id in logo_ids:
            if str(logo_id[0]) in request.form:
                sql_quories.remove_logo(logo_id[0])
        return redirect("/")

@app.route("/upload", methods=["POST"])
def upload():
    if not check_credentials.csrf_check(request.form["csrf_token"]):
        return render_template("error.html", error="detected csrf_vulnerability exploitation attempt")
    if "upload_document" in request.files:
        topic_id = request.form["topic_id"]
        if check_credentials.check_topic_ownership(topic_id):
            document_file = request.files["upload_document"]
            document_filename = secure_filename(document_file.filename)
            if len(document_filename) == 0:
                return render_template("error.html", error="no file to upload")
            if document_file.mimetype == "application/msword":
                document_data = document_file.read()
                sql_quories.insert_file(document_filename, document_data, topic_id, session["username"])
                return redirect("/student_topics/" + str(topic_id))
            else: return render_template("error.html", error="only doc files are allowed")
    elif "upload_logo" in request.files:
        if check_credentials.is_pi():
            logo_file = request.files["upload_logo"]
            logo_filename = secure_filename(logo_file.filename)
            if len(logo_filename) == 0:
                return render_template("error.html", error="no file to upload")
            if logo_file.mimetype == "image/jpeg":
                logo_b64 = str(base64.b64encode(logo_file.read()))
                sql_quories.insert_logo(logo_filename, logo_b64[2:-1]) #logo inserted without b' at the front and ' at the end
                return redirect("/")
            else: return render_template("error.html", error="only jpg and jpeg files are allowed")
        else: return render_template("error.html", error="insufficient credentials")
    else: return render_template("error.html", error="insufficient credentials")

@app.route("/view_feedback", methods=["GET", "POST"]) #archive_message redirects here with GET
def view_feedback():
    if request.method == "POST":
        if not check_credentials.csrf_check(request.form["csrf_token"]):
            return render_template("error.html", error="detected csrf_vulnerability exploitation attempt")
    allow_pi = check_credentials.is_pi()
    archived = "view_archived_feedback" in request.form
    if allow_pi:
        messages = sql_quories.fetch_feedback(archived)
        return render_template("feedback.html", allow_pi=allow_pi, messages=messages,
                                archived=archived)
    else: return render_template("error.html", error="insufficient credentials")