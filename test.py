import db
import logging
import datetime

# sql = "select count(*) from django_web_submitproblem where user_id = 1 and problem_id = 1 and result_id = 4"
# res = db.run_sql(sql)
# print(res[0][0])

# logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s --- %(message)s', filename="log.txt")
#
# if __name__ == '__main__':
#     logging.info("Start print log")
#     logging.debug("Do something")
#     logging.warning("Something maybe fail.")
#     logging.info("Finish")

# sql = "select start_time from django_web_contest where contest_id = 1"
# res = db.run_sql(sql)
# now = datetime.datetime.now()
# print(res[0][0])
# print(now)
# print(res[0][0].hour)
# td = now - res[0][0]
# print(td)
# print(td.hour)
# print(td.minute)
# print(td.seconds)
# contest_id = 1
# sql = "select punish_time from django_web_contest where contest_id = " + str(contest_id)
# res = db.run_sql(sql)
# print(res[0][0])
user_id = 11
contest_id = 0
problem_id = 1
result_code = 1

# def get_punish_num(user_id, contest_id, problem_id, result_code):
#     sql = "select count(*) from django_web_submitproblem where user_id = " + str(user_id) + " and problem_id = " + str(
#         problem_id) + " and result_id != " + str(result_code) + " and contest_id = " + str(contest_id)
#     res = db.run_sql(sql)
#     return res[0][0]
#
#
# def get_contest_start(contest_id):
#     sql = "select start_time from django_web_contest where contest_id = " + str(contest_id)
#     res = db.run_sql(sql)
#     return res[0][0]
#
#
# def get_time_spent(contest_id):
#     start_time = get_contest_start(contest_id)
#     now = datetime.datetime.now()
#     dt = now - start_time
#     return dt.seconds
#
#
# def get_punish_time(contest_id):
#     sql = "select punish_time from django_web_contest where contest_id = " + str(contest_id)
#     res = db.run_sql(sql)
#     return res[0][0]
#
#
# def update_user_contest(problem_time, user_id, contest_id):
#     sql = "update django_web_user_contest set ac_num = ac_num+1 , total_time = total_time + " + str(
#         problem_time) + " where contest_id = " + str(contest_id) + " and user_id = " + str(user_id)
#     res=db.run_sql(sql)
#     print(res)
#
#
# def insert_user_contest_problem(punish_num, contest_id, problem_id, user_id):
#     time_spent = get_time_spent(contest_id)
#     punish_time = get_punish_time(contest_id)
#     punish_time = punish_num * punish_time * 60
#     problem_time = time_spent + punish_time
#     sql = "insert into django_web_user_contest_problem(use_time,punish_time,contest_id,problem_id,user_id) values(%s,%s,%s,%s,%s)";
#     data = (time_spent, punish_num, contest_id, problem_id, user_id)
#     db.InsertData(sql, data)
#     update_user_contest(problem_time, user_id, contest_id)
#
#
# punish_num = get_punish_num(user_id, contest_id, problem_id, result_code)
# insert_user_contest_problem(punish_num, contest_id, problem_id, user_id)

# sql = "select count(*) from django_web_submitproblem where user_id = " + str(user_id) + " and problem_id = " + str(
#     problem_id) + " and result_id = " + str(result_code) + " and contest_id = " + str(contest_id)
# sql = "select is_true from django_web_user_contest_problem where contest_id = " + str(
#         contest_id) + " and user_id = " + str(user_id) + " and problem_id = " + str(problem_id)
# # print(sql)
# res = db.run_sql(sql)
# print(res)
# sql = "select count(*) from django_web_user_contest_problem where contest_id = " + str(
#     contest_id) + " and problem_id = " + str(problem_id) + " and first_ac = 1"
# res = db.run_sql(sql)
# print(res[0][0] == 0)
# sql = "update django_web_user_contest_problem set punish_time = punish_time + 1 where contest_id = " + str(
#     contest_id) + " and user_id = " + str(user_id) + " and problem_id = " + str(problem_id)
# res = db.run_sql(sql)
# def aaa():
#     sql = "select start_time,punish_time from django_web_contest where contest_id = " + str(contest_id)
#     res = db.run_sql(sql)
#     return res[0]
#
#
# start_time, b = aaa()
# now = datetime.datetime.now()
# dt = now - start_time
# print(dt)

# sql = "select punish_time from django_web_user_contest_problem where user_id = " + str(
#     user_id) + " and contest_id = " + str(contest_id) + " and problem_id = " + str(problem_id)
# res = db.run_sql(sql)
# print(res[0][0])

# print((0+1)%2)
# sql = "update django_web_user_contest_problem set use_time = " + str(18615) + ",first_ac = " + str(
#     1) + ",is_true = 1 where contest_id = " + str(contest_id) + " and user_id = " + str(
#     user_id) + " and problem_id = " + str(problem_id)
# db.run_sql(sql)

sql = "select count(*) from django_web_submitproblem where user_id = " + str(user_id) + " and problem_id = " + str(
        problem_id) + " and result = " + str(result_code) + " and submit_id != " + str(126)
print(sql)
res=db.run_sql(sql)
print(res[0][0] == 0)