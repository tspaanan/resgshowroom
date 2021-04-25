from flask.helpers import make_response
from db import db

def add_keyword(keyword, page_id):
    sql = "INSERT INTO keywords (keyword,visible) VALUES (:keyword,TRUE)"
    db.session.execute(sql, {"keyword":keyword})
    #fetching the id for keyword just added
    result = db.session.execute("SELECT id FROM keywords LIMIT 1 OFFSET (SELECT COUNT(*) FROM keywords)-1")
    sql = "INSERT INTO page_keywords (page_id,keyword_id) VALUES (:page_id,:keyword_id)"
    db.session.execute(sql, {"page_id":page_id, "keyword_id":result.fetchone()[0]})
    db.session.commit()

def add_publication(data: list, page_id):
    sql = "INSERT INTO publications (title,subtitle,journal,volume,issue,year,page_no,doi,visible) VALUES \
            (:title,:subtitle,:journal,:volume,:issue,:year,:page_no,:doi,TRUE)"
    db.session.execute(sql, {"title":data[0], "subtitle":data[1], "journal":data[2], "volume":int(data[3]) if data[3] != "" else None,
                         "issue":data[4], "year":int(data[5]) if data[5] != "" else None, "page_no":data[6], "doi":data[7]})
    #fetching the id for publication just added
    result = db.session.execute("SELECT id FROM publications LIMIT 1 OFFSET (SELECT COUNT(*) FROM publications)-1")
    sql = "INSERT INTO page_publications (page_id,publication_id) VALUES (:page_id,:publication_id)"
    db.session.execute(sql, {"page_id":page_id, "publication_id":result.fetchone()[0]})
    db.session.commit()

def archive_message(message_id):
    sql = "UPDATE messages SET archived=TRUE WHERE id=:message_id"
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()

def fetch_feedback(archived):
    sql = "SELECT id,message,time FROM messages WHERE archived=:archived AND page_id=1 AND visible=TRUE"
    result = db.session.execute(sql, {"archived":archived})
    return result.fetchall()

def fetch_images():
    sql = "SELECT data FROM images WHERE visible=TRUE"
    result = db.session.execute(sql)
    image_data = result.fetchone()[0]
    response = make_response(bytes(image_data))
    response.headers.set("Content-Type","image/jpeg")
    return response

def fetch_introduction(page_id):
    sql = "SELECT introduction FROM pages WHERE id=:page_id"
    result = db.session.execute(sql, {"page_id":page_id})
    return result.fetchone()[0]

def fetch_keywords(page_id):
    sql = "SELECT keyword FROM keywords KW,page_keywords PK WHERE KW.id=PK.keyword_id \
           AND PK.page_id=:page_id AND KW.visible=TRUE"
    result = db.session.execute(sql, {"page_id":page_id})
    return result.fetchall()

def fetch_member_pages():
    sql = "SELECT id,title FROM pages WHERE id>1 AND visible=TRUE"
    result = db.session.execute(sql)
    return result.fetchall()

def fetch_messages(topic_id):
    sql = "SELECT message,time,user_id FROM messages WHERE topic_id=:topic_id AND visible=TRUE ORDER BY time DESC"
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()
    
def fetch_password(username):
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()

def fetch_publications(page_id):
    sql = "SELECT title,subtitle,journal,volume,year,issue, \
           page_no,doi FROM publications P,page_publications PP WHERE \
           P.id=PP.publication_id AND PP.page_id=:page_id AND P.visible=TRUE"
    result = db.session.execute(sql, {"page_id":page_id})
    return result.fetchall()

def fetch_role(username):
    sql = "SELECT role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()

def fetch_title(page_id):
    sql = "SELECT title FROM pages WHERE id=:page_id"
    result = db.session.execute(sql, {"page_id":page_id})
    return result.fetchone()[0]

def fetch_topic_ids():
    sql = "SELECT id FROM topics WHERE visible=TRUE"
    result = db.session.execute(sql)
    return result.fetchall()

def fetch_topic_content(page_id):
    sql = "SELECT topic,description,responsible_user_id,chosen FROM topics WHERE id=:page_id AND visible=TRUE"
    result = db.session.execute(sql, {"page_id":page_id})
    return result.fetchall()

def fetch_topics():
    sql = "SELECT topic,description,responsible_user_id FROM topics WHERE chosen=FALSE AND visible=TRUE"
    result = db.session.execute(sql)
    return result.fetchall()

def fetch_user_id(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()[0]

def insert_credentials(session, new_name):
    username = session["username"]
    new_user_id = fetch_user_id(username)
    result = db.session.execute("SELECT id FROM pages WHERE title=:new_name", {"new_name":new_name})
    new_page_id = result.fetchone()[0]
    sql = "INSERT INTO page_ownership (user_id,page_id) VALUES (:new_user_id,:new_page_id)"
    db.session.execute(sql, {"new_user_id":new_user_id, "new_page_id":new_page_id})
    db.session.commit()
    if new_user_id != 1:
        db.session.execute(sql, {"new_user_id":"1", "new_page_id":new_page_id})
        db.session.commit()
    return new_page_id

def insert_message(page_id, content, topic_id, session):
    if page_id != 0:
        sql = "INSERT INTO messages (message,time,archived,page_id,visible) VALUES" \
            "(:content,NOW(),FALSE,:page_id,TRUE)"
        db.session.execute(sql, {"content":content, "page_id":page_id})
    else:
        username = session["username"]
        sql = "INSERT INTO messages (message,time,archived,topic_id,visible,user_id) VALUES" \
            "(:content,NOW(),FALSE,:topic_id,TRUE,:user_id)"
        db.session.execute(sql, {"content":content, "topic_id":topic_id, "user_id":fetch_user_id(username)})
    db.session.commit()

def insert_page(title, introduction):
    sql = "INSERT INTO pages (title,introduction,visible) VALUES (:new_name,:new_introduction,TRUE)"
    db.session.execute(sql, {"new_name":title, "new_introduction":introduction})
    db.session.commit()

def insert_topic(topic, description, username):
    user_id = fetch_user_id(username)
    sql = "INSERT INTO topics (topic,description,responsible_user_id,chosen,visible) VALUES (:new_topic,:new_description,:user_id,FALSE,TRUE)"
    db.session.execute(sql, {"new_topic":topic, "new_description":description, "user_id":user_id})
    db.session.commit()
    #return topic_id of newly created topic
    return db.session.execute("SELECT id FROM publications LIMIT 1 OFFSET (SELECT COUNT(*) FROM publications)-1").fetchone()[0]

def insert_user(username, password, role):
    sql = "INSERT INTO users (username,password,role) VALUES (:username,:password,:role)"
    db.session.execute(sql, {"username":username, "password":password, "role":role})
    db.session.commit()

def reserve_topic(session, topic_id):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":session["username"]})
    sql = "UPDATE topics SET chosen=TRUE,student_id=:username_id WHERE id=:topic_id"
    db.session.execute(sql, {"username_id":result.fetchone()[0], "topic_id":topic_id})
    db.session.commit()

def update_introduction(introduction, page_id):
    sql = "UPDATE pages SET introduction=:new_introduction WHERE id=:page_id"
    db.session.execute(sql, {"new_introduction":introduction, "page_id":page_id})
    db.session.commit()

def update_title(title, page_id):
    sql = "UPDATE pages SET title=:new_title WHERE id=:page_id"
    db.session.execute(sql, {"new_title":title, "page_id":page_id})
    db.session.commit()