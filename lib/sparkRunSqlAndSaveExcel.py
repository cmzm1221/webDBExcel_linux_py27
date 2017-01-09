# -*- coding:utf-8 -*-
__author__ = 'chenmei'


import subprocess
import os, time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from base.writeToExcel import WriteToExcel
from base.connectSpark import ConnectSpark


class RunSqlAndSaveExcel(ConnectSpark):
    server_data_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/data/fromServer/'

    # 执行sql语句、把结果保存在新excel 文档中，文件名称excel_result.xls
    def runSQLAndOnlySaveNewExcel(self, sql_file):
        res = {'errno':0, 'errmsg':'', 'save_excel_name':''}

        if self.conn == None:
            res['errno'] = 1002
            res['errmsg'] ='connect spark fail'
            return res

        try:
            # __readSqlFileAndRunSQL 执行结果 {'errno':0, 'errmsg':'', 'res_value':{'num_nrows_run_sql':0, 'sql_run_result':''}}
            res_runsql = self.spark_readSqlFileAndRunSQL(sql_file)
            # print "res_runsql = ", res_runsql
            # print "save_excel_name = ", save_excel_name
            if res_runsql['errno'] == 0:
                num_nrows_run_sql = res_runsql['res_value']['num_nrows_run_sql']
                sql_run_result = res_runsql['res_value']['sql_run_result']
                save_excel_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.xls'
                we = WriteToExcel(save_excel_name)
                # we.saveNewExcel_noCompare 返回 {'errno':0, 'errmsg':''}
                res_saveExcel = we.saveNewExcel_noCompare(num_nrows_run_sql, sql_run_result)
                if res_saveExcel['errno'] <> 0:
                    res['errno'] = res_saveExcel['errno']
                    res['errmsg'] = res_saveExcel['errmsg']
                    return res
                res['save_excel_name'] = save_excel_name
            else:
                res['errno'] = res_runsql['errno']
                res['errmsg'] = res_runsql['errmsg']
        except Exception, e:
            res['errno'] = 999
            res['errmsg'] = str(e)
        finally:
            return res

    # 读取sql语句的文件并执行,返回执行查询结果(行数和内容)
    def spark_readSqlFileAndRunSQL(self, sql_file):
        res = {'errno':0, 'errmsg':'', 'res_value':{'num_nrows_run_sql':0, 'sql_run_result':''}}
        try:
            fp = open(sql_file, 'rb')   # 文件句柄
            sql = fp.read()
            fp.close()
        except:
            res['errno'] = 1013
            res['errmsg'] = 'read sql/txt file fail'
            return res

        try:
            values = self.query(sql)   # 接收全部的返回结果行
            # print'values=', values
            rows = len(values)         # 返回结果的行数
            res['res_value']['num_nrows_run_sql'] = rows
            res['res_value']['sql_run_result'] = values
        except:
            res['errno'] = 1012
            res['errmsg'] = 'execute sql fail'
        finally:
            return res

    # 执行2个sql 文件，并进行对比，把结果保存为excel
    def spark_runSQLAndCompareAndSaveNewExcel(self, sql_file1, sql_file2, query_data):
        res = {'errno':0, 'errmsg':'', 'save_excel_name':''}

        if self.conn == None:
            res['errno'] = 1002
            res['errmsg'] ='connect spark fail'
            return res

        try:
            # spark_readSqlFileAndRunSQL 执行结果 {'errno':0, 'errmsg':'', 'res_value':{'num_nrows_run_sql':0, 'sql_run_result':''}}
            self.queryDate(query_data)

            res_runsql1 = self.spark_readSqlFileAndRunSQL(sql_file1)    # 第 1 个sql 查询结果
            res_runsql2 = self.spark_readSqlFileAndRunSQL(sql_file2)    # 第 2 个sql 查询结果
            # print "res_runsql = ", res_runsql
            # print "save_excel_name = ", save_excel_name
            if res_runsql1['errno'] == 0 and res_runsql2['errno'] == 0:
                num_nrows_run_sql1 = res_runsql1['res_value']['num_nrows_run_sql']
                num_nrows_run_sql2 = res_runsql2['res_value']['num_nrows_run_sql']
                sql_run_result1 = res_runsql1['res_value']['sql_run_result']
                sql_run_result2 = res_runsql2['res_value']['sql_run_result']
                save_excel_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.xls'
                we = WriteToExcel(save_excel_name)
                # we.saveNewExcel_noCompare 返回 {'errno':0, 'errmsg':''}
                res_saveExcel = we.saveNewExcel_Compare(buffer_excel_num=num_nrows_run_sql1,
                                                        buffer_excel_values=sql_run_result1,
                                                        ods_excel_num=num_nrows_run_sql2,
                                                        ods_excel_values=sql_run_result2)
                if res_saveExcel['errno'] <> 0:
                    res['errno'] = res_saveExcel['errno']
                    res['errmsg'] = res_saveExcel['errmsg']
                    return res
                res['save_excel_name'] = save_excel_name
            else:
                res['errno'] = res_runsql1['errno']
                res['errmsg'] = res_runsql1['errmsg']
                res['errno'] = res_runsql2['errno']
                res['errmsg'] = res_runsql2['errmsg']
        except Exception, e:
            res['errno'] = 999
            res['errmsg'] = str(e)
        finally:
            return res

if __name__ == '__main__':
    # r = RunSqlAndSaveExcel(db_host='192.168.104.20', port=15000, user='spark', password='', database='policy_dw', authMechanism='PLAIN')
    # print r.runSQLAndOnlySaveNewExcel(r'/root/chenmei/spark.sql')
    #
    # buffer_excel_num = 2
    # ods_excel_num = 2
    # buffer_excel_values = [[u'1a1', u'1b1', u'1c1'], [u'1a2', u'1b2', u'1c2']]
    # ods_excel_values    = [[u'2a1', u'2b1', u'2c1'], [u'2a2', u'2b2', u'2c2']]
    # w = WriteToExcel('cmtest.xls')
    # print w.saveNewExcel_Compare(buffer_excel_num, buffer_excel_values, ods_excel_num, ods_excel_values)
    # # print w.saveNewExcel_noCompare(buffer_excel_num, buffer_excel_values)


    buffer_excel_num = 3
    ods_excel_num = 3
    buffer_excel_values = [[u'1a1', u'1b1', u'1c1', u'1d1', u'1e1'], [u'1a2', u'1b2', u'1c2', u'1d2', u'1e2'], [u'1a3', u'1b3', u'1c3', u'1d3', u'1e3']]
    ods_excel_values    = [[u'1a1', u'2b1', u'1c1', u'2d1', u'2e1'], [u'2a2', u'1b2', u'2c2', u'2d2', u'2e2'], [u'2a3', u'2b3', u'2c3', u'2d3', u'2e3']]
    w = WriteToExcel('cmtest.xls')
    print w.saveNewExcel_Compare(buffer_excel_num, buffer_excel_values, ods_excel_num, ods_excel_values)

