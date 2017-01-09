# -*- coding:utf-8 -*-
__author__ = 'ChenMei'
"""
本脚本功能：备份、还原数据库
1、方法 restoreDatabase_Mysql 还原数据库；
2、方法 backupDatabase_Mysql 备份数据库
"""

import pymysql as MySQLdb
import xlrd, sys, os

sys.path.append(os.path.dirname(__file__))
from base.connectMysql import ConnectMysql


class MysqlRestoreAndBackup(ConnectMysql):
    conn = None
    cur = None

    # 还原数据库，读取excel文件
    def restoreDatabase_Mysql(self, excel_name, sheet_name):
        # print excel_name, sheet_name
        res = {'errno':0, 'errmsg':'', 'error_sheet_name':''}
        if self.cur == None:
            res['errno'] = 1002
            res['errmsg'] ='connect mysql fail'
            return res

        try:
            wbk = xlrd.open_workbook(excel_name)

            try:
                st = wbk.sheet_by_name(sheet_name)
            except:
                res['errno'] = 1010
                res['errmsg'] ='sheetName not exist'   # 输入的工作表名称在excel 文档中不存在
                res['error_sheet_name'] = sheet_name
                return res

            st_name = st.name
            try:
                data_name = st_name.split(".")[0]
                table_name = st_name.split(".")[1]
                self.conn.select_db(data_name)                  # 连接到数据库
            except:
                res['errno'] = 1004
                res['errmsg'] = 'fail connect database'
                res['error_sheet_name'] = st_name
                return res
            try:
                self.cur.execute('TRUNCATE table ' + table_name + ';')    # 先把表清空
            except:
                res['errno'] = 1011
                res['errmsg'] = 'table not exist'
                res['error_sheet_name'] = st_name
                return res
            try:
                table_title = ','.join(st.row_values(0))        # 表字段列表
                num_nrows_value = st.nrows-1                    # 获取要插入的数据总共有几行
                num_ncols_value = st.ncols                      # 获取要插入的数据总共有几列

                value = []
                for i in range(1, st.nrows):
                    value.append(st.row_values(i))

                for i in range(num_nrows_value):
                    for j in range(num_ncols_value):
                        if value[i][j] == "":
                            value[i][j] = None

                prams_num = "%s," * st.ncols
                prams_num = prams_num[0:-1]
                self.cur.executemany("insert into " + table_name + "(" + table_title + ")" + " values(" + prams_num + ")", value)
                self.conn.commit()
            except:
                res['errno'] = 1009
                res['errmsg'] = 'execute mysql fail'
                res['error_sheet_name'] = st_name
            return res

        except Exception, e:
            # print e
            res['errno'] = 999
            res['errmsg'] = str(e)
            return res

    # 备份数据库
    # db 数据库, table 表, start_position 查询的起始位置, num 查询条数
    def backupDatabase_Mysql(self, db_name, table_name, start_position=0, num=0):
        res = {'errno':0, 'errmsg':'', 'result_values':''}

        if self.cur == None:
            res['errno'] = 1002
            res['errmsg'] ='connect mysql fail'
            return res
        try:
            # __readDataBase 返回  {'errno':0, 'errmsg':'', 'result_values':''}
            res_readDataBase = self.__readDataBase(db_name, table_name, start_position, num)
            if res_readDataBase['errno'] == 0:
                res_value = res_readDataBase['result_values']
                res['result_values'] = res_value
            else:
                res['errno'] = res_readDataBase['errno']
                res['errmsg'] = res_readDataBase['errmsg']
            return res

        except Exception, e:
            print e

    # 读取mysql 数据库，返回表字段数、表字段名、数据条数、数据
    def __readDataBase(self, db_name, table_name, begin_position=0, select_num=0):
        res = {'errno':0, 'errmsg':'', 'result_values':''}

        sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '" + table_name \
              + "' and table_schema = '" + db_name + "';"        # 获取表字段名
        # print "db_name=", db_name
        # print "table_name=", table_name
        # print "begin_position = ", begin_position
        # print "select_num = ", select_num
        try:
            num_ncols = self.cur.execute(sql)                        # 返回表字段个数
            table_title = self.cur.fetchall()                        # fetchall():接收全部的返回结果行
            try:
                self.conn.select_db(db_name)                             # 切换到数据库
            except:
                res['errno'] = 1004
                res['errmsg'] = 'fail connect database'
                return res
            try:
                if select_num == 0:
                    sql_selTableData = 'select * from ' + table_name + ';'
                else:
                    sql_selTableData = 'select * from ' + table_name + ' limit ' + str(begin_position) + ',' + str(select_num) + ';'
                num_selTableData = self.cur.execute(sql_selTableData)    # 返回条目数量
                values = self.cur.fetchall()
                res_values = {}
                res_values['num_ncols'] = num_ncols
                res_values['table_title'] = table_title
                res_values['num_selTableData'] = num_selTableData
                res_values['values'] = values
                res['result_values'] = res_values
            except:
                res['errno'] = 1012
                res['errmsg'] = 'execute sql fail'
            return res
        except Exception, e:
            # print "执行sql 语句错误，检查数据库连接信息：IP、PORT、user、password、dbname"
            res['errno'] = 999
            res['errmsg'] = str(e)
            return res


if __name__ == "__main__":
    m = MysqlRestoreAndBackup()
    print m.backupDatabase_Mysql('mysql', 'db', 0, 0)