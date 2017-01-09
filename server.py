# -*- coding:utf-8 -*-
__author__ = 'ChenMei'

import time, os
import pymysql as MySQLdb
from flask import Flask, jsonify, request, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from lib.base.util import Util
from toWeb.toWeb_MysqlRestoreAndBackup import ToWeb_MysqlRestoreAndBackup
from toWeb.toWeb_MysqlRunsqlAndSaveExcel import ToWeb_MysqlRunSqlAndSaveExcel
from toWeb.toWeb_Compare2Excel import ToWeb_Compare2Excel
from toWeb.toWeb_SparkRunSqlAndSaveExcel import ToWeb_SparkRunSqlAndSaveExcel
from toWeb.toWeb_SparkRunSqlAndCompareAndSaveExcel import ToWeb_SparkRunSqlAndCompareAndSaveExcel
from toWeb.toWeb_Compare2txt import ToWeb_Compare2Txt

app = Flask(__name__)

config_file = os.path.dirname(os.path.realpath(__file__)) + '/conf/base.conf'
ip = Util.getConfig(config_file, 'serverInfo', "ip")
port = int(Util.getConfig(config_file, 'serverInfo', "port"))

server_data_dir = os.path.dirname(os.path.realpath(__file__)) + '/data/fromServer/'
client_data_dir = os.path.dirname(os.path.realpath(__file__)) + '/data/fromClient/'
app.config['UPLOAD_FOLDER'] = client_data_dir             # UPLOAD_FOLDER 指定了我们文件上传之后在服务器上的存放位置
ALLOWED_EXTENSIONS = set(['txt','sql','xls','xlsx','docx'])   # ALLOWED_EXTENSIONS 则指定了允许上传的文件类型, set(['txt','pdf','png','jpg','jpeg','gif'])


@app.route('/', methods=['GET'])
def index():
      return render_template("index.html")


@app.route('/mysql/backupData', methods=['POST'])
def mysqlBackupData():
    t = ToWeb_MysqlRestoreAndBackup()
    res = t.toWeb_mysqlBackupData()
    return str(res)


@app.route('/mysql/restoreData', methods=['POST'])
def mysqlRestoreData():
    res = {'errno':0, 'errmsg':'', 'url':''}
    try:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            url_for('uploaded_file', filename=filename)
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024    # 限制文件最大16M
        t = ToWeb_MysqlRestoreAndBackup()
        res = t.toWeb_mysqlRestoreData(fileName=filename)
    except:
        res['errno'] = 1014
        res['errmsg'] = 'please upload excel/txt/sql'
    return str(res)


@app.route('/mysql/runSqlAndSaveExcel', methods=['POST'])
def runSqlAndSaveExcel():
    res = {'errno':0, 'errmsg':'', 'url':''}
    try:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            url_for('uploaded_file', filename=filename)
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024    # 限制文件最大16M
        t = ToWeb_MysqlRunSqlAndSaveExcel()
        res = t.toWeb_runSqlAndSaveExcel(fileName=filename)
    except:
        res['errno'] = 1014
        res['errmsg'] = 'please upload excel/txt/sql'
    return str(res)


@app.route('/spark/runSqlAndSaveExcel', methods=['POST'])
def spark_runSqlAndSaveExcel():
    res = {'errno':0, 'errmsg':'', 'url':''}
    try:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            url_for('uploaded_file', filename=filename)
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024    # 限制文件最大16M
        t = ToWeb_SparkRunSqlAndSaveExcel()
        res = t.toWeb_SparkRunSqlAndSaveExcel(fileName=filename)
    except:
        res['errno'] = 1014
        res['errmsg'] = 'please upload excel/txt/sql'
    return str(res)


@app.route('/spark/runSqlAndCompareAndSaveExcel', methods=['POST'])
def spark_runSqlAndCompareAndSaveExcel():
    res = {'errno':0, 'errmsg':'', 'url':''}
    try:
        file1 = request.files['file1']
        if file1 and allowed_file(file1.filename):
            filename1 = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            url_for('uploaded_file', filename=filename1)

        file2 = request.files['file2']
        if file2 and allowed_file(file2.filename):
            filename2 = secure_filename(file2.filename)
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            url_for('uploaded_file', filename=filename2)
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024    # 限制文件最大16M
        # print filename1,filename2
        t = ToWeb_SparkRunSqlAndCompareAndSaveExcel()
        res = t.toWeb_SparkRunSqlAndCompareAndSaveExcel(sqlFile1_name=filename1, sqlFile2_name=filename2)
    except:
        res['errno'] = 1014
        res['errmsg'] = 'please upload excel/txt/sql'
    return str(res)


@app.route('/compare2excel', methods=['POST'])
def compare2Excel():
    res = {'errno':0, 'errmsg':'', 'url':''}
    try:
        file1 = request.files['file1']
        if file1 and allowed_file(file1.filename):
            filename1 = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            url_for('uploaded_file', filename=filename1)

        file2 = request.files['file2']
        if file2 and allowed_file(file2.filename):
            filename2 = secure_filename(file2.filename)
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            url_for('uploaded_file', filename=filename2)
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024    # 限制文件最大16M
        # print filename1,filename2
        c2e = ToWeb_Compare2Excel()
        res = c2e.toWeb_Compare2Excel(excel1_name=filename1, excel2_name=filename2)
    except:
        res['errno'] = 1014
        res['errmsg'] = 'please upload excel/txt/sql'
    return str(res)


@app.route('/compare2excel_retains', methods=['POST'])
def compare2Excel_retains():
    res = {'errno':0, 'errmsg':'', 'url':''}
    try:
        file1 = request.files['file1']
        if file1 and allowed_file(file1.filename):
            filename1 = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            url_for('uploaded_file', filename=filename1)

        file2 = request.files['file2']
        if file2 and allowed_file(file2.filename):
            filename2 = secure_filename(file2.filename)
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            url_for('uploaded_file', filename=filename2)
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024    # 限制文件最大16M
        c2e = ToWeb_Compare2Excel()
        res = c2e.toWeb_Compare2Excel_retains(excel1_name=filename1, excel2_name=filename2)
    except:
        res['errno'] = 1014
        res['errmsg'] = 'please upload excel/txt/sql'
    return str(res)


@app.route('/compare2txt_intersection', methods=['POST'])
def compare2txt_intersection():
    res = {'errno':0, 'errmsg':'', 'url':''}
    try:
        file1 = request.files['file1']
        if file1 and allowed_file(file1.filename):
            filename1 = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            url_for('uploaded_file', filename=filename1)

        file2 = request.files['file2']
        if file2 and allowed_file(file2.filename):
            filename2 = secure_filename(file2.filename)
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            url_for('uploaded_file', filename=filename2)
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024    # 限制文件最大16M
        c2e = ToWeb_Compare2Txt()
        res = c2e.toWeb_Compare2txt(txt1_name=filename1, txt2_name=filename2, type=1)
    except:
        res['errno'] = 1014
        res['errmsg'] = 'please upload excel/txt/sql'
    return str(res)


@app.route('/compare2txt_union', methods=['POST'])
def compare2txt_union():
    res = {'errno':0, 'errmsg':'', 'url':''}
    try:
        file1 = request.files['file1']
        if file1 and allowed_file(file1.filename):
            filename1 = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            url_for('uploaded_file', filename=filename1)

        file2 = request.files['file2']
        if file2 and allowed_file(file2.filename):
            filename2 = secure_filename(file2.filename)
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            url_for('uploaded_file', filename=filename2)
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024    # 限制文件最大16M
        c2e = ToWeb_Compare2Txt()
        res = c2e.toWeb_Compare2txt(txt1_name=filename1, txt2_name=filename2, type=2)
    except:
        res['errno'] = 1014
        res['errmsg'] = 'please upload excel/txt/sql'
    return str(res)


@app.route('/compare2txt_difference', methods=['POST'])
def compare2txt_difference():
    res = {'errno':0, 'errmsg':'', 'url':''}
    try:
        file1 = request.files['file1']
        if file1 and allowed_file(file1.filename):
            filename1 = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            url_for('uploaded_file', filename=filename1)

        file2 = request.files['file2']
        if file2 and allowed_file(file2.filename):
            filename2 = secure_filename(file2.filename)
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            url_for('uploaded_file', filename=filename2)
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024    # 限制文件最大16M
        c2e = ToWeb_Compare2Txt()
        res = c2e.toWeb_Compare2txt(txt1_name=filename1, txt2_name=filename2, type=3)
    except:
        res['errno'] = 1014
        res['errmsg'] = 'please upload excel/txt/sql'
    return str(res)


@app.route('/uploaded_file', methods=['POST'])
def uploaded_file():
    request.form.get('filename')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


@app.route('/excel/download/<excel>', methods=['GET'])
def downloadExcel(excel):
    return send_from_directory(server_data_dir, excel, as_attachment=True)


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8972, debug=True)
    app.run(host=ip, port=port, debug=True)

