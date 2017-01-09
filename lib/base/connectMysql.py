# -*- coding:utf-8 -*-
__author__ = 'ChenMei'

import pymysql as MySQLdb


class ConnectMysql:

    def __init__(self, db_host='127.0.0.1', port=3306, user='root', password=''):
        try:
            self.conn = MySQLdb.connect(host=db_host, port=port, user=user, passwd=password, charset='utf8')
            self.cur = self.conn.cursor()
        except Exception, e:
            print e

    def __del__(self):
        try:
            self.cur.close()
            self.conn.close()   # close connection
        except Exception, e:
            print e


if __name__ == '__main__':
    c = ConnectMysql(db_host='127.0.0.1', port=3306, user='root', password='123456')