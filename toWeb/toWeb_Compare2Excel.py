# -*- coding:utf-8 -*-
__author__ = 'ChenMei'
import sys, os, time
import xlrd, xlwt
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lib.base.util import Util

class ToWeb_Compare2Excel():
    base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    server_data_dir = base_dir + '/data/fromServer/'
    client_data_dir = base_dir + '/data/fromClient/'
    config_file = base_dir + '/conf/base.conf'
    ip = Util.getConfig(config_file, 'serverInfo', "ip")
    port = Util.getConfig(config_file, 'serverInfo', "port")

    # 对比2个excel，在结果的excel 中没有保留原2个excel 的数据
    def toWeb_Compare2Excel(self, excel1_name, excel2_name):
        res = {'errno':0, 'errmsg':'', 'url':''}
        try:
            if (excel1_name[-3:] == 'xls' or excel1_name[-4:] == 'xlsx') \
                    and (excel2_name[-3:] == 'xls' or excel2_name[-4:] == 'xlsx') :  # 判断文件类型
                    excel1_path_name = self.client_data_dir + excel1_name
                    excel2_path_name = self.client_data_dir + excel2_name
                    # __compare2ExcelAndSaveNewExcel 返回的执行结果 {'errno':0, 'errmsg':'', 'file_name':''}
                    saveExcel_name = self.__compare2ExcelAndSaveNewExcel(excel1=excel1_path_name, excel2=excel2_path_name)
                    if saveExcel_name['errno'] ==0:
                        res_url = "http://" + self.ip + ":" + self.port + "/excel/download/" + saveExcel_name['file_name']
                        res['url'] = res_url
                    else:
                        res['errno'] = saveExcel_name['errno']
                        res['errmsg'] = saveExcel_name['errmsg']
            else:
                res['errno'] = 1008
                raise Exception('file type error')
        except Exception, e:
            if res['errno'] == 0:
                res['errno'] = 999
            res['errmsg'] = str(e)
        return res

    # 把期望excel 和实际的excel 做对比，把对比结果保存在新的excel 中
    def __compare2ExcelAndSaveNewExcel(self, excel1, excel2):
        value_title = self.__onlyGetOneRow(excel1)
        num_nrows_read_excel, sql_run_result = self.__onlyReadExcel(excel1)
        num_nrows_read_web, sql_run_result_web = self.__onlyReadExcel(excel2)
        # __compare2Excel 返回的执行结果 {'errno':0, 'errmsg':'', 'file_name':''}
        save_excel_name = self.__compare2Excel(num_nrows_read_excel, sql_run_result, num_nrows_read_web, sql_run_result_web, value_title)
        return save_excel_name

    # 只读取excel的数据，返回除表头的条数和数据
    def __onlyReadExcel(self, excel_name):
        wbk_rd = xlrd.open_workbook(excel_name)
        st_rd = wbk_rd.sheet_by_index(0)              # 读取第一个工作表
        num_nrows_value = st_rd.nrows-1               # 获取要插入的数据总共有几行
        value = []
        for i in range(1, st_rd.nrows):
            value.append(st_rd.row_values(i))
        return num_nrows_value, value

    # 只获取到第1个excel文档的第一行表头
    def __onlyGetOneRow(self, excel_name):
        wbk_rd = xlrd.open_workbook(excel_name)
        st_rd = wbk_rd.sheet_by_index(0)              # 读取第一个工作表
        value = []
        for i in range(1):
            value.append(st_rd.row_values(i))
        return value

    # 写对比后的结果，单独保存为excel_result.xls
    def __compare2Excel(self, qiwang_excel_num, qiwang_excel_values, shiji_excel_num, shiji_excel_values, value_title):
        res = {'errno':0, 'errmsg':'', 'file_name':''}
        try:
            wbk = xlwt.Workbook()
            st = wbk.add_sheet('compare_result', cell_overwrite_ok=True)     # compare_result 是工作表名
            style = xlwt.XFStyle()                # 创建样式的对象
            font = xlwt.Font()                    # 创建字体的对象
            font.name = 'Times New Roman'         # 字体的名字
            font.bold = True                      # 字体加粗
            style.font = font

            cols = len(value_title[0])    # 列数
            for i in range(cols):
                st.write(0, i, value_title[0][i], style)

            style_pass = xlwt.easyxf('pattern: pattern solid, fore_colour green;')
            style_fail = xlwt.easyxf('pattern: pattern solid, fore_colour red;')
            if qiwang_excel_num == shiji_excel_num:
                for i in range(qiwang_excel_num):
                    for j in range(len(qiwang_excel_values[i])):
                        if qiwang_excel_values[i][j] == shiji_excel_values[i][j]:
                            st.write(i+1, j, u'通过', style_pass)
                        else:
                            st.write(i+1, j, u'失败', style_fail)
            else:
                res['errno'] = 1015
                res['errmsg'] = 'Line number is not consistent'
                print "excel中设置对比的期望行数=" + str(qiwang_excel_num) +" 与 实际执行sql语句返回的行数=" + str(shiji_excel_num) +" 不一致。"
                return res
            file_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.xls'
            file_path_name = ToWeb_Compare2Excel.server_data_dir + file_name
            wbk.save(file_path_name)
            res['file_name'] = file_name
        except Exception, e:
            res['errno'] = 999
            res['errmsg'] = str(e)
        finally:
            return res

    # 对比2个excel，在结果的excel 中保留原2个excel 的数据
    def toWeb_Compare2Excel_retains(self, excel1_name, excel2_name):
        res = {'errno':0, 'errmsg':'', 'url':''}
        try:
            if (excel1_name[-3:] == 'xls' or excel1_name[-4:] == 'xlsx') \
                    and (excel2_name[-3:] == 'xls' or excel2_name[-4:] == 'xlsx') :  # 判断文件类型
                    excel1_path_name = self.client_data_dir + excel1_name
                    excel2_path_name = self.client_data_dir + excel2_name
                    # __compare2ExcelAndSaveNewExcel 返回的执行结果 {'errno':0, 'errmsg':'', 'file_name':''}
                    saveExcel_name = self.compare2ExcelAndSaveNewExcel_retains(excel1=excel1_path_name, excel2=excel2_path_name)
                    if saveExcel_name['errno'] ==0:
                        res_url = "http://" + self.ip + ":" + self.port + "/excel/download/" + saveExcel_name['file_name']
                        res['url'] = res_url
                    else:
                        res['errno'] = saveExcel_name['errno']
                        res['errmsg'] = saveExcel_name['errmsg']
            else:
                res['errno'] = 1008
                raise Exception('file type error')
        except Exception, e:
            if res['errno'] == 0:
                res['errno'] = 999
            res['errmsg'] = str(e)
        return res

    # 把期望excel 和实际的excel 做对比，把对比结果保存在新的excel 中
    def compare2ExcelAndSaveNewExcel_retains(self, excel1, excel2):
        num_nrows_read_excel, sql_run_result = self.__onlyReadExcel_retains(excel1)
        num_nrows_read_web, sql_run_result_web = self.__onlyReadExcel_retains(excel2)
        # __compare2Excel 返回的执行结果 {'errno':0, 'errmsg':'', 'file_name':''}
        save_excel_name = self.__compare2Excel_retains(num_nrows_read_excel, sql_run_result, num_nrows_read_web, sql_run_result_web)
        return save_excel_name

    # 读取excel的数据，返回所有条数和数据（包含第1行）
    def __onlyReadExcel_retains(self, excel_name):
        wbk_rd = xlrd.open_workbook(excel_name)
        st_rd = wbk_rd.sheet_by_index(0)              # 读取第一个工作表
        num_nrows_value = st_rd.nrows               # 获取要插入的数据总共有几行
        value = []
        for i in range(st_rd.nrows):
            value.append(st_rd.row_values(i))
        return num_nrows_value, value

    # 写对比后的结果，保留原2个excel 的数据单独保存为excel_result.xls
    def __compare2Excel_retains(self, qiwang_excel_num, qiwang_excel_values, shiji_excel_num, shiji_excel_values):
        res = {'errno':0, 'errmsg':'', 'file_name':''}
        try:
            wbk = xlwt.Workbook()
            st = wbk.add_sheet('compare_result', cell_overwrite_ok=True)     # compare_result 是工作表名
            style = xlwt.XFStyle()                # 创建样式的对象
            font = xlwt.Font()                    # 创建字体的对象
            font.name = 'Times New Roman'         # 字体的名字
            font.bold = True                      # 字体加粗
            style.font = font

            style_pass = xlwt.easyxf('pattern: pattern solid, fore_colour green;')
            style_fail = xlwt.easyxf('pattern: pattern solid, fore_colour red;')

            col1_num = len(qiwang_excel_values[0])   # 期望的列数
            col2_num = len(shiji_excel_values[0])    # 实际的列数

            if qiwang_excel_num != shiji_excel_num:
                res['errno'] = 1015
                res['errmsg'] = 'Line number is not consistent'
                print "excel中设置对比的期望行数=" + str(qiwang_excel_num) +" 与 实际执行sql语句返回的行数=" + str(shiji_excel_num) +" 不一致。"
                return res

            if col1_num != col2_num:
                res['errno'] = 1016
                res['errmsg'] = 'column number is not consistent'
                print "excel中设置对比的期望列数=" + str(col1_num) +" 与 实际执行sql语句返回的列数=" + str(col2_num) +" 不一致。"
                return res

            for i in range(qiwang_excel_num):
                for j in range(col1_num):
                    st.write(i, j*3, qiwang_excel_values[i][j])
                    st.write(i, j*3+1, shiji_excel_values[i][j])

                    if qiwang_excel_values[i][j] == shiji_excel_values[i][j]:
                        st.write(i, j*3+2, u'通过', style_pass)
                    else:
                        st.write(i, j*3+2, u'失败', style_fail)

            file_name = time.strftime('%Y%m%d%H%M%S', time.localtime()) + '.xls'
            file_path_name = ToWeb_Compare2Excel.server_data_dir + file_name
            wbk.save(file_path_name)
            res['file_name'] = file_name
        except Exception, e:
            res['errno'] = 999
            res['errmsg'] = str(e)
        finally:
            return res


if __name__ == "__main__":
    t = ToWeb_Compare2Excel()
    # print t.toWeb_Compare2Excel(r"F:\test\xyk_openline_dsj.xls", r"F:\test\xyk_openline_zc.xlsx")
    print t.compare2ExcelAndSaveNewExcel_retains(r"F:\test\xyk_openline_dsj.xls", r"F:\test\xyk_openline_zc.xlsx")