# -*- coding:utf-8 -*-
__author__ = 'chenmei'

import pymysql as MySQLdb
import xlwt
import os, time
import sys
reload(sys)
sys.setdefaultencoding('utf8')


sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from base.connectMysql import ConnectMysql
from base.writeToExcel import WriteToExcel


class RunSqlAndSaveExcel(ConnectMysql):
    server_data_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/data/fromServer/'
    conn = None
    cur = None

    # 执行sql语句、把结果保存在新excel 文档中，文件名称excel_result.xls
    def runSQLAndOnlySaveNewExcel(self, sql_file, mysqldb_db):
        res = {'errno':0, 'errmsg':'', 'save_excel_name':''}

        if self.cur == None:
            res['errno'] = 1002
            res['errmsg'] ='connect mysql fail'
            return res
        try:
            # __readSqlFileAndRunSQL 执行结果 {'errno':0, 'errmsg':'', 'res_value':{'num_nrows_run_sql':0, 'sql_run_result':''}}
            res_runsql = self.__readSqlFileAndRunSQL(sql_file, mysqldb_db)
            # print "res_runsql = ", res_runsql
            # print "save_excel_name = ", save_excel_name
            if res_runsql['errno'] == 0:
                num_nrows_run_sql = res_runsql['res_value']['num_nrows_run_sql']
                sql_run_result = res_runsql['res_value']['sql_run_result']
                save_excel_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.xls'
                we = WriteToExcel(save_excel_name)
                # we.saveNewExcel_noCompare 返回 {'errno':0, 'errmsg':''}
                res_saveExcel = we.saveNewExcel_noCompare(num_nrows_run_sql, sql_run_result)
                if res_saveExcel['errno'] != 0:
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
    def __readSqlFileAndRunSQL(self, sql_file, mysqldb_db):
        res = {'errno':0, 'errmsg':'', 'res_value':{'num_nrows_run_sql':0, 'sql_run_result':''}}
        # print sql_file
        # print mysqldb_db
        try:
            fp = open(sql_file, 'rb')   # 文件句柄
            sql = fp.read()
            fp.close()
        except:
            res['errno'] = 1013
            res['errmsg'] = 'read sql/txt file fail'
            return res

        try:
            if len(mysqldb_db) != 0:
                self.conn.select_db(mysqldb_db)
        except:
            res['errno'] = 1004
            res['errmsg'] = 'fail connect database'
            return res

        try:
            num_nrows_run_sql = self.cur.execute(sql)                # 返回结果的行数
            sql_run_result = self.cur.fetchall()                     # fetchall():接收全部的返回结果行
            self.conn.commit()
            res['res_value']['num_nrows_run_sql'] = num_nrows_run_sql
            res['res_value']['sql_run_result'] = sql_run_result
        except:
            res['errno'] = 1012
            res['errmsg'] = 'execute sql fail'
        finally:
            return res


if __name__ == '__main__':
    r = RunSqlAndSaveExcel(db_host='127.0.0.1', port=3307, user='root', password='')
    print r.runSQLAndOnlySaveNewExcel(r'E:\sql.txt', 'bi')
