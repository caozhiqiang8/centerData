import json
from flask import  render_template, request
from public.db_con import mysql_connect
from user_query import user_query_blue

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
            '''.format(teaName)
            usrInfo = mysql_connect(sql)
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
            usrInfo = mysql_connect(sql)
            usrInfo = json.loads(usrInfo.to_json(orient='records', force_ascii=False))
            data = {
                'usrInfo': usrInfo,
                'msg': 'OK'
            }
            return data
        else:
            return '用户名不能为空'

