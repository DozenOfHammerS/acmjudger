#!/usr/bin/env python
# coding=utf-8
import protect, logging, threading, deal_data, config, deal_data, run_program, db, DBData, datetime


def worker():
    '''工作线程，循环扫描队列，获得评判任务并执行'''
    result_code = DBData.result_code
    while True:
        if protect.q.empty() is True:  # 队列为空，空闲
            logging.info("%s idle" % (threading.current_thread().name))
        task = protect.q.get()  # 获取任务，如果队列为空则阻塞
        submit_id = task['submit_id']
        problem_id = task['problem_id']
        language = task['language']
        user_id = task['user_id']
        contest_id = task['contest_id']
        data_count = deal_data.get_data_count(task['problem_id'])  # 获取测试数据的个数
        logging.info("judging %s" % submit_id)
        result = run_program.run(
            problem_id,
            submit_id,
            language,
            data_count,
            user_id)  # 评判
        logging.info("%s result %s" % (result['submit_id'], result['result']))
        update_result(result)  # 将结果写入数据库
        if result['result'] == result_code["Accepted"]:
            add_accept_total(result["problem_id"])  # 增加题目AC数
        if is_not_accepted(result["user_id"], result["problem_id"], result_code["Accepted"]):
            add_user_accept_total(result["user_id"])  # 增加用户AC数
        if contest_id > 0 and is_not_Accepted_Contest(user_id, contest_id, problem_id,
                                                      result_code["Accepted"]):  # 此题为比赛题且此前未AC
            # 如果这次不是ac 更新punish_num+=1
            if result['result'] != result_code["Accepted"]:
                update_punish_time(contest_id, user_id, problem_id)
            else:  # 如果是ac
                is_fac = is_first_ac(contest_id, problem_id)  # 判断是否是首A
                start_time, punish_time = get_contest_start_and_punish_time(contest_id)
                use_time = get_time_spent(start_time)
                punish_num = get_punish_num(user_id, contest_id, problem_id)
                use_total_time = punish_num * punish_num + use_time
                update_user_contest_problem(contest_id, user_id, problem_id, use_time, is_fac)
                update_user_contest(contest_id, user_id, use_total_time)
        if config.auto_clean:  # 清理work目录
            deal_data.clean_work_dir(result['submit_id'])  # result的结构见program_info（run_program.py）
        protect.q.task_done()  # 一个任务完成


# program_info = {
#         "submit_id": solution_id,
#         "problem_id": problem_id,
#         "take_time": 0,
#         "take_memory": 0,
#         "user_id": user_id,
#         "result": 0,
#     }

def is_first_ac(contest_id, problem_id):
    protect.dblock.acquire()
    sql = "select count(*) from django_web_user_contest_problem where contest_id = " + str(
        contest_id) + " and problem_id = " + str(problem_id) + " and first_ac = 1"
    res = db.run_sql(sql)
    protect.dblock.release()
    return (res[0][0] + 1) % 2


def update_result(result):
    protect.dblock.acquire()
    sql = "update django_web_submitproblem set take_time= " + str(result["take_time"]) + " ,take_memory=" + str(
        result["take_memory"]) + ", result=" + str(result["result"]) + " where submit_id = " + str(
        result["submit_id"])
    db.run_sql(sql)
    protect.dblock.release()


def add_accept_total(problem_id):
    protect.dblock.acquire()
    sql = "update django_web_problem set total_ac = total_ac + 1 where problem_id = " + str(problem_id)
    db.run_sql(sql)
    protect.dblock.release()


def is_not_accepted(user_id, problem_id, result_code):
    protect.dblock.acquire()
    sql = "select count(*) from django_web_submitproblem where user_id = " + str(user_id) + " and problem_id = " + str(
        problem_id) + " and result = " + str(result_code)
    res = db.run_sql(sql)
    protect.dblock.release()
    return res[0][0] == 0


def add_user_accept_total(user_id):
    protect.dblock.acquire()
    sql = "update django_web_user set total_ac = total_ac + 1 where id = " + str(user_id)
    db.run_sql(sql)
    protect.dblock.release()


def is_not_Accepted_Contest(user_id, contest_id, problem_id, result_code):
    protect.dblock.acquire()
    # sql = "select count(*) from django_web_submitproblem where user_id = " + str(user_id) + " and problem_id = " + str(
    #     problem_id) + " and result_id = " + str(result_code) + " and contest_id = " + str(contest_id)
    sql = "select is_true from django_web_user_contest_problem where contest_id = " + str(
        contest_id) + " and user_id = " + str(user_id) + "and problem_id = " + str(problem_id)
    res = db.run_sql(sql)
    protect.dblock.release()
    return res[0][0] == 0


def get_punish_num(user_id, contest_id, problem_id):
    protect.dblock.acquire()
    # sql = "select count(*) from django_web_submitproblem where user_id = " + str(user_id) + " and problem_id = " + str(
    #     problem_id) + " and result_id != " + str(result_code) + " and contest_id = " + str(contest_id)
    sql = "select punish_time from django_web_user_contest_problem where user_id = " + str(
        user_id) + " and contest_id = " + str(contest_id) + " and problem_id = " + str(problem_id)
    res = db.run_sql(sql)
    protect.dblock.release()
    return res[0][0]


def get_contest_start_and_punish_time(contest_id):
    protect.dblock.acquire()
    sql = "select start_time,punish_time from django_web_contest where contest_id = " + str(contest_id)
    res = db.run_sql(sql)
    protect.dblock.release()
    return res[0]


def get_time_spent(start_time):
    now = datetime.datetime.now()
    dt = now - start_time
    return dt.seconds


def get_punish_time(contest_id):
    protect.dblock.acquire()
    sql = "select punish_time from django_web_contest where contest_id = " + str(contest_id)
    res = db.run_sql(sql)
    protect.dblock.release()
    return res[0][0]


def update_user_contest(contest_id, user_id, use_total_time):
    protect.dblock.acquire()
    sql = "update django_web_user_contest set ac_num = ac_num + 1 , total_time = total_time + " + str(
        use_total_time) + " where contest_id = " + str(contest_id) + " and user_id = " + str(user_id)
    db.run_sql(sql)
    protect.dblock.release()


def update_user_contest_problem(contest_id, user_id, problem_id, use_time, is_fac):
    protect.dblock.acquire()
    # sql = "insert into django_web_user_contest_problem(use_time,punish_time,contest_id,problem_id,user_id) values(%s,%s,%s,%s,%s)";
    # data = (time_spent, punish_num, contest_id, problem_id, user_id)
    # db.InsertData(sql, data)
    sql = "update django_web_user_contest_problem set use_time = " + str(use_time) + ",first_ac = " + str(
        is_fac) + ",is_true = 1 where contest_id = " + str(contest_id) + " and user_id = " + str(
        user_id) + " and problem_id = " + str(problem_id)
    db.run_sql(sql)
    protect.dblock.release()


def update_punish_time(contest_id, user_id, problem_id):
    protect.dblock.acquire()
    sql = "update django_web_user_contest_problem set punish_time = punish_time + 1 where contest_id = " + str(
        contest_id) + " and user_id = " + str(user_id) + " and problem_id = " + str(problem_id)
    db.run_sql(sql)
    protect.dblock.release()
