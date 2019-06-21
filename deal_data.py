#!/usr/bin/env python
# coding=utf-8
import os, shutil, config, logging


def clean_work_dir(solution_id):
    '''清理word目录，删除临时文件'''
    dir_name = os.path.join(config.work_dir, str(solution_id))  # 得到 生成的对应提交代码文件 的路径
    shutil.rmtree(dir_name)  # 递归删除路径及路径包含的文件


def get_data_count(problem_id):
    '''获得测试数据的个数信息'''
    full_path = os.path.join(config.data_dir, str(problem_id))  # 得到对应题目测试数据存放的文件夹的路径
    try:
        files = os.listdir(full_path)  # 得到此路径下的所有文件及文件夹（返回list）
    except OSError as e:
        logging.error(e)
        return 0
    count = 0
    for item in files:
        if item.endswith(".in") and item.startswith("data"):  # 判断该文件的前缀是否为'data'以及后缀是否为'.in'
            count += 1
    logging.info("数据个数：" + str(count))
    return count
