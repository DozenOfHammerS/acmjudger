#!/usr/bin/env python
# coding=utf-8
import protect, judge_main, logging, check_dangerout_code, compile, db, DBData


def run(problem_id, submit_id, language, data_count, user_id):  # 判题函数
    protect.low_level()
    '''获取程序执行时间和内存'''
    time_limit, mem_limit = get_problem_limit(problem_id)
    program_info = {
        "submit_id": submit_id,
        "problem_id": problem_id,
        "take_time": 0,
        "take_memory": 0,
        "user_id": user_id,
        "result": 0,
    }
    # result_code = {
    #     "Waiting": 0,
    #     "Accepted": 1,
    #     "Time Limit Exceeded": 2,
    #     "Memory Limit Exceeded": 3,
    #     "Wrong Answer": 4,
    #     "Runtime Error": 5,
    #     "Output limit": 6,
    #     "Compile Error": 7,
    #     "Presentation Error": 8,
    #     "System Error": 11,
    #     "Judging": 12,
    # }
    result_code = DBData.result_code
    if check_dangerout_code.check_dangerous_code(submit_id, language) == False:  # 事先检查
        program_info['result'] = result_code["Runtime Error"]
        return program_info
    compile_result = compile.compile(submit_id, language)
    if compile_result is False:  # 编译错误
        program_info['result'] = result_code["Compile Error"]
        return program_info
    if data_count == 0:  # 没有测试数据
        program_info['result'] = result_code["System Error"]
        return program_info
    result = judge_main.judge(
        data_count,
        time_limit,
        mem_limit,
        program_info,
        language)
    logging.debug(result)
    return result


def get_problem_limit(problem_id):
    protect.dblock.acquire()
    sql = "select time_limit,mem_limit from django_web_problem  where problem_id = " + str(problem_id)
    res = db.run_sql(sql)
    protect.dblock.release()
    return res[0]
