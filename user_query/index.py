import json
from flask import render_template, request
from public.db_con import mysql_connect
from user_query import user_query_blue
import pandas as pd
import os




# 用户数据查询
@user_query_blue.route('/userQuery', methods=['get', 'post'])
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
            '''.format(teaName,teaName,teaName)
            usrInfo = mysql_connect(sql)
            usrInfo = json.loads(usrInfo.to_json(orient='records', force_ascii=False))
            print(usrInfo)
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
              and (oc.user_name ='{}' or oc.user_id = '{}'  ) and oc.user_id != 0
                        '''.format(stuName,stuName)
            usrInfo = mysql_connect(sql)
            usrInfo = json.loads(usrInfo.to_json(orient='records', force_ascii=False))
            data = {
                'usrInfo': usrInfo,
                'msg': 'OK'
            }
            return data
        else:
            return '用户名不能为空'


@user_query_blue.route('/schoolQuery', methods=['post'])
def schoolQuery():
    data = json.loads(request.get_data())
    code = data['code']
    schoolId = data['schoolId']
    print(schoolId,code)
    if code == '1':
        sql = '''
        SELECT u.ett_user_id as 'jid',u.user_id ,t.teacher_name as 'name',oc.user_name ,oc.password
        from user_info u , oracle2utf.coschuser_info oc, teacher_info  t  
        where u.ETT_USER_ID = oc.jid and u.DC_SCHOOL_ID = {} and t.USER_ID = u.ref  and u.STATE_ID = 0
        '''.format(schoolId)
        schoolInfo = mysql_connect(sql)
    else:
        sql = '''
            SELECT u.ett_user_id as 'jid',u.user_id ,s.stu_name as 'name' ,ou.user_name ,ou.password,s.stu_no,s.stu_district_no ,c.class_grade ,c.class_name
            from user_info u ,j_class_user jc , class_info  c, oracle2utf.user_info ou, student_info s
            where u.ETT_USER_ID = ou.user_id and u.DC_SCHOOL_ID = {} and jc.class_id = c.class_id and jc.user_id = u.ref  and s.user_id = u.ref and c.year = '2022~2023'
            and u.STATE_ID = 0
            ORDER BY c.class_grade,c.class_name              '''.format(schoolId)
        schoolInfo = mysql_connect(sql)

    schoolInfo = json.loads(schoolInfo.to_json(orient='records', force_ascii=False))
    data = {
        'schoolInfo': schoolInfo,
        'msg': 'OK'
    }

    return data


@user_query_blue.route('/download', methods=['post'])
def download():
    data = json.loads(request.get_data())
    data = data['data']

    df = pd.json_normalize(data)

    # 获取下载文件路径
    path = '{}\\static\\file\\'.format(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    # 数据保存到下载路径
    df.to_excel('{}学校帐号密码.xlsx'.format(path))

    file_path = '{}学校帐号密码.xlsx'.format(path)
    file_path = file_path.replace('/','\\')
    print(file_path)

    file = open(file_path, "rb").read()

    # 删除
    os.remove(file_path)

    return file

