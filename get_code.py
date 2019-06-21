#!/usr/bin/env python
# coding=utf-8
import protect, logging, os, config, codecs, DBData


def get_code(submit_id, problem_id, language):
    '''从数据库获取代码并写入work目录下对应的文件'''
    # file_name = {
    #     "gcc": "main.c",
    #     "g++": "main.cpp",
    #     "java": "Main.java",
    #     'ruby': "main.rb",
    #     "perl": "main.pl",
    #     "pascal": "main.pas",
    #     "go": "main.go",
    #     "lua": "main.lua",
    #     'python2': 'main.py',
    #     'python3': 'main.py',
    #     "haskell": "main.hs"
    # }
    lans = DBData.lans
    select_code_sql = "select code from django_web_submitproblem where submit_id=" + str(
        submit_id)
    feh = protect.run_sql(select_code_sql)
    if feh is not None:
        try:
            logging.info("I get code!")
            code = feh[0][0]
        except:
            logging.error("1 cannot get code of runid %s" % submit_id)
            return False
    else:
        logging.error("feh is None")
        logging.error("2 cannot get code of runid %s" % submit_id)
        return False
    try:  # 在work_dir下生成以solution_id为名字的文件夹
        logging.info("尝试创建提交文件夹")
        work_path = os.path.join(config.work_dir, str(submit_id))
        protect.low_level()
        os.mkdir(work_path, 0o777)
    except OSError as e:
        logging.info("创建提交文件夹失败")
        if str(e).find("exist") > 0:  # 文件夹已经存在
            pass
        else:
            logging.error(e)
            return False
    try:  # 生成空文件 后缀由所选语言决定
        real_path = os.path.join(
            config.work_dir,
            str(submit_id),
            lans[language][1])
    except KeyError as e:
        logging.error(e)
        return False
    try:  # 将代码填入放生成的空文件内
        protect.low_level()
        f = codecs.open(real_path, 'w')
        try:
            f.write(code)
        except:
            logging.error("%s not write code to file" % submit_id)
            f.close()
            return False
        f.close()
    except OSError as e:
        logging.error(e)
        return False
    return True
