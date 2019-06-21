#!/usr/bin/env python
# coding=utf-8
import protect, logging, os, config, DBData




def judge_result(problem_id, submit_id, data_num):
    protect.low_level()
    '''对输出数据进行评测'''
    result_code = DBData.result_code
    logging.debug("Judging result")
    correct_result = os.path.join(
        config.data_dir, str(problem_id), 'data%s.out' %
                                          data_num)  # 获取存放正确输出的文件的路径
    user_result = os.path.join(
        config.work_dir, str(submit_id), 'out%s.txt' %
                                         data_num)  # 获取存放用户代码输出的文件的路径
    try:  # 尝试获取样例结果与用户程序输出结果
        correct = open(correct_result).read().replace('\r', '').rstrip()  # 删除\r,删除行末的空格和换行
        user = open(user_result).read().replace('\r', '').rstrip()
    except:
        logging.error("打开样例结果于程序输出结果失败")
        return False
    print("correct:" + correct)
    print("user:" + user)
    print("result:", correct.__eq__(user))
    # if correct.__eq__(user):  # 完全相同:AC
    #     return "Accepted"
    # if correct.split().__eq__(user.split()):  # 除去空格,tab,换行相同:PE
    #     return "Presentation Error"
    # if correct in user:  # 输出多了
    #     return "Output limit"
    # return "Wrong Answer"  # 其他WA
    try:
        if correct.__eq__(user):  # 完全相同:AC
            return result_code["Accepted"]
        if correct.split().__eq__(user.split()):  # 除去空格,tab,换行相同:PE
            return result_code["Presentation Error"]
        if correct in user:  # 输出多了 OLE
            return result_code["Output Limit"]
        return result_code["Wrong Answer"]  # 其他WA
    except:
        logging.error("未知状态值")
        return result_code["System Error"]
