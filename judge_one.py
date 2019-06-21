#!/usr/bin/env python
# coding=utf-8
import protect, os, config, shlex, logging, lorun, DBData


def judge_one_mem_time(submit_id, problem_id, data_num, time_limit, mem_limit, language):
    protect.low_level()
    '''评测一组数据'''
    lans = DBData.lans
    input_path = os.path.join(config.data_dir, str(problem_id), 'data%s.in' % data_num)  # 获取存放输入数据的文件的路径
    try:
        input_data = open(input_path)  # 尝试打开
    except:
        return False  # 无法打开
    # 创建一个供写入数据的txt文件（用于存放用户程序的运行结果）
    output_path = os.path.join(config.work_dir, str(submit_id), 'out%s.txt' % data_num)
    temp_out_data = open(output_path, 'w')  # 以写入方法创建打开上述文件
    if lans[language][0] == 'java':
        mem_limit += 1000000
        cmd = 'java -cp %s Main' % (os.path.join(config.work_dir, str(submit_id)))
        main_exe = shlex.split(cmd)  # 使用类似shell的语法分割cmd
    elif lans[language][0] == 'python2':
        cmd = 'python2 %s' % (os.path.join(config.work_dir, str(submit_id), 'main.pyc'))
        main_exe = shlex.split(cmd)
    elif lans[language][0] == 'python3':
        cmd = 'python3 %s' % (os.path.join(config.work_dir, str(submit_id), 'main.py'))
        main_exe = shlex.split(cmd)
    elif lans[language][0] == 'lua':
        cmd = "lua %s" % (os.path.join(config.work_dir, str(submit_id), "main"))
        main_exe = shlex.split(cmd)
    elif lans[language][0] == "ruby":
        cmd = "ruby %s" % (os.path.join(config.work_dir, str(submit_id), "main.rb"))
        main_exe = shlex.split(cmd)
    elif lans[language][0] == "perl":
        cmd = "perl %s" % (os.path.join(config.work_dir, str(submit_id), "main.pl"))
        main_exe = shlex.split(cmd)
    else:
        main_exe = [os.path.join(config.work_dir, str(submit_id), 'main'), ]
    runcfg = {
        'args': main_exe,
        'fd_in': input_data.fileno(),  # 一个整型的文件描述符(文件id)
        'fd_out': temp_out_data.fileno(),  # 同上
        'timelimit': time_limit,  # in MS
        'memorylimit': mem_limit,  # in KB
    }
    protect.low_level()
    rst = lorun.run(runcfg)  # 在lorun黑盒中运行程序
    input_data.close()
    temp_out_data.close()
    logging.debug(rst)
    return rst  # {result:int,timeused:int,memoryused:int}
