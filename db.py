#!/usr/bin/env python
# coding=utf-8

import time
import config
import MySQLdb
import logging
import types


def run_sql(sql):
    '''执行sql语句,并返回结果'''
    con = None
    while True:
        try:
            con = MySQLdb.connect(config.db_host, config.db_user, config.db_password,
                                  config.db_name, charset=config.db_charset)
            break
        except:
            logging.error('Cannot connect to database,trying again')
            time.sleep(1)
    cur = con.cursor()
    try:
        if type(sql) == type(""):
            cur.execute(sql)
        elif type(sql) == type([]):
            for i in sql:
                cur.execute(i)
    except MySQLdb.OperationalError as e:
        logging.error(e)
        cur.close()
        con.close()
        return False
    con.commit()
    data = cur.fetchall()
    cur.close()
    con.close()
    return data


def InsertData(sql, data):
    while True:
        try:
            con = MySQLdb.connect(config.db_host, config.db_user, config.db_password,
                                  config.db_name, charset=config.db_charset)
            break
        except:
            logging.error('Cannot connect to database,trying again')
            time.sleep(1)
    cur = con.cursor()
    try:
        res = cur.execute(sql, data)
    except Exception as e:
        con.rollback()
        logging.error(e)
        cur.close()
        con.close()
        return False
    con.commit()
    return res
