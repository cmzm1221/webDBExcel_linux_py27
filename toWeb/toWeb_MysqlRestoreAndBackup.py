# -*- coding:utf-8 -*-
__author__ = 'ChenMei'
import sys, os, time
from flask import Flask, request

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lib.mysqlRestoreAndBackup import MysqlRestoreAndBackup
from lib.base.writeToExcel import WriteToExcel
from lib.base.util import Util

app = Flask(__name__)


class ToWeb_MysqlRestoreAndBackup():
    server_data_dir = os.path.dirname(os.path.dirname(__file__)) + '/data/fromServer/'
    client_data_dir = os.path.dirname(os.path.dirname(__file__)) + '/data/fromClient/'
    config_file = os.path.dirname(os.path.dirname(__file__)) + '/conf/base.conf'
    ip = Util.getConfig(config_file, 'serverInfo', "ip")
    port = Util.getConfig(config_file, 'serverInfo', "port")

    # 备份数据库，接收请求信息入口
    def toWeb_mysqlBackupData(self):
        res = {'errno':0, 'errmsg':'', 'url':''}
        try:
            db_host = request.form.get('dbHost')
            port = request.form.get('port')
            user = request.form.get('user')
            password = request.form.get('password')
            db_name = request.form.get('dbName')
            table_name_list = request.form.get('tableNameList')
            start_position = request.form.get('startPosition')
            num = request.form.get('num')

            if start_position:
                start_position = int(start_position)
            else:
                start_position = 0

            if num:
                num = int(num)
            else:
                num = 0

            if db_host==None or user==None or db_name==None or table_name_list==None or start_position<0 or num<0:
                # print db_host
                # print port
                # print user
                # print password
                # print db_name
                # print table_name_list
                # print start_position
                # print num

                res['errno'] = 1001
                res['errmsg'] = 'invalid params'
                return res


            if port:
                port = int(port)
            else:
                port = 3306

            if password:
                pass
            else:
                password = ''

            # mysqlBackup 返回 {'errno':0, 'errmsg':'', 'res_url':''}
            res_mysqlbackup = self.mysqlBackup(db_host=db_host, port=port, user=user, password=password, db_name=db_name,
                                        table_name_list=table_name_list, start_position=start_position, num=num)

            if res_mysqlbackup['errno'] == 0:
                res['url'] = res_mysqlbackup['res_url']
            else:
                res['errno'] = res_mysqlbackup['errno']
                res['errmsg'] = res_mysqlbackup['errmsg']
        except Exception, e:
            print "ToWeb_MysqlRestoreAndBackup.toWeb_mysqlBackupData error message = ", e
            if res['errno'] == 0:
                res['errno'] = 999
            res['errmsg'] = str(e)
            print "res = ", res
        return res

    # 备份 mysql 数据库支持多个个表
    def mysqlBackup(self, db_host, user, db_name, table_name_list, port=3306, password='', start_position=0, num=0):
        res = {'errno':0, 'errmsg':'', 'res_url':''}
        file_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.xls'
        tableNameList = table_name_list.split(',')
        try:
            w = WriteToExcel(file_name)
            for table_name in tableNameList:
                    m = MysqlRestoreAndBackup(db_host, port, user, password)
                    # m.backupDatabase_Mysql 返回值为 {'errno':0, 'errmsg':'', 'result_values':''}
                    res_executemysql = m.backupDatabase_Mysql(db_name, table_name, start_position, num)
                    if res_executemysql['errno'] == 0:
                        sheet_name = db_name + "." + table_name
                        num_ncols = res_executemysql['result_values']['num_ncols']
                        table_title = res_executemysql['result_values']['table_title']
                        num_selTableData = res_executemysql['result_values']['num_selTableData']
                        values = res_executemysql['result_values']['values']
                        w.writeExcel(sheet_name, table_title, num_ncols, num_selTableData, values)    # 保存到excel文件
                        res_url = "http://" + self.ip + ":" + self.port + "/excel/download/" + file_name
                        res['res_url'] = res_url
                    else:
                        res['errno'] = res_executemysql['errno']
                        res['errmsg'] = res_executemysql['errmsg']
        except Exception, e:
            res['errno'] = 999
            res['errmsg'] = str(e)
        finally:
            return res

    # 还原数据库，接收请求信息入口
    def toWeb_mysqlRestoreData(self, fileName):
        res = {'errno':0, 'errmsg':'', 'error_sheet_name_list':[]}
        try:
            db_host = request.form.get('dbHost')
            port = request.form.get('port')
            user = request.form.get('user')
            password = request.form.get('password')
            sheet_name_list = request.form.get('sheetNameList')

            if db_host == None or user == None or fileName == None or sheet_name_list == '':
                res['errno'] = 1001
                res['errmsg'] = 'invalid params'
                return res
            if fileName[-3:] <> 'xls' and fileName[-4:] <> 'xlsx':
                res['errno'] = 1008
                res['errmsg'] = 'file type error'
                return res

            if port:
                port = int(port)
            else:
                port = 3306

            if password:
                pass
            else:
                password = ''

            file_path_name = self.client_data_dir + fileName
            #  self.mysqlRestoreData 返回res = {'errno':0, 'errmsg':'', 'error_sheet_name':[]}
            med = self.mysqlRestoreData(db_host=db_host, port=port, user=user, password=password,
                                        file_path_name=file_path_name, sheet_name_list=sheet_name_list)
            if med['errno'] == 0:
                res['error_sheet_name_list'] = med['error_sheet_name']

            if med['errno'] <> 0:
                res['errno'] = med['errno']
                res['errmsg'] = med['errmsg']

        except Exception, e:
            res['errno'] = 999
            res['errmsg'] = str(e)
        finally:
            return res

    # 还原数据库
    def mysqlRestoreData(self, db_host, port, user, password, file_path_name,  sheet_name_list):
        res = {'errno':0, 'errmsg':'', 'error_sheet_name':[]}
        try:
            m = MysqlRestoreAndBackup(db_host, port, user, password)
            for sheet_name in (sheet_name_list.split(",")):    # 对每个工作表遍历
                res_every_do = m.restoreDatabase_Mysql(file_path_name, sheet_name)   # 返回结果 {'errno':0, 'errmsg':'', 'error_sheet_name':''}
                if res_every_do['errno'] == 1002 or res_every_do['errno'] == 999:
                    res['errno'] = res_every_do['errno']
                    res['errmsg'] = res_every_do['errmsg']
                    break
                else:
                    res['error_sheet_name'].append(res_every_do)
                    continue
        except Exception, e:
            res['errno'] = 999
            res['errmsg'] = str(e)
        finally:
            return res


if __name__ == "__main__":
    t = ToWeb_MysqlRestoreAndBackup()
    res = t.mysqlBackup(db_host="227.0.0.1", user="root", db_name="test", table_name_list="user_info", password="123456", start_position=0, num=0)
    print "res = ", res
    # print t.mysqlRestoreData("127.0.0.1",  3306, "root", "123456", r"E:\work_python\puhui\webDBExcel\data\fromServer\c.xls", "test.user_info,test1.user_info2")