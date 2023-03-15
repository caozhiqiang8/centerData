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
        order by active_time  desc 
    '''
    data = mysql_connect(sql)
    pad_license_json = json.loads((data.groupby('state_id').count()).to_json())
    pad_license_count = pad_license_json['license_id']
    pad_license = json.loads(data.to_json(orient='records', force_ascii=False))
    data = {
        'pad_license': pad_license,
        'pad_license_count':pad_license_count
    }

    return data



