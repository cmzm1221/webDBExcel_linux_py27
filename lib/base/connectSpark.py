# -*- coding:utf-8 -*-
__author__ = 'ChenMei'

import pyhs2


class ConnectSpark:
    conn = None
    cur = None

    def __init__(self, db_host='192.168.104.20', port=15000, user='spark', password='', database='default', authMechanism='PLAIN'):
        try:
            self.conn = pyhs2.connect(host=db_host, port=port, user=user, password=password, database=database, authMechanism=authMechanism,)  # create connection to hive server2
        except Exception, e:
            print e

    def queryDate(self, query_data):
        try:
            with self.conn.cursor() as cursor:
                toDate_sql = "set dt = '" + str(query_data) + "'"    # set dt = '20160508';
                cursor.execute(toDate_sql)
        except Exception, e:
            print e

    def query(self, sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetch()
        except Exception, e:
            print e

    def __del__(self):
        try:
            self.conn.close()   # close connection
        except Exception, e:
            print e


if __name__ == '__main__':
    queryDate = '20160509'
    # sql = "select * from address_list limit 2"
    sql = "select 'ods.ods_openline_credit_app_verify', count(1) from ods.ods_openline_credit_app_verify	where dt= ${hiveconf:dt} "
    hive_client = ConnectSpark(db_host='192.168.104.20', port=15000, user='spark', password='', database='policy_dw', authMechanism='PLAIN')
    hive_client.queryDate(queryDate)
    values = hive_client.query(sql)
    print 'values=',values
