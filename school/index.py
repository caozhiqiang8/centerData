import json

from school import school_blue
from flask import render_template
from public.db_con import sqlite_connect, mysql_connect


@school_blue.route('/school', methods=['get'])
def school():
    return render_template('school.html')


@school_blue.route('/schoolCRM', methods=['get'])
def schoolCRM():
    sql = '''
                SELECT type as 'name' ,count(*) as 'value' from school_crm 
                GROUP BY  type 
                ORDER BY value desc 
                '''
    data = sqlite_connect(sql)
    data['value'] = data['value'].astype('str')
    school_crm = data.to_dict('records')
    data = {
        'school_crm': school_crm
    }
    return data


@school_blue.route('/schoolInfo', methods=['get'])
def schoolInfo():
    sql = '''
    select * from school_info
    '''
    schoolInfo = sqlite_connect(sql)

    schoolInfo = json.loads(schoolInfo.to_json(orient='records', force_ascii=False))

    data = {
        'schoolInfo': schoolInfo
    }
    return data
