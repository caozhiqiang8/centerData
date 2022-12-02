import json
from flask import  render_template, request
from public.db_con import mysql_connect
from axp_class import  axp_class_blue


# 爱学派课堂分析
@axp_class_blue.route('/classRoom', methods=['get'])
def classRoom():
    return render_template('classRoom.html')


# 爱学派课堂分析
@axp_class_blue.route('/classRoomInfo', methods=['get'])
def classRoomInfo():
    code = request.values.get('code')
    print(code)
    sql = '''
            SELECT c.class_id , c.class_name ,c.year  ,DATE_FORMAT(c.axp_begin_time,'%%Y-%%m-%%d') as axp_begin_time,DATE_FORMAT(c.axp_end_time,'%%Y-%%m-%%d') as axp_end_time ,fr.school_id ,fr.name  
            from class_info c, franchised_school_info fr  where c.axp_end_time >  NOW()  and c.dc_school_id = fr.school_id  
            and fr.school_id >50000 and fr.enable = 0  and fr.school_type in (3,4)  and c.pattern='行政班'
            ORDER BY fr.school_id, c.axp_end_time desc 
            '''
    axpClassData = mysql_connect(sql)

    if code == '1':
        sql = '''
        SELECT fr.school_id, fr.name,c.class_id ,c.axp_begin_time,c.axp_end_time,ol.c_time,ol.remark
        from franchised_school_info  fr , class_info c, operate_log_info ol where fr.school_id = c.dc_school_id and ol.operate_table = 'class_info' and ol.operate_rowsid=c.class_id 
        and fr.SCHOOL_TYPE in (3,4) and fr.enable = 0 AND ol.remark LIKE '%%增加有效期%%1年%%至%%' and ol.c_time >='2022-07-15'  and c.pattern='行政班' and axp_begin_time is not null
        ORDER BY ol.c_time DESC
        '''
        axpClassRenew = mysql_connect(sql)
        axpClassRenewCount = axpClassRenew['class_id'].count()
        axpClassNewCount = axpClassData[axpClassData['axp_begin_time'] >= '2022-07-15 00:00:00']['class_id'].count()

        axpSchool = (axpClassData.groupby(['school_id', 'name'], as_index=False).count()).sort_values(by='class_id',
                                                                                                      ascending=False)
        axpSchool = (axpSchool.reset_index(drop=True)).iloc[:, 0:3]
        axpSchool = json.loads(axpSchool.to_json(orient='records', force_ascii=False))
        axpClassCount = axpClassData['class_id'].count()

        data = {
            'axpSchool': axpSchool,
            'axpClassCount': int(axpClassCount),
            'axpClassRenewCount': int(axpClassRenewCount),
            'axpClassNewCount': int(axpClassNewCount),
        }
        return data

    if code == '2':
        axpClass = json.loads(axpClassData.to_json(orient='records', force_ascii=False))

        data = {
            'axpClass': axpClass,
        }
        return data

