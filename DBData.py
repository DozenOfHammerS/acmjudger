import db

result_code = None
lans = None


def get_result_code():
    sql = "select id,status from django_web_result"
    res = db.run_sql(sql)
    global result_code
    result_code = dict()
    for id, status in res:
        result_code[status] = id


def get_lans():
    sql = "select id,lan,filename,buildcmd from django_web_lang"
    res = db.run_sql(sql)
    global lans
    lans = dict()
    for id, lan, filename, cmd in res:
        lans[id] = (lan, filename, cmd)
