#!/usr/bin/env python
# coding=utf-8
import protect, time, get_code, deal_data, db, logging, threading, DBData


def put_task_into_queue():
    '''循环扫描数据库,将任务添加到队列'''
    while True:
        protect.q.join()  # 阻塞程序,直到队列里面的任务全部完成
        sql = "select submit_id, problem_id, user_id, contest_id, `language` from django_web_submitproblem where result = 0"
        data = db.run_sql(sql)
        time.sleep(0.5)  # 延时0.5秒,防止因速度太快不能获取代码
        for i in data:
            submit_id, problem_id, user_id, contest_id, language = i
            protect.dblock.acquire()
            ret = get_code.get_code(submit_id, problem_id, language)
            protect.dblock.release()
            if ret is False:  # 生成文件失败 再次尝试
                # 防止因速度太快不能获取代码
                logging.error("首次生成文件失败 by %s" % threading.current_thread().name)
                time.sleep(0.5)
                protect.dblock.acquire()
                ret = get_code.get_code(submit_id, problem_id, language)
                protect.dblock.release()
            if ret is False:  # 生成文件依旧失败
                protect.dblock.acquire()
                logging.error("再次生成文件失败 by %s " % threading.current_thread().name)
                update_solution_status(submit_id, DBData.result_code["System Error"])  # 设置结果为系统错误
                protect.dblock.release()
                deal_data.clean_work_dir(submit_id)  # 清理get_code函数所产生的文件夹及文件
                continue
            logging.info("生成文件成功 by %s " % threading.current_thread().name)
            task = {  # 生成判题任务
                "submit_id": submit_id,
                "problem_id": problem_id,
                "contest_id": contest_id,
                "user_id": user_id,
                "language": language,
            }
            protect.q.put(task)  # 将判题任务添加到判题队列中
            protect.dblock.acquire()
            update_solution_status(submit_id, DBData.result_code["Judging"])  # 状态结果改成正在判题
            protect.dblock.release()
        time.sleep(0.5)


def update_solution_status(submit_id, status):
    sql = "update django_web_submitproblem set result = " + str(status) + " where submit_id = " + str(submit_id)
    db.run_sql(sql)
