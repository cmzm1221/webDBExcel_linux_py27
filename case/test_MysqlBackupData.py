# -*- coding:utf-8 -*-
import unittest
import urllib,json
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lib.base.util import Util


server_url = "http://127.0.0.1:8972/mysql/backupData"


class Test_MysqlBackupData(unittest.TestCase):
    # config_file = os.path.dirname(__file__) + '/conf/base.conf'
    # server_url = Util.getConfig(config_file, "URL", 'baseURL')

    # 全部参数都填写,备份2个数据库
    def test_mysql_BackupData1(self):
        params = urllib.urlencode({
            'dbHost':"127.0.0.1",
            'port':3306,
            'user':'root',
            'password':'123456',
            'dbName':'mysql',
            'tableNameList':'db,user',
            'startPosition':0,
            'num':0})

        # print server_url
        url = server_url
        res = eval(urllib.urlopen(url, params).read())
        # print res
        self.assertEqual(res['errno'], 0)
        self.assertEqual(res['url'][-3:],'xls')

        # result1 = json.loads(res)
        # url1 = result1['url']
        # urllib.urlretrieve(url1, r'F:\test\bbbb.xls')

    # 端口号未填写
    def test_mysql_BackupData2(self):
        params = urllib.urlencode({
            'dbHost':"127.0.0.1",
            'user':'root',
            'password':'123456',
            'dbName':'mysql',
            'tableNameList':'db,user',
            'startPosition':0,
            'num':0})

        url = server_url
        res = eval(urllib.urlopen(url, params).read())
        # print res
        self.assertEqual(res['errno'], 0)
        self.assertEqual(res['url'][-3:],'xls')

    # 数据库密码未填写
    def test_mysql_BackupData3(self):
        params = urllib.urlencode({
            'dbHost':"127.0.0.1",
            'port':3307,
            'user':'root',
            'dbName':'mysql',
            'tableNameList':'db,user',
            'startPosition':0,
            'num':0})

        url = server_url
        res = eval(urllib.urlopen(url, params).read())
        self.assertEqual(res['errno'], 0)
        self.assertEqual(res['url'][-3:],'xls')

    # IP 填写错误
    def test_mysql_BackupData4(self):
        params = urllib.urlencode({
            'dbHost':"227.0.0.1",
            'port':3306,
            'user':'root',
            'password':'123456',
            'dbName':'mysql',
            'tableNameList':'db,user',
            'startPosition':0,
            'num':0})

        url = server_url
        res = eval(urllib.urlopen(url, params).read())
        # print res
        self.assertEqual(res['errno'], 1002)
        self.assertEqual(res['errmsg'],'connect mysql fail')

    # 数据库名不存在
    def test_mysql_BackupData5(self):
        params = urllib.urlencode({
            'dbHost':"127.0.0.1",
            'port':3306,
            'user':'root',
            'password':'123456',
            'dbName':'mysqlaaa',
            'tableNameList':'db,user',
            'startPosition':0,
            'num':0})

        url = server_url
        res = eval(urllib.urlopen(url, params).read())
        # print res
        self.assertEqual(res['errno'], 1004)
        self.assertEqual(res['errmsg'],'fail connect database')

    # 表名不存在
    def test_mysql_BackupData6(self):
        params = urllib.urlencode({
            'dbHost':"127.0.0.1",
            'port':3306,
            'user':'root',
            'password':'123456',
            'dbName':'mysql',
            'tableNameList':'db1, user',
            'startPosition':0,
            'num':0})

        url = server_url
        res = eval(urllib.urlopen(url, params).read())
        self.assertEqual(res['errno'], 1012)
        self.assertEqual(res['errmsg'],'execute sql fail')

    # 起始位置类型错误
    def test_mysql_BackupData7(self):
        params = urllib.urlencode({
            'dbHost':"127.0.0.1",
            'port':3306,
            'user':'root',
            'password':'123456',
            'dbName':'mysql',
            'tableNameList':'db, user',
            'startPosition':'a',
            'num':0})

        url = server_url
        res = eval(urllib.urlopen(url, params).read())
        # print res
        self.assertEqual(res['errno'], 999)
        self.assertEqual(res['url'], '')

    # 起始位数是负数
    def test_mysql_BackupData8(self):
        params = urllib.urlencode({
            'dbHost':"127.0.0.1",
            'port':3306,
            'user':'root',
            'password':'123456',
            'dbName':'mysql',
            'tableNameList':'db, user',
            'startPosition':-1,
            'num':0})

        url = server_url
        res = eval(urllib.urlopen(url, params).read())
        # print res
        self.assertEqual(res['errno'], 1001)
        self.assertEqual(res['errmsg'], 'invalid params')
        self.assertEqual(res['url'], '')

    # 查询条数是负数
    def test_mysql_BackupData9(self):
        params = urllib.urlencode({
            'dbHost':"127.0.0.1",
            'port':3306,
            'user':'root',
            'password':'123456',
            'dbName':'mysql',
            'tableNameList':'db, user',
            'startPosition':1,
            'num':-1})

        url = server_url
        res = eval(urllib.urlopen(url, params).read())
        # print res
        self.assertEqual(res['errno'], 1001)
        self.assertEqual(res['errmsg'], 'invalid params')
        self.assertEqual(res['url'], '')
