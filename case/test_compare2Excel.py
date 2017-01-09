# -*- coding:utf-8 -*-

import poster
import cookielib
import urllib2
import json
import urllib
import unittest

opener = poster.streaminghttp.register_openers()
opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

server_url = "http://172.16.26.36:8972/compare2excel"

class Test_Compare2Excel(unittest.TestCase):
    # 请求参数都填写
    def test_mysql_compare2Excel1(self):
        params = {'file1': open(r"F:\test\a1.xls", "rb"),'file2': open(r"F:\test\a2.xls", "rb")}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print result
        self.assertEqual(result['errno'], 0)
        self.assertEqual(result['errmsg'], '')
        self.assertEqual(result['url'][-3:], 'xls')

    # 文件1上传类型错误
    def test_mysql_compare2Excel2(self):
        params = {'file1': open(r"F:\test\sql.txt", "rb"),'file2': open(r"F:\test\a2.xls", "rb")}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print "result = ", result
        self.assertEqual(result['errno'], 1008)
        self.assertEqual(result['errmsg'], 'file type error')
        self.assertEqual(result['url'], '')

    # 文件2上传类型错误
    def test_mysql_compare2Excel3(self):
        params = {'file1': open(r"F:\test\a1.xls", "rb"),'file2': open(r"F:\test\sql.txt", "rb")}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print "result = ", result
        self.assertEqual(result['errno'], 1008)
        self.assertEqual(result['errmsg'], 'file type error')
        self.assertEqual(result['url'], '')

    # 文件1未上传
    def test_mysql_compare2Excel4(self):
        params = {'file1': '','file2': open(r"F:\test\a2.xls", "rb")}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print "result = ", result
        self.assertEqual(result['errno'], 1014)
        self.assertEqual(result['errmsg'], 'please upload excel')
        self.assertEqual(result['url'], '')

    # 文件2未上传
    def test_mysql_compare2Excel5(self):
        params = {'file1': open(r"F:\test\a1.xls", "rb"), 'file2': ''}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print "result = ", result
        self.assertEqual(result['errno'], 1014)
        self.assertEqual(result['errmsg'], 'please upload excel')
        self.assertEqual(result['url'], '')

    # 2文件1的行数少于文件2的行数
    def test_mysql_compare2Excel6(self):
        params = {'file1': open(r"F:\test\a1.xls", "rb"), 'file2': open(r"F:\test\a3.xls", "rb")}
        datagen, headers = poster.encode.multipart_encode(params)
        request = urllib2.Request(server_url, datagen, headers)
        result = eval(urllib2.urlopen(request).read())
        # print "result = ", result
        self.assertEqual(result['errno'], 1015)
        self.assertEqual(result['errmsg'], 'Line number is not consistent')
        self.assertEqual(result['url'], '')