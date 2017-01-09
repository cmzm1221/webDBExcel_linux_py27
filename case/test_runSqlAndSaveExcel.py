# -*- coding:utf-8 -*-

import poster
import cookielib
import urllib2
import json
import urllib
import unittest

opener = poster.streaminghttp.register_openers()
opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

server_url = "http://127.0.0.1:8972/mysql/runSqlAndSaveExcel"


class Test_RunSqlAndSaveExcel(unittest.TestCase):
    # 请求参数都填写
    def test_mysql_runSqlAndSaveExcel1(self):
        params = {'file': open(r"F:\test\sql.txt", "rb"),
                      'dbHost':"127.0.0.1",
                      'port':3306,
                      'user':'root',
                      'password':'123456',
                      'dbName':'test'
                    }
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print "result = ", result
        self.assertEqual(result['errno'], 0)
        self.assertEqual(result['errmsg'], '')
        self.assertEqual(result['url'][-3:], 'xls')
        # result1 = json.loads(result)
        # url1 = result1['url']
        # urllib.urlretrieve(url1, r'F:\test\aaaa.xls')

    # 数据库未填写
    def test_mysql_runSqlAndSaveExcel2(self):
        params = {'file': open(r"F:\test\sql.txt", "rb"),
                      'dbHost':"127.0.0.1",
                      'port':3306,
                      'user':'root',
                      'password':'123456'
                    }
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        self.assertEqual(result['errno'], 0)
        self.assertEqual(result['errmsg'], '')
        self.assertEqual(result['url'][-3:], 'xls')
        # result1 = json.loads(result)
        # url1 = result1['url']
        # urllib.urlretrieve(url1, r'F:\test\b.xls')

    # 端口号未填写填写
    def test_mysql_runSqlAndSaveExcel3(self):
        params = {'file': open(r"F:\test\sql.txt", "rb"),
                      'dbHost':"127.0.0.1",
                      'user':'root',
                      'password':'123456',
                      'dbName':'test'
                    }
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        self.assertEqual(result['errno'], 0)
        self.assertEqual(result['errmsg'], '')
        self.assertEqual(result['url'][-3:], 'xls')

    # 密码未填写填写
    def test_mysql_runSqlAndSaveExcel4(self):
        params = {'file': open(r"F:\test\sql.txt", "rb"),
                      'dbHost':"127.0.0.1",
                      'user':'root',
                      'port':3306,
                      'dbName':'test'
                    }
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print result
        self.assertEqual(result['errno'], 1002)
        self.assertEqual(result['errmsg'], 'connect mysql fail')
        self.assertEqual(result['url'], '')

    # sql 文件中，数据库连接失败
    def test_mysql_runSqlAndSaveExcel5(self):
        params = {'file': open(r"F:\test\sql2.txt", "rb"),
                      'dbHost':"127.0.0.1",
                      'user':'root',
                      'password':'123456',
                      'port':3306,
                      'dbName':'test'
                    }
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print result
        self.assertEqual(result['errno'], 1012)
        self.assertEqual(result['errmsg'], 'execute sql fail')
        self.assertEqual(result['url'], '')

    # 上传的文件类型错误
    def test_mysql_runSqlAndSaveExcel6(self):
        params = {'file': open(r"F:\test\c.xls", "rb"),
                      'dbHost':"127.0.0.1",
                      'user':'root',
                      'password':'123456',
                      'port':3306,
                      'dbName':'test'
                    }
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print result
        self.assertEqual(result['errno'], 1008)
        self.assertEqual(result['errmsg'], 'file type error')
        self.assertEqual(result['url'], '')

    # 文件未上传
    def test_mysql_runSqlAndSaveExcel7(self):
        params = {'file': '',
                      'dbHost':"127.0.0.1",
                      'user':'root',
                      'password':'123456',
                      'port':3306,
                      'dbName':'test'
                    }
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print result
        self.assertEqual(result['errno'], 1014)
        self.assertEqual(result['errmsg'], 'please upload excel')
        self.assertEqual(result['url'], '')
