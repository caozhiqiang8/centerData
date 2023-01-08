import json
from flask import render_template
from public.db_con import mysql_connect
from pad_license import pad_license_blue


@pad_license_blue.route('/padLicense', methods=['get'])
def padLincense():
    return render_template('padLicense.html')


@pad_license_blue.route('/padLicenseInfo', methods=['get'])
def padLicenseInfo():
    sql = '''
    	select license_id,remarks,state_id,os.school_id,os.name , DATE_FORMAT(opl.c_time ,'%%Y-%%m-%%d %%H:%%i:%%S') as c_time ,DATE_FORMAT(opl.active_time  ,'%%Y-%%m-%%d %%H:%%i:%%S') as active_time 
        from oracle2utf.pad_license_info  opl,oracle2utf.school_info  os 
        where  opl.school_id = os.SCHOOL_ID
        and opl.REMARKS not like '%%测试%%' and opl.REMARKS not like '%%test%%'
       and opl.REMARKS not like '%%TEST%%'
        and opl.REMARKS not like '%%分校%%'
        order by active_time  desc 
    '''
    data = mysql_connect(sql)
    pad_license_count = json.loads((data.groupby('state_id').count()).iloc[:, [1]].to_json())
    pad_license_1 = pad_license_count['remarks']['1']
    pad_license_8 = pad_license_count['remarks']['8']
    pad_license_7 = pad_license_count['remarks']['7']
    pad_license_sum = pad_license_1 + pad_license_8 + pad_license_7

    pad_license = json.loads(data.to_json(orient='records', force_ascii=False))
    data = {
        'pad_license': pad_license,
        'pad_license_1': pad_license_1,
        'pad_license_8': pad_license_8,
        'pad_license_7': pad_license_7,
        'pad_license_sum': pad_license_sum,
    }

    return data
