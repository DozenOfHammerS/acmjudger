#!/usr/bin/env python
# coding=utf-8
import protect, judge_one, judge_result, logging, db, DBData


def judge(data_count, time_limit, mem_limit, program_info, language):
    protect.low_level()
    '''评测编译类型语言'''
    max_mem = 0
    max_time = 0
    submit_id = program_info["submit_id"]
    problem_id = program_info["problem_id"]
    lans = DBData.lans
    result_code = DBData.result_code
    if lans[language][0] in ["java", 'python2', 'python3', 'ruby', 'perl']:  # 若所选语言是这些 条件放宽
        time_limit = time_limit * 2
        mem_limit = mem_limit * 2
    for i in range(data_count):
        ret = judge_one.judge_one_mem_time(  # 评测一组数据
            submit_id,
            problem_id,
            i + 1,
            time_limit + 10,
            mem_limit,
            language)
        if lans[language][0] == 'java' and ret["memoryused"] > mem_limit:
            ret["result"] = result_code["Memory Limit Exceeded"]
        if ret == False:  # 无法打开相应测试数据
            logging.error("ret = False")
            get_sample_result(submit_id, i + 1, ret["timeused"], ret["memoryused"], result_code["System Error"])
            continue
        if ret['result'] == result_code["Runtime Error"]:
            program_info['result'] = result_code["Runtime Error"]
            get_sample_result(submit_id, i + 1, ret["timeused"], ret["memoryused"], result_code["Runtime Error"])
            return program_info
        elif ret['result'] == result_code["Time Limit Exceeded"]:
            program_info['result'] = result_code["Time Limit Exceeded"]
            program_info['take_time'] = time_limit + 10
            return program_info
        elif ret['result'] == result_code["Memory Limit Exceeded"]:
            program_info['result'] = result_code["Memory Limit Exceeded"]
            program_info['take_memory'] = mem_limit
            return program_info
        if max_time < ret["timeused"]:
            max_time = ret['timeused']
        if max_mem < ret['memoryused']:
            max_mem = ret['memoryused']
        result = judge_result.judge_result(problem_id, submit_id, i + 1)
        if result == False:  # 无法获取测试输出或样例输出
            get_sample_result(submit_id, i + 1, 0, 0, result_code["System Error"])
            continue
        if result == result_code["Wrong Answer"] or result == result_code["Output Limit"]:
            program_info['result'] = result
            get_sample_result(submit_id, i + 1, ret["timeused"], ret["memoryused"], result)
            break
        elif result == result_code['Presentation Error']:
            program_info['result'] = result
            get_sample_result(submit_id, i + 1, ret["timeused"], ret["memoryused"], result)
        elif result == result_code['Accepted']:
            get_sample_result(submit_id, i + 1, ret["timeused"], ret["memoryused"], result)
            if program_info['result'] != result_code['Presentation Error']:
                program_info['result'] = result
        else:
            logging.error("judge did not get result")
    if program_info["result"] == result_code["Waiting"]:
        program_info["result"] = result_code["System Error"]
    program_info['take_time'] = max_time
    program_info['take_memory'] = max_mem
    return program_info


def get_sample_result(submit_id, sample_id, time, mem, result):
    sql = "Insert into django_web_sample(submit_id,sample_id,take_time,take_memory,result) " \
          "values(%s,%s,%s,%s,%s)"
    data = (submit_id, sample_id, time, mem, result)
    protect.dblock.acquire()
    res = db.InsertData(sql, data)
    protect.dblock.release()
    if res <= 0:
        logging.error("样例结果插入失败")
