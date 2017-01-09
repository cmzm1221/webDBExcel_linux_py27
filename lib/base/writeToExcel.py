# -*- coding:utf-8 -*-
__author__ = 'ChenMei'

import xlwt
import os,time


class WriteToExcel:
    # 往excel 文档中写入数据
    # wook_book_name 保存的 excel 文档名称; sheet_name 需要保存的工作表名;  table_title 保存的表字段名称，在第一行;
    # num_ncols 保存文档的列个数; num_selTableData 保存数据的行条数; values 保存的数据

    data_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/data/fromServer/'

    def __init__(self, file_name):
        self.file_name = file_name
        self.wbk = xlwt.Workbook(encoding='utf-8')

    def writeExcel(self, sheet_name, table_title, num_ncols, num_selTableData, values):
        try:
            style = xlwt.XFStyle()                # 创建样式的对象
            font = xlwt.Font()                    # 创建字体的对象
            font.name = 'Times New Roman'         # 字体的名字
            font.bold = True                      # 字体加粗
            style.font = font
            st = self.wbk.add_sheet(sheet_name, cell_overwrite_ok=True)

            for i in range(num_ncols):
                st.write(0, i, table_title[i], style)       # 写表字段，加样式
                st.col(i).width = 4444                      # 设置cell的宽度,width = 3333  # 3333 = 1" (one inch).

            for i in range(num_selTableData):
                for j in range(num_ncols):
                    if values[i][j] is None:
                        st.write(i+1, j, values[i][j])          # 写数据
                    else:
                        st.write(i+1, j, str(values[i][j]))     # 写数据
        except Exception, e:
            print "保存 excel 失败，请检查excel 是否是打开状态 或者 保存盘符是否存在。"
            print e

    # 把结果保存在excel 中,只传行数和值
    def saveNewExcel_noCompare(self, num_nrows, sql_run_result):
        # print num_nrows, sql_run_result
        res = {'errno':0, 'errmsg':''}
        if num_nrows >= 1:
            try:
                num_ncols = len(sql_run_result[0])
                st = self.wbk.add_sheet("result", cell_overwrite_ok=True)        # 工作表名称
                for i in range(num_nrows):
                    for j in range(num_ncols):
                        if sql_run_result[i][j] is None:
                            st.write(i+1, j, sql_run_result[i][j])          # 写数据
                        else:
                            st.write(i+1, j, str(sql_run_result[i][j]))     # 写数据
            except:
                res['errno'] = 1005
                res['errmsg'] = 'write excel fail'
        else:
            res['errno'] = 1005
            res['errmsg'] = 'write excel fail'
        return res

    # 把2个sql 查询完成后的数据写入一个excel 中，并且进行对比。对对比通过还是失败的结果没有排序
    def saveNewExcel_Compare2(self, first_excel_num, first_excel_values, second_excel_num, second_excel_values):
        # print num_nrows, sql_run_result
        res = {'errno':0, 'errmsg':''}
        first_num_ncols = len(first_excel_values[0])     # first层的列数,即统计的表名数量
        second_num_ncols = len(second_excel_values[0])           # second 层的列数,即统计的表名数量

        if first_excel_num >= 1 and second_excel_num >= 1 and first_excel_num == second_excel_num \
                and first_num_ncols == second_num_ncols:
            try:
                st = self.wbk.add_sheet("result", cell_overwrite_ok=True)        # 工作表名称

                # 记录first 层的数据
                for i in range(first_excel_num):
                    for j in range(first_num_ncols):
                        if first_excel_values[i][j] is None:
                            st.write(i, j, first_excel_values[i][j])          # 写数据
                        else:
                            st.write(i, j, str(first_excel_values[i][j]))     # 写数据

                # 记录second 层数据
                second_end_ncols = first_num_ncols + second_num_ncols  # second 结束列数=first层列数 + second层列数
                x = 0
                for i in range(second_excel_num):
                    y = 0
                    for j in range(first_num_ncols, second_end_ncols):
                        if second_excel_values[x][y] is None:
                            st.write(i, j, second_excel_values[x][y])          # 写数据
                        else:
                            st.write(i, j, str(second_excel_values[x][y]))     # 写数据
                        y = y+1
                    x = x+1

                # 记录对比结果
                compare_begin_ncols = first_num_ncols * 2      # 开始的列数=first层列数+second层列数，即行数的2倍
                compare_end_ncols = first_num_ncols * 3        # 开始的列数=first层列数的3倍
                style_pass = xlwt.easyxf('pattern: pattern solid, fore_colour green;')
                style_fail = xlwt.easyxf('pattern: pattern solid, fore_colour red;')
                x = 0
                for i in range(first_excel_num):
                    y = 0
                    for j in range(compare_begin_ncols, compare_end_ncols):
                        if str(first_excel_values[x][y]) == str(second_excel_values[x][y]):
                            st.write(i, j, u'通过', style_pass)          # 写数据
                        else:
                            st.write(i, j, u'失败', style_fail)     # 写数据
                        y = y+1
                    x = x+1
                # self.wbk.save('cmtest2.xls')
            except:
                res['errno'] = 1005
                res['errmsg'] = 'write excel fail'
        else:
            res['errno'] = 1007
            res['errmsg'] = 'compare excel fail' + '数据条数少于1或者条数不一致'
        return res

    # 把2个sql 查询完成后的数据写入一个excel 中，并且进行对比。对对比通过、失败的有做排序：先记录buffer层条数=0，再记录buffer层条数>0且和ods层条数相同，最后记录条数不相同的。
    def saveNewExcel_Compare(self, buffer_excel_num, buffer_excel_values, ods_excel_num, ods_excel_values):
        res = {'errno':0, 'errmsg':''}
        buffer_num_ncols = len(buffer_excel_values[0])     # buffer层的列数,即统计的表名数量
        ods_num_ncols = len(ods_excel_values[0])           # ods 层的列数,即统计的表名数量

        if buffer_excel_num >= 1 and ods_excel_num >= 1 and buffer_excel_num == ods_excel_num \
                and buffer_num_ncols == ods_num_ncols:
            try:
                st = self.wbk.add_sheet("result", cell_overwrite_ok=True)        # 工作表名称
                # 设置列的宽度
                st.col(0).width = 2222
                st.col(1).width = 4444*4
                st.col(2).width = 5555
                st.col(3).width = 4444*4
                st.col(4).width = 5555
                st.col(5).width = 3333

                # 设置边框
                borders = xlwt.Borders()
                borders.left = 1
                borders.right = 1
                borders.top = 1
                borders.bottom = 1
                # borders.bottom_colour=0x3A

                font = xlwt.Font()
                font.bold = True         # 设置字体加粗
                style = xlwt.XFStyle()   # 单元格实例化
                style.font = font
                style.borders = borders

                # 先写表头的2行
                st.write(0, 1, str(buffer_excel_values[0][0]), style)
                st.write(0, 2, str(buffer_excel_values[0][1]), style)
                st.write(1, 1, str(buffer_excel_values[1][0]), style)
                st.write(1, 2, str(buffer_excel_values[1][1]), style)

                st.write(0, 3, str(ods_excel_values[0][0]), style)
                st.write(0, 4, str(ods_excel_values[0][1]), style)
                st.write(1, 3, str(ods_excel_values[1][0]), style)
                st.write(1, 4, str(ods_excel_values[1][1]), style)

                st.write_merge(0, 1, 0, 0, '序号', style)
                st.write_merge(0, 1, 5, 5, '条数对比结果', style)
                for i in range(2, buffer_excel_num):              # 写序号
                    st.write(i, 0, str(i-1), style)

                zero_num = 0
                zero_index = []
                same_num = 0
                same_index = []
                deff_nume = 0
                deff_index = []

                for i in range(2, buffer_excel_num):
                    if int(buffer_excel_values[i][1]) == 0:      # 1、buffer 条数=0
                        zero_num += 1
                        zero_index.append(i)
                    else:                                        # 2、buffer 条数>0
                        if int(buffer_excel_values[i][1]) == int(ods_excel_values[i][1]):  # 2.1、 2边值相等
                            same_num += 1
                            same_index.append(i)
                        else:                                    # 2.2、 2边值不相等
                            deff_nume += 1
                            deff_index.append(i)

                # 设置背景颜色
                pattern_pass = xlwt.Pattern()
                pattern_pass.pattern = xlwt.Pattern.SOLID_PATTERN
                pattern_pass.pattern_fore_colour = 17

                style_pass = xlwt.XFStyle()
                style_pass.borders = borders
                style_pass.pattern = pattern_pass

                pattern_fail = xlwt.Pattern()
                pattern_fail.pattern = xlwt.Pattern.SOLID_PATTERN
                pattern_fail.pattern_fore_colour = 2

                style_fail = xlwt.XFStyle()
                style_fail.borders = borders
                style_fail.pattern = pattern_fail

                style_ordinary = xlwt.XFStyle()
                style_ordinary.borders = borders

                if zero_num >= 1:
                    x = 0
                    for i in range(2, zero_num+2):
                        st.write(i, 1, str(buffer_excel_values[zero_index[x]][0]), style_ordinary)   # 写表名
                        st.write(i, 2, str(buffer_excel_values[zero_index[x]][1]), style_ordinary)   # 写统计条数
                        st.write(i, 3, str(ods_excel_values[zero_index[x]][0]), style_ordinary)      # 写表名
                        st.write(i, 4, str(ods_excel_values[zero_index[x]][1]), style_ordinary)      # 写统计条数
                        if str(buffer_excel_values[zero_index[x]][1]) == str(ods_excel_values[zero_index[x]][1]):
                            st.write(i, 5, u'通过', style_pass)
                        else:
                            st.write(i, 5, u'失败', style_fail)
                        x += 1

                if same_num >= 1:
                    x = 0
                    sum_num2 = same_num + zero_num + 2
                    for i in range(zero_num+2, sum_num2):
                        st.write(i, 1, str(buffer_excel_values[same_index[x]][0]), style_ordinary)   # 写表名
                        st.write(i, 2, str(buffer_excel_values[same_index[x]][1]), style_ordinary)   # 写统计条数
                        st.write(i, 3, str(ods_excel_values[same_index[x]][0]), style_ordinary)      # 写表名
                        st.write(i, 4, str(ods_excel_values[same_index[x]][1]), style_ordinary)      # 写统计条数
                        if str(buffer_excel_values[same_index[x]][1]) == str(ods_excel_values[same_index[x]][1]):
                            st.write(i, 5, u'通过', style_pass)
                        else:
                            st.write(i, 5, u'失败', style_fail)
                        x += 1

                if deff_nume >= 1:
                    x = 0
                    sum_num_begin = same_num + zero_num + 2
                    for i in range(sum_num_begin, buffer_excel_num):
                        st.write(i, 1, str(buffer_excel_values[deff_index[x]][0]), style_ordinary)   # 写表名
                        st.write(i, 2, str(buffer_excel_values[deff_index[x]][1]), style_ordinary)   # 写统计条数
                        st.write(i, 3, str(ods_excel_values[deff_index[x]][0]), style_ordinary)      # 写表名
                        st.write(i, 4, str(ods_excel_values[deff_index[x]][1]), style_ordinary)      # 写统计条数
                        if str(buffer_excel_values[deff_index[x]][1]) == str(ods_excel_values[deff_index[x]][1]):
                            st.write(i, 5, u'通过', style_pass)
                        else:
                            st.write(i, 5, u'失败', style_fail)
                        x += 1
                # self.wbk.save('cmtest.xls')
            except Exception, e:
                print e
                res['errno'] = 1005
                res['errmsg'] = 'write excel fail'
        else:
            res['errno'] = 1007
            res['errmsg'] = 'compare excel fail' + '数据条数少于1或者条数不一致'
        return res

    def __del__(self):
        try:
            save_file = self.data_dir + self.file_name
            self.wbk.save(save_file)  # 保存 excel 文档
        except Exception, e:
            print '析构函数出错：',e

if __name__== '__main__':
    buffer_excel_num = 9
    ods_excel_num = 9
    buffer_excel_values = [['统计日期','20160517'], ['表名1','条数1'],[u'1a1', u'0'], [u'1a2', u'100'], [u'1a3', u'200'], [u'1a4', u'300'], [u'1a5', u'400'], [u'1a6', u'500'], [u'1a7', u'0']]
    ods_excel_values    = [['统计日期','20160517'], ['表名2','条数2'],[u'1a1', u'0'], [u'2a2', u'100'], [u'2a3', u'201'], [u'2a4', u'300'], [u'2a5', u'401'], [u'2a6', u'500'], [u'2a7', u'0']]
    w = WriteToExcel('cmtest.xls')
    # print w.saveNewExcel_Compare2(buffer_excel_num, buffer_excel_values, ods_excel_num, ods_excel_values)
    print w.saveNewExcel_Compare(buffer_excel_num, buffer_excel_values, ods_excel_num, ods_excel_values)
    # print w.saveNewExcel_noCompare(buffer_excel_num, buffer_excel_values)