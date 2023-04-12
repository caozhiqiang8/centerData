import datetime
import json
import time
import pandas as pd
import requests
from public.db_con import mysql_connect, sqlite_connect, write_Sqlite
from public.df_merge import df_merge
from public.record_time import cost_time
from public.school_crm import school_crm
import threading
import schedule

task_df_list = []

def task_yb(time):
    sql = '''
    SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'yb'
    FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
    WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1 {}
    and fr.school_type in (3,4) and tt.task_type in (7,8,9)  and tt.classroom_id is null and s.school_id = fr.school_id  and tt.c_time is not null
    GROUP BY date,fr.school_id
    '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


def task_xzy(time):
    sql = '''
    SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'xzy'
    FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
    WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1  {}
    and fr.school_type in (3,4) and tt.task_type in (1)  and tt.classroom_id is null and s.school_id = fr.school_id  and tt.c_time is not null
    GROUP BY date,fr.school_id
    '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


def task_tl(time):
    sql = '''
    SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'tl'
    FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
    WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1  {}
    and fr.school_type in (3,4) and tt.task_type in (2)  and tt.classroom_id is null and s.school_id = fr.school_id  and tt.c_time is not null
    GROUP BY date,fr.school_id
    '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


def task_dl(time):
    sql = '''
    SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'dt'
    FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
    WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1  {}
    and fr.school_type in (3,4) and tt.task_type in (3)  and tt.classroom_id is null and s.school_id = fr.school_id  and tt.c_time is not null
    GROUP BY date,fr.school_id
    '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


def task_cy(time):
    sql = '''
    SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'cy'
    FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
    WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1  {}
    and fr.school_type in (3,4) and tt.task_type in (4)  and tt.classroom_id is null and s.school_id = fr.school_id  and tt.c_time is not null
    GROUP BY date,fr.school_id
    '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


def task_wkc(time):
    sql = '''
    SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'wkc'
                FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
                WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 
                and tc.LOCAL_STATUS = 1 and tt.c_time is not null and fr.school_type in (3,4) and ( ( tt.task_type =13 
                and video_id is not  null) or tt.task_type =6)   and tt.classroom_id is null and s.school_id = fr.school_id  {}
                GROUP BY date,fr.school_id
    '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


def task_zbk(time):
    sql = '''
    SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'zbk'
    FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
    WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1  {}
    and fr.school_type in (3,4) and tt.task_type in (10)  and tt.classroom_id is null and s.school_id = fr.school_id  and tt.c_time is not null
    GROUP BY date,fr.school_id
    '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


def task_dtk(time):
    sql = '''
    SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'dtk'
                FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
                WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0  and tc.LOCAL_STATUS = 1 and tt.c_time is not null
                and fr.school_type in (3,4) and tt.task_type =13 and tt.video_id is null  and tt.classroom_id is null and s.school_id = fr.school_id {}
                GROUP BY date,fr.school_id
    '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


def task_gxh(time):
    sql = '''
    SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'gxh'
    FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
    WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1  {}
    and fr.school_type in (3,4) and tt.task_type in (14)  and tt.classroom_id is null and s.school_id = fr.school_id  and tt.c_time is not null
    GROUP BY date,fr.school_id
    '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


def task_xs(time):
    sql = '''
    SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'xs'
    FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
    WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1  {}
    and fr.school_type in (3,4) and tt.task_type in (15)  and tt.classroom_id is null and s.school_id = fr.school_id  and tt.c_time is not null
    GROUP BY date,fr.school_id
    '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


def task_axp(time):
    sql = '''
        SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'axp'
        FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
        WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0  and tc.LOCAL_STATUS = 1 and tt.c_time is not null
        and fr.school_type in (3,4)  and tt.classroom_id is not  null and s.school_id = fr.school_id {}
        GROUP BY date,fr.school_id
        '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


def tas_dtk_lxc(time):
    sql = '''
        select DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'dtk_lxc' 
            from tp_task_info  tt ,as_answer_sheet_info aasi,tp_course_info tc,franchised_school_info fr,school_info s
            where tt.task_type =13 and tt.TASK_VALUE_ID = aasi.paper_id  and aasi.practice_book_id is not null and tt.publish_status  =1 and tt.c_time is not null and tt.video_id is null
            and tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1 and fr.school_type in (3,4)  
            and tt.classroom_id is null and s.school_id = fr.school_id  {}
            GROUP BY date,fr.school_id
        '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


def task_dtk_fj(time):
    sql = '''
        select DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'dtk_fj' 
            from tp_task_info  tt ,as_answer_sheet_info aasi,tp_course_info tc,franchised_school_info fr,school_info s
            where tt.task_type =13 and tt.TASK_VALUE_ID = aasi.paper_id   and aasi.meta_type = 1 and tt.publish_status  =1  and tt.video_id is null and tt.c_time is not null
            and tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1 and fr.school_type in (3,4)  
            and tt.classroom_id is null and s.school_id = fr.school_id {}
            GROUP BY date,fr.school_id
        '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


def task_dtk_sj(time):
    sql = '''
        select DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'dtk_sj' 
            from tp_task_info  tt ,as_answer_sheet_info aasi,tp_course_info tc,franchised_school_info fr,school_info s
            where tt.task_type =13 and tt.TASK_VALUE_ID = aasi.paper_id   and aasi.meta_type = 3 and tt.publish_status  =1  and tt.video_id is null and tt.c_time is not null
            and tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1 and fr.school_type in (3,4)  
            and tt.classroom_id is null and s.school_id = fr.school_id {}
            GROUP BY date,fr.school_id
        '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


def task_hp(time):
    sql = '''
                SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'hp'
                    FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
                    WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1 and tt.c_time is not null
                    and fr.school_type in (3,4)  and tt.classroom_id is null  and  tt.correct_model = 1  and s.school_id = fr.school_id {}
                    GROUP BY date,fr.school_id
                '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


def task_zp(time):
    sql = '''
                SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as 'date',fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'zp'
                    FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
                    WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1 and tt.c_time is not null
                    and fr.school_type in (3,4)  and tt.classroom_id is null  and  tt.correct_model = 2  and s.school_id = fr.school_id  {}
                    GROUP BY date,fr.school_id
                '''.format(time)
    task = mysql_connect(sql)
    task_df_list.append(task)


@cost_time
def school_info():
    sql = '''    
    SELECT s.school_id,s.name,s.province,s.city, fr.c_time , fr.validity_time ,s.ip,uu.user_name,uu.password FROM oracle2utf.coschuser_info uu,user_info u,j_role_user ru,school_info s , franchised_school_info fr 
        WHERE uu.jid = u.ett_user_id
        and fr.school_id = s.school_id 
        and fr.school_type  in (3,4 )
          AND u.dc_school_id = s.school_id
          AND u.ref = ru.user_id
          AND ru.role_id = 4
        and fr.ENABLE != 1
          GROUP BY u.user_id
                '''
    task = mysql_connect(sql)
    write_Sqlite(df=task, if_exists='replace', table_name='school_info')


@cost_time
def day_school_task(c_time):
    funs = [task_yb, task_xzy, task_tl, task_dl, task_cy, task_wkc, task_zbk, task_dtk, task_gxh, task_xs, task_axp,
            tas_dtk_lxc, task_dtk_fj, task_dtk_sj, task_hp, task_zp]

    # 线程池子
    threads = []
    # 一个函数一个线程,添加到池子
    for i in funs:
        t = threading.Thread(target=i, kwargs={'time': c_time})
        threads.append(t)
    # 开启线程
    for i in threads:
        # 线程保护
        i.setDaemon(True)
        i.start()
    print('开启线程数量：{}'.format(len(threading.enumerate())))
    # 所有子线程结束以后才执行后面
    for i in threads:
        i.join()

    task_df = df_merge(on=['date', 'name', 'school_id', 'province', 'city'], how='outer', df=task_df_list)
    print('合并表格完成')

    # replace清空后添加，，append追加
    if c_time == '':
        write_Sqlite(df=task_df, table_name='day_school_task', if_exists='replace')
    else:
        write_Sqlite(df=task_df, table_name='day_school_task', if_exists='append')
    threads.clear()
    task_df_list.clear()


@cost_time
def year_province_count():
    provinceInfo = pd.DataFrame(
        data=['台湾', '黑龙江', '内蒙古', "吉林", '北京', "辽宁", "河北", "天津", "山西", "陕西", "甘肃", "宁夏", "青海", "新疆", "西藏", "四川", "重庆",
              "山东", "河南", "江苏", "安徽", "湖北", "浙江", "福建", "江西", "湖南", "贵州", "云南", "广东", "广西", "海南", '上海'],
        columns=['province'])
    years = {'y22_23_2': ['2023-01-15', '2023-07-15'],'y22_23_1': ['2022-07-15', '2023-01-15'],
             'y21_22_2': ['2022-01-15', '2022-07-15'],'y21_22_1': ['2021-07-15', '2022-01-15'],
             'y20_21_2': ['2021-01-15', '2021-07-15'],'y20_21_1': ['2020-07-15', '2021-01-15'],
             'y19_20_2': ['2020-01-15', '2020-07-15'],'y19_20_1': ['2019-07-15', '2020-01-15'],
             'y18_19_2': ['2019-01-15', '2019-07-15'],'y18_19_1': ['2018-07-15', '2019-01-15'],
             'y17_18_2': ['2018-01-15', '2018-07-15'],'y17_18_1': ['2017-07-15', '2018-01-15'],
             }
    sql = '''
        select * from day_school_task 
        order by date 
        '''
    sql_data = sqlite_connect(sql)
    sql_data['school_id'] = sql_data['school_id'].astype('str')

    year_province_data = []
    for k, v in years.items():
        data = (sql_data[(sql_data['date'] >= v[0]) & (sql_data['date'] < v[1])]).groupby(
            ['school_id', 'name', 'province'], as_index=False).sum().groupby(
            by=['province'], as_index=False).count().iloc[:, 0:2]
        data = df_merge(on=['province'], how='left', df=[provinceInfo, data])
        data.columns = ['province', '{}'.format(k)]
        year_province_data.append(data)
    year_province_df = df_merge(on=['province'], how='left', df=year_province_data)

    write_Sqlite(df=year_province_df, table_name='year_province_data', if_exists='replace')
    year_province_data.clear()
    # return year_province_df

@cost_time
def pad_license_dau(b_time,e_time,group_by_time,index,table_name,if_exists):
    body = '''
    {
      "size": 0,
      "query": {
        "bool": {
          "must": [
            {
              "term": {
                "app_name": {
                  "value": "aiStudy"
                }
              }
            },
            {
              "range": {
                "process_time": {
                  "gte": "%s",
                  "lte": "%s"
                }
              }
            },
            {
              "range": {
                "message_type": {
                  "gte": 1,
                  "lte": 100
                }
              }
            },
            {
              "term": {
                "return_result": {
                  "value": "1"
                }
              }
            }
          ]
        }
      },
      "aggs": {
        "distinctjId": {
          "cardinality": {
            "field": "jId"
          }
        },
        "group_by_time":{
          "date_histogram": {
            "field": "process_time",
            "interval": "%s"
          },
          "aggs": {
            "disjId": {
              "cardinality": {
                "field": "jId"
              }
            }
          }
        }
      }
    }
    ''' % (b_time, e_time,group_by_time)
    HEADERS = {
        'Content-Type': 'application/json',
        'kbn-xsrf': 'true',
    }

    url = 'http://52.82.30.42:5601/api/console/proxy?path={}/_search&method=POST'.format(index)
    res = requests.post(url=url, verify='path', auth=('kibana', 'etiantian2018!'), data=body, headers=HEADERS)
    res = json.loads(res.text)
    data = res['aggregations']['group_by_time']['buckets']
    df_list = []
    for i in data:
        df = pd.DataFrame.from_dict(i, orient='index').T
        df['disJid'] = i['disjId']['value']
        df_list.append(df)
    res_df = pd.concat(df_list, axis=0, ignore_index=True)
    res_df = res_df.loc[:, ['key_as_string', 'doc_count', 'disJid']]
    res_df.columns = ['time', 'pv', 'uv']
    write_Sqlite(df=res_df, table_name=table_name, if_exists=if_exists)
    df_list.clear()


if __name__ == '__main__':

    c_time = "and tt.c_time >= '2023-01-15 00:00:00'"
    # 同步每天学校任务数
    schedule.every(2).hours.do(day_school_task,c_time)
    # 计算学年省市学校数
    schedule.every(2).hours.do(year_province_count)
    # 学校列表
    schedule.every(2).hours.do(school_info)

    # 学习机活跃度
    now_time = pd.to_datetime(datetime.datetime.now())
    b_time = (now_time - pd.to_timedelta(1, unit='d')).strftime("%Y-%m-%d 00:00:00")
    e_time = now_time.strftime("%Y-%m-%d 00:00:00")
    index = 'message_log'
    print(b_time)
    print(e_time)
    schedule.every().day.at("05:00").do(pad_license_dau,b_time,e_time,'1h',index,'pad_license_dau_h','append')
    schedule.every().day.at("05:10").do(pad_license_dau,b_time,e_time,'1d',index,'pad_license_dau','append')

    while True:
        schedule.run_pending()
        time.sleep(1)

