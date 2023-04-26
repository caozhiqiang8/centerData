import json
from flask import render_template, request
from public.db_con import mysql_connect,sqlite_connect
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
    data['state_id'] = data['state_id'].replace([0,1,7,8],['出库未激活','未加卡','已激活',' B转C'])
    pad_license_json = json.loads((data.groupby('state_id').count()).to_json())
    pad_license_count = pad_license_json['license_id']
    pad_license = json.loads(data.to_json(orient='records', force_ascii=False))
    data = {
        'pad_license': pad_license,
        'pad_license_count':pad_license_count
    }

    return data

@pad_license_blue.route('/padLicenseDau', methods=['get'])
def padLicenseDau():
    res_id = request.args.get('res')
    print(res_id)
    if res_id =='0':
        sql = '''
        SELECT strftime('%Y-%m-%d',time ) as 'date' , pv,uv  from pad_license_dau
        '''
    elif res_id =='1':
        sql = '''
        SELECT time as 'date' , pv,uv  from pad_license_dau_h  

        '''
    data = sqlite_connect(sql=sql)
    data_x = data['date'].to_list()
    data_y1 = data['pv'].to_list()
    data_y2 = data['uv'].to_list()
    data = {
        'data_x':data_x,
        'data_y':[data_y1,data_y2]

    }
    return data



