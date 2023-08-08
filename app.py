import pandas as pd
from flask import Flask, render_template, send_from_directory
from flask_compress import Compress
from datetime import timedelta
from login import login_blue
from index import index_blue
from school import school_blue
from user_query import user_query_blue
from task import task_blue
from practise import practise_book_blue
from axp_class import axp_class_blue
from monitor import monitor_blue
from exam import exam_blue
from pad_license import pad_license_blue
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(login_blue)
app.register_blueprint(index_blue)
app.register_blueprint(school_blue)
app.register_blueprint(user_query_blue)
app.register_blueprint(task_blue)
app.register_blueprint(practise_book_blue)
app.register_blueprint(axp_class_blue)
app.register_blueprint(monitor_blue)
app.register_blueprint(exam_blue)
app.register_blueprint(pad_license_blue)

app.config["SECRET_KEY"] = "akjsdhkjashdkjhaksk120191101asd"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60 * 8)

# app.config['UPLOAD_FOLDER'] = './static/file'

Compress(app)


# 知识图谱
@app.route('/atlas', methods=['get'])
def atlas():
    return render_template("atlas.html")


# 图片对比
@app.route('/image1/<int:page>', methods=['get'])
def image(page):
    res = pd.read_excel(r'C:\Users\caozhiqiang\Desktop\新建 XLSX 工作表(3).xlsx', sheet_name='Sheet1')
    begin = 0
    end = 100
    if page:
        begin = page * end - end
        end = page * end
        if end > len(res['Old_Path'].to_list()):
            begin = 0
            end = 100
    else:
        begin = 0
        end = 100

    old_path = res['Old_Path'].to_list()[begin:end]
    new_name = res['New_Name'].to_list()[begin:end]
    data = {
        'old_path': old_path,
        'new_name': new_name,
    }
    print(begin)
    print(end)
    return render_template("image.html", data=data)

@app.route('/download', methods=['get'])
def download():
    dir_path = r'C:\Users\caozhiqiang\Desktop'
    file_name = '初三G110.xlsx'
    attachment_filename = 'g10'
    return send_from_directory(dir_path, file_name, attachment_filename='学校G10.xlsx')

CORS(app, resources=r'/*')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
