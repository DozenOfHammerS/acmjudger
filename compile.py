#!/usr/bin/env python
# coding=utf-8
import protect, os, config, subprocess, db, logging, threading, DBData


def compile(submit_id, language):
    protect.low_level()
    '''将程序编译成可执行文件'''
    dir_work = os.path.join(config.work_dir, str(submit_id))  # 获得代码文件的路径
    # build_cmd = {
    #     "gcc": "gcc main.c -o main -Wall -lm -O2 -std=c99 --static -DONLINE_JUDGE",
    #     "g++": "g++ main.cpp -O2 -Wall -lm --static -DONLINE_JUDGE -o main",
    #     "java": "javac Main.java",
    #     "ruby": "reek main.rb",
    #     "perl": "perl -c main.pl",
    #     "pascal": 'fpc main.pas -O2 -Co -Ct -Ci',
    #     "go": '/opt/golang/bin/go build -ldflags "-s -w"  main.go',
    #     "lua": 'luac -o main main.lua',
    #     "python2": 'python2 -m py_compile main.py',
    #     "python3": 'python3 -m py_compile main.py',
    #     "haskell": "ghc -o main main.hs",
    # }
    lans = DBData.lans
    # if language not in build_cmd.keys():
    #     return False
    p = subprocess.Popen(
        lans[language][2],  # 命令行
        shell=True,  # 在shell里执行命令行
        cwd=dir_work,  # 移动到dir_work目录下（设置工作目录）
        stdout=subprocess.PIPE,  # 需要建立标准输出管道 为了获取输出信息
        stderr=subprocess.PIPE)  # 需要建立标准错误管道 为了获取错误信息
    out, err = p.communicate()  # 获取编译错误信息
    err_txt_path = os.path.join(config.work_dir, str(submit_id), 'error.txt')  # 创建错误信息文件的路径
    f = open(err_txt_path, 'w')
    f.write(str(err))
    f.write(str(out))  # 写入错误信息和输出信息
    f.close()
    if p.returncode == 0:  # 返回值为0,编译成功
        logging.info("编译成功 by %s" % threading.current_thread().name)
        return True
    protect.dblock.acquire()
    logging.info("编译失败 by %s" % threading.current_thread().name)
    update_compile_info(str(submit_id), err + out)  # 更新编译结果信息
    protect.dblock.release()
    return False


def update_compile_info(submit_id, msg):
    # sql = "update django_web_SubmitProblem set result = " + str(
    #     DBData.result_code["Compile Error"]) + " where submit_id = " + str(submit_id)
    # db.run_sql(sql)
    pass
