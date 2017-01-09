# -*- coding:utf-8 -*-
__author__ = 'ChenMei'
import sys, os, time
from flask import Flask, request

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lib.sparkRunSqlAndSaveExcel import RunSqlAndSaveExcel
from lib.base.util import Util

class ToWeb_SparkRunSqlAndCompareAndSaveExcel():
    base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    server_data_dir = base_dir + '/data/fromServer/'
    client_data_dir = base_dir + '/data/fromClient/'
    config_file = base_dir + '/conf/base.conf'
    ip = Util.getConfig(config_file, 'serverInfo', "ip")
    port = Util.getConfig(config_file, 'serverInfo', "port")

    # 执行sql 文件，并把执行结果保存在excel 中, 接收请求信息入口
    def toWeb_SparkRunSqlAndCompareAndSaveExcel(self, sqlFile1_name, sqlFile2_name):
        res = {'errno':0, 'errmsg':'', 'url':''}
        try:
            db_host = request.form.get('dbHost')
            port = request.form.get('port')
            user = request.form.get('user')
            password = request.form.get('password')
            db_name = request.form.get('dbName')
            query_data = request.form.get('query_date')

            if db_host==None or user==None or sqlFile1_name==None or sqlFile2_name==None:
                res['errno'] = 1001
                raise Exception('invalid params')
            if port:
                port = int(port)
            else:
                port = 15000

            if password:
                pass
            else:
                password = ''

            if db_name:
                pass
            else:
                db_name = 'default'

            if query_data:
                pass
            else:
                query_data = time.strftime('%Y%m%d', time.localtime(time.time()-86400))

            if sqlFile1_name[-3:] in ('sql', 'txt') and sqlFile2_name[-3:] in ('sql', 'txt'):   # 判断文件类型
                sql1_path_name = self.client_data_dir + sqlFile1_name
                sql2_path_name = self.client_data_dir + sqlFile2_name
                rqse = RunSqlAndSaveExcel(db_host=db_host, port=port, user=user, password=password, database=db_name)
                # rqse.runSQLAndOnlySaveNewExcel 返回结果 {'errno':0, 'errmsg':'', 'save_excel_name':''}
                res_rssw = rqse.spark_runSQLAndCompareAndSaveNewExcel(sql1_path_name, sql2_path_name, query_data)
                print res_rssw
                # print "res_rssw = ",res_rssw

                if res_rssw['errno'] == 0:
                    res_url = "http://" + self.ip + ":" + self.port + "/excel/download/" + res_rssw['save_excel_name']
                    res['url'] = res_url
                else:
                    res['errno'] = res_rssw['errno']
                    res['errmsg'] = res_rssw['errmsg']
            else:
                res['errno'] = 1008
                res['errmsg'] = 'file type error'
        except Exception, e:
            res['errno'] = 999
            res['errmsg'] = str(e)
        return res