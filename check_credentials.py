def is_pi(db, session):
    #TODO: write elegantly what's below
    sql = "SELECT role FROM users WHERE username=:username"
    try:
        username = session["username"]
    except:
        username = "admin_test"
    print(username)
    result = db.session.execute(sql, {"username":username})
    if result.fetchone()[0] == "admin_test":
        return True
    else:
        return False