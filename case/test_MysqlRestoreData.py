# -*- coding:utf-8 -*-

import poster
import cookielib
import urllib2
import unittest


opener = poster.streaminghttp.register_openers()
opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
server_url = 'http://127.0.0.1:8972/mysql/restoreData'


class Test_MysqlRestoreData(unittest.TestCase):
    # 全部参数都填写,只还原1个工作表
    def test_mysql_restoreData1(self):
        params = {'file': open(r"F:\test\c.xls", "rb"),
                  'dbHost':"127.0.0.1",
                  'port':3306,
                  'user':'root',
                  'password':'123456',
                  'sheetNameList':'test.user_info'}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print result
        self.assertEqual(result['errno'], 0)
        self.assertEqual(result['errmsg'], '')
        self.assertEqual(result['error_sheet_name_list'][0]['errno'], 0)
        self.assertEqual(result['error_sheet_name_list'][0]['errmsg'], '')
        self.assertEqual(result['error_sheet_name_list'][0]['error_sheet_name'], '')

    # 全部参数都填写,还原2个工作表
    def test_mysql_restoreData2(self):
        params = {'file': open(r"F:\test\c.xls", "rb"),
                  'dbHost':"127.0.0.1",
                  'port':3306,
                  'user':'root',
                  'password':'123456',
                  'sheetNameList':'test.user_info,test1.user_info2'}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print result
        self.assertEqual(result['errno'], 0)
        self.assertEqual(result['errmsg'], '')
        self.assertEqual(result['error_sheet_name_list'][0]['errno'], 0)
        self.assertEqual(result['error_sheet_name_list'][0]['errmsg'], '')
        self.assertEqual(result['error_sheet_name_list'][0]['error_sheet_name'], '')
        self.assertEqual(result['error_sheet_name_list'][1]['errno'], 0)
        self.assertEqual(result['error_sheet_name_list'][1]['errmsg'], '')
        self.assertEqual(result['error_sheet_name_list'][1]['error_sheet_name'], '')

    # 端口号未填写
    def test_mysql_restoreData3(self):
        params = {'file': open(r"F:\test\c.xls", "rb"),
                  'dbHost':"127.0.0.1",
                  'user':'root',
                  'password':'123456',
                  'sheetNameList':'test.user_info'}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print result
        self.assertEqual(result['errno'], 0)
        self.assertEqual(result['errmsg'], '')
        self.assertEqual(result['error_sheet_name_list'][0]['errno'], 0)
        self.assertEqual(result['error_sheet_name_list'][0]['errmsg'], '')
        self.assertEqual(result['error_sheet_name_list'][0]['error_sheet_name'], '')

    # 数据库连接失败：密码未填写
    def test_mysql_restoreData4(self):
        params = {'file': open(r"F:\test\c.xls", "rb"),
                  'dbHost':"127.0.0.1",
                  'port':3306,
                  'user':'root',
                  'sheetNameList':'test.user_info,test1.user_info2'}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print result
        self.assertEqual(result['errno'], 1002)
        self.assertEqual(result['errmsg'], 'connect mysql fail')
        self.assertEqual(result['error_sheet_name_list'], [])

    # 数据库连接失败：输入的工作表名称在 excel 中不存在
    def test_mysql_restoreData5(self):
        params = {'file': open(r"F:\test\c.xls", "rb"),
                  'dbHost':"127.0.0.1",
                  'port':3306,
                  'user':'root',
                  'password':'123456',
                  'sheetNameList':'test.user_info,test.user_info3,test1.user_info2'}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print result
        self.assertEqual(result['errno'], 0)
        self.assertEqual(result['errmsg'], '')
        self.assertEqual(result['error_sheet_name_list'][0]['errno'], 0)
        self.assertEqual(result['error_sheet_name_list'][2]['errno'], 0)
        self.assertEqual(result['error_sheet_name_list'][1]['errno'], 1010)
        self.assertEqual(result['error_sheet_name_list'][1]['errmsg'], 'sheetName not exist')
        self.assertEqual(result['error_sheet_name_list'][1]['error_sheet_name'], 'test.user_info3')

    # 数据库连接失败：输入的工作表名称的数据库在 mysql 中不存在
    def test_mysql_restoreData6(self):
        params = {'file': open(r"F:\test\c.xls", "rb"),
                  'dbHost':"127.0.0.1",
                  'port':3306,
                  'user':'root',
                  'password':'123456',
                  'sheetNameList':'test2.user_info'}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print result
        self.assertEqual(result['errno'], 0)
        self.assertEqual(result['errmsg'], '')
        self.assertEqual(result['error_sheet_name_list'][0]['errno'], 1004)
        self.assertEqual(result['error_sheet_name_list'][0]['errmsg'], 'fail connect database')
        self.assertEqual(result['error_sheet_name_list'][0]['error_sheet_name'], 'test2.user_info')

    # 数据库连接失败：输入的工作表名称的表在 mysql 中不存在
    def test_mysql_restoreData7(self):
        params = {'file': open(r"F:\test\c.xls", "rb"),
                  'dbHost':"127.0.0.1",
                  'port':3306,
                  'user':'root',
                  'password':'123456',
                  'sheetNameList':'test.user_info2'}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print result
        self.assertEqual(result['errno'], 0)
        self.assertEqual(result['errmsg'], '')
        self.assertEqual(result['error_sheet_name_list'][0]['errno'], 1011)
        self.assertEqual(result['error_sheet_name_list'][0]['errmsg'], 'table not exist')
        self.assertEqual(result['error_sheet_name_list'][0]['error_sheet_name'], 'test.user_info2')

    # 上传的excel 文件类型错误
    def test_mysql_restoreData8(self):
        params = {'file': open(r"F:\test\sql.txt", "rb"),
                  'dbHost':"127.0.0.1",
                  'port':3306,
                  'user':'root',
                  'password':'123456',
                  'sheetNameList':'test.user_info'}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print result
        self.assertEqual(result['errno'], 1008)
        self.assertEqual(result['errmsg'], 'file type error')
        self.assertEqual(result['error_sheet_name_list'], [])

    # 执行sql 语句失败，excel 文档中表字段在实际数据库中不存在
    def test_mysql_restoreData9(self):
        params = {'file': open(r"F:\test\c.xls", "rb"),
                  'dbHost':"127.0.0.1",
                  'port':3306,
                  'user':'root',
                  'password':'123456',
                  'sheetNameList':'test.user_info1'}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print result
        self.assertEqual(result['errno'], 0)
        self.assertEqual(result['errmsg'], '')
        self.assertEqual(result['error_sheet_name_list'][0]['errno'], 1009)
        self.assertEqual(result['error_sheet_name_list'][0]['errmsg'], 'execute mysql fail')
        self.assertEqual(result['error_sheet_name_list'][0]['error_sheet_name'], 'test.user_info1')

    # 文件未上传
    def test_mysql_restoreData10(self):
        params = {'file': '',
                  'dbHost':"127.0.0.1",
                  'port':3306,
                  'user':'root',
                  'password':'123456',
                  'sheetNameList':'test.user_info'}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print result
        self.assertEqual(result['errno'], 1014)
        self.assertEqual(result['errmsg'], 'please upload excel')
        self.assertEqual(result['url'], '')