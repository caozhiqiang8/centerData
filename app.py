import json
import pandas as pd
from flask import Flask, render_template, request, redirect,session
from public.sqlDB import mysqlDB, sqliteDB, yearSchoolCount
from datetime import timedelta


app = Flask(__name__)
app.config["SECRET_KEY"] = "akjsdhkjashdkjhaksk120191101asd"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60 * 8)

# 登录
@app.route('/',methods = ['get','post'])
@app.route('/login',methods = ['get','post'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        data = request.get_json()
        print(data)

        if data['userName'] == 'admin' and data['passWord'] == '1111':
            data = {
                'code': '0',
            }
            session['userName'] = 'admin'
            session['passWord'] = '1111'
            return data
        else:
            data = {
                'code': '1',
                'masg': '帐号密码错误'

            }
            return data

# 首页路由
@app.route('/index', methods=['get'])
def index():
    return render_template('index.html')

# 首页地图接口
@app.route('/getMap', methods=['get'])
def getMap():
    sql = '''
    select * from every_day_task 
    order by date 
    '''
    task = sqliteDB(sql)
    task['school_id'] = task['school_id'].astype('str')

    y21_22, y21_22Count = yearSchoolCount(df=task, beginTime='2021-07-15', endTime='2022-07-15')
    y20_21, y20_21Count = yearSchoolCount(df=task, beginTime='2020-07-15', endTime='2021-07-15')
    y19_20, y19_20Count = yearSchoolCount(df=task, beginTime='2019-07-15', endTime='2020-07-15')
    y18_19, y18_19Count = yearSchoolCount(df=task, beginTime='2018-07-15', endTime='2019-07-15')
    y17_18, y17_18Count = yearSchoolCount(df=task, beginTime='2017-07-15', endTime='2018-07-15')
    yearCount = [y17_18Count, y18_19Count, y19_20Count, y20_21Count, y21_22Count]
    data = {
        'y21_22': y21_22,
        'y20_21': y20_21,
        'y19_20': y19_20,
        'y18_19': y18_19,
        'y17_18': y17_18,
        'yearCount': yearCount,

    }
    return data

# 用户数据查询
@app.route('/userQuery', methods=['get', 'post'])
def userQuery():
    if request.method == 'GET':
        return render_template('userQuery.html')
    if request.method == 'POST':
        data = json.loads(request.get_data())
        teaName = data['teaName']
        stuName = data['stuName']
        print(teaName, stuName)
        if teaName:
            sql = '''
            SELECT s.name,s.school_id ,u.ett_user_id,oc.user_name , oc.password,t.teacher_name as real_name ,u.state_id, DATE_FORMAT(u.C_TIME,'%%Y-%%m-%%d %%H:%%i:%%s')  as c_time 
            from  oracle2utf.coschuser_info oc,user_info u,school_info s,teacher_info t
            where  oc.jid = u.ETT_USER_ID and u.DC_SCHOOL_ID = s.school_id and u.ref = t.user_id  
            and oc.user_name ='{}'
            '''.format(teaName)
            usrInfo = mysqlDB(sql)
            usrInfo = json.loads(usrInfo.to_json(orient='records', force_ascii=False))
            data = {
                'usrInfo': usrInfo,
                'msg': 'OK'
            }
            return data
        elif stuName:
            sql = '''
            SELECT s.name,s.school_id ,u.ett_user_id,oc.user_name , oc.password,t.stu_name as real_name ,u.state_id,DATE_FORMAT(u.C_TIME,'%%Y-%%m-%%d %%H:%%i:%%s')  as c_time 
            from  oracle2utf.user_info oc,user_info u,school_info s,student_info t 
            where  oc.user_id = u.ETT_USER_ID and u.DC_SCHOOL_ID = s.school_id and u.ref = t.user_id 
            and oc.user_name ='{}'
                        '''.format(stuName)
            usrInfo = mysqlDB(sql)
            usrInfo = json.loads(usrInfo.to_json(orient='records', force_ascii=False))
            data = {
                'usrInfo': usrInfo,
                'msg': 'OK'
            }
            return data
        else:
            return '用户名不能为空'

# 作业分析路由
@app.route('/task', methods=['get'])
def task():
    return render_template('task.html')

# 学校每日作业情况
@app.route('/getSchoolTaskCount', methods=['get'])
def getSchoolTaskCount():
    sql = '''
    select * from every_day_task  where date >= '2022-01-15'
    order by date
    '''
    task = sqliteDB(sql)
    schoolTaskCount = task.groupby(['school_id','name'],as_index=False).sum().sort_values(by='zuoye_count',ascending = False)
    schoolTaskCount = json.loads(schoolTaskCount.to_json(orient='records', force_ascii=False))
    data = {
        'schoolTaskCount':schoolTaskCount,
        'msg':'ok'
    }
    return data

# 平台每日作业情况
@app.route('/getTaskCount', methods=['get'])
def getTaskCount():
    sql = '''
    select * from every_day_task  where date >='2019-07-15'
    order by date
    '''
    task = sqliteDB(sql)

    taskCount = task.groupby(['date'],as_index=False).sum()
    x_date = taskCount['date'].to_list()
    y_list = []
    for i in (taskCount.columns.to_list())[2:]:
        y_list.append(taskCount['{}'.format(i)].to_list())
    type_name = ['学资源', '讨论', '单题', '测验', '微课程', '一般任务', '直播课', '答题卡', '个性化', '先声', '爱学派归档', '答题卡互批', '答题卡自批', '答题卡练习册',
                 '答题卡附件', '答题卡试卷', '新答题卡','作业总数']
    data = {
        'x_date':x_date,
        'y_list':y_list,
        'type_name':type_name,
        'msg':'ok'
    }
    return data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)
