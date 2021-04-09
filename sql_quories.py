from flask.helpers import make_response

def archive_message(db, message_id):
        sql = "UPDATE messages SET archived=TRUE WHERE id=:message_id"
        db.session.execute(sql, {"message_id":message_id})
        db.session.commit()

def fetch_feedback(db, archived):
        sql = "SELECT id,message,time FROM messages WHERE archived=:archived"
        result = db.session.execute(sql, {"archived":archived})
        return result.fetchall()

def fetch_images(db):
    sql = "SELECT data FROM images"
    result = db.session.execute(sql)
    image_data = result.fetchone()[0]
    response = make_response(bytes(image_data))
    response.headers.set("Content-Type","image/jpeg")
    return response

def fetch_introduction(db, page_id):
    sql = "SELECT introduction FROM pages WHERE id=:page_id"
    result = db.session.execute(sql, {"page_id":page_id})
    return result.fetchone()[0]

def fetch_keywords(db, page_id):
    sql = "SELECT keyword FROM keywords KW,page_keywords PK WHERE KW.id=PK.keyword_id \
           AND PK.page_id=:page_id"
    result = db.session.execute(sql, {"page_id":page_id})
    return result.fetchall()

def fetch_member_pages(db):
    sql = "SELECT id FROM pages WHERE id>1"
    result = db.session.execute(sql)
    return result.fetchall()

def fetch_password(db, username):
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()

def fetch_publications(db, page_id):
    sql = "SELECT title,subtitle,journal,volume,year,issue, \
           page_no,doi FROM publications P,page_publications PP WHERE \
           P.id=PP.publication_id AND PP.page_id=:page_id"
    result = db.session.execute(sql, {"page_id":page_id})
    return result.fetchall()

def fetch_title(db, page_id):
    sql = "SELECT title FROM pages WHERE id=:page_id"
    result = db.session.execute(sql, {"page_id":page_id})
    return result.fetchone()[0]

def fetch_topics(db):
    sql = "SELECT topic,description,responsible_user_id FROM topics WHERE chosen=FALSE"
    result = db.session.execute(sql)
    return result.fetchall()

def insert_credentials(db, session, new_name):
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
    return new_page_id

def insert_message(db, page_id, content):
    sql = "INSERT INTO messages (message,time,archived,page_id) VALUES" \
        "(:content,NOW(),FALSE,:page_id)"
    db.session.execute(sql, {"content":content, "page_id":page_id})
    db.session.commit()

def insert_page(db, title, introduction):
    sql = "INSERT INTO pages (title,introduction) VALUES (:new_name,:new_introduction)"
    db.session.execute(sql, {"new_name":title, "new_introduction":introduction})
    db.session.commit()

def insert_user(db, username, password, role):
    sql = "INSERT INTO users (username,password,role) VALUES (:username, :password, :role)"
    db.session.execute(sql, {"username":username, "password":password, "role":role})
    db.session.commit()

def update_introduction(db, introduction, page_id):
    sql = "UPDATE pages SET introduction=:new_introduction WHERE id=:page_id"
    db.session.execute(sql, {"new_introduction":introduction, "page_id":page_id})
    db.session.commit()

def update_title(db, title, page_id):
    sql = "UPDATE pages SET title=:new_title WHERE id=:page_id"
    db.session.execute(sql, {"new_title":title, "page_id":page_id})
    db.session.commit()