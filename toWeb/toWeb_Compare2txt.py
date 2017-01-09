# -*- coding:utf-8 -*-
__author__ = 'ChenMei'
import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lib.base.util import Util

class ToWeb_Compare2Txt():
    base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    server_data_dir = base_dir + '/data/fromServer/'
    client_data_dir = base_dir + '/data/fromClient/'
    config_file = base_dir + '/conf/base.conf'
    ip = Util.getConfig(config_file, 'serverInfo', "ip")
    port = Util.getConfig(config_file, 'serverInfo', "port")

    # 对比2个txt，找出交集、并集、差集
    def toWeb_Compare2txt(self, txt1_name, txt2_name, type):
        res = {'errno':0, 'errmsg':'', 'url':''}
        try:
            if (txt1_name[-3:] == 'txt') and (txt2_name[-3:] == 'txt'):  # 判断文件类型
                    txt1_path_name = self.client_data_dir + txt1_name
                    txt2_path_name = self.client_data_dir + txt2_name
                    # compare2TxtAndSaveNewTxt  返回的执行结果 {'errno':0, 'errmsg':'', 'file_name':''}
                    saveTxt_name = self.compare2TxtAndSaveNewTxt(txt1=txt1_path_name, txt2=txt2_path_name, type=type)
                    if saveTxt_name['errno'] ==0:
                        res_url = "http://" + self.ip + ":" + self.port + "/excel/download/" + saveTxt_name['file_name']
                        res['url'] = res_url
                    else:
                        res['errno'] = saveTxt_name['errno']
                        res['errmsg'] = saveTxt_name['errmsg']
            else:
                res['errno'] = 1008
                raise Exception('file type error')
        except Exception, e:
            if res['errno'] == 0:
                res['errno'] = 999
            res['errmsg'] = str(e)
        return res

    def compare2TxtAndSaveNewTxt(self,txt1, txt2, type):
        res = {'errno':0, 'errmsg':'', 'file_name':''}
        try:
            if type in (1, 2, 3):
                s1 = set(open(txt1, 'r').readlines())
                s2 = set(open(txt2, 'r').readlines())

                file_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.txt'
                file_path_name = self.server_data_dir + file_name

                save_file = open(file_path_name, 'w')
                if type == 1:   # 求交集
                    save_file.writelines(s1.intersection(s2))
                elif type == 2:  # 求并集
                    save_file.writelines(s1.union(s2))
                elif type == 3:  # 求差集
                    save_file.writelines(s1.difference(s2).union(s2.difference(s1)))

                res['file_name'] = file_name
            else:
                res['errno'] = 1017
                res['errmsg'] = 'type error'
        except Exception, e:
            res['errno'] = 999
            res['errmsg'] = str(e)
        finally:
            return res
