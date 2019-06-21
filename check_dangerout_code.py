#!/usr/bin/env python
# coding=utf-8
import config, os, DBData


def check_dangerous_code(submit_id, language):
    if DBData.lans[language][0] in ['python2', 'python3']:
        code = open(
            os.path.join(config.work_dir, str(submit_id), "main.py")).readlines()  # 打开代码文件 读取所有行(直到结束符 EOF)并返回list
        support_modules = [
            're',  # 正则表达式
            'sys',  # sys.stdin
            'string',  # 字符串处理
            'scanf',  # 格式化输入
            'math',  # 数学库
            'cmath',  # 复数数学库
            'decimal',  # 数学库，浮点数
            'numbers',  # 抽象基类
            'fractions',  # 有理数
            'random',  # 随机数
            'itertools',  # 迭代函数
            'functools',
            # Higher order functions and operations on callable objects
            'operator',  # 函数操作
            'readline',  # 读文件
            'json',  # 解析json
            'array',  # 数组
            'sets',  # 集合
            'queue',  # 队列
            'types',  # 判断类型
        ]
        for line in code:
            if line.find('import') >= 0:  # line中包含'import'
                words = line.split()  # 切割字符串
                tag = 0  # 标记 只要一个被支持就行
                for w in words:
                    if w in support_modules:
                        tag = 1
                        break
                if tag == 0:
                    return False  # RE
        return True
    if DBData.lans[language][0] in ['gcc', 'g++']:
        try:
            code = open(os.path.join(config.work_dir, str(submit_id), "main.c")).read()  # 打开代码文件 读取所有（c）
        except:
            code = open(os.path.join(config.work_dir, str(submit_id), "main.cpp")).read()  # 打开代码文件 读取所有（c++）
        if code.find('system') >= 0:  # code中有'system'
            return False
        return True
    #    if language == 'java':
    #        code = file('/work/%s/Main.java'%solution_id).read()
    #        if code.find('Runtime.')>=0:
    #            return False
    #        return True
    if DBData.lans[language][0] == 'go':
        code = open(os.path.join(config.work_dir, str(submit_id), "main.go")).read()
        danger_package = [
            'os', 'path', 'net', 'sql', 'syslog', 'http', 'mail', 'rpc', 'smtp', 'exec', 'user',
        ]
        for item in danger_package:
            if code.find('"%s"' % item) >= 0:
                return False
        return True
