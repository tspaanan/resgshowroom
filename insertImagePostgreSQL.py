def tempInsert(db):
    filename = "pexels-ern-361096.jpg"
    with open(filename, 'rb') as f:
        data = f.read()

    sql = "INSERT INTO images (name,data) VALUES ('testiLogo',:data)"
    try:
        db.session.execute(sql, {"data":data})
        db.session.commit()
    except:
        print('Exception occured...')

