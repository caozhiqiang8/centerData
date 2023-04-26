import json
from school import school_blue
from flask import render_template,request
from public.db_con import sqlite_connect, mysql_connect,es_formal_connect
import pandas as pd


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


@school_blue.route('/schoolInfo', methods=['get','post'])
def schoolInfo():
    data = json.loads(request.get_data())
    school_name = data['school_name']
    school_id  = data['school_id']
    print(data)
    if school_name:
        sql = '''
                select * from school_info where name  like '%{}%'
                '''.format(school_name)
    elif school_id :
        sql = '''
                      select * from school_info where school_id = '{}'
                      '''.format(school_id)

    schoolInfo = sqlite_connect(sql)

    schoolInfo = json.loads(schoolInfo.to_json(orient='records', force_ascii=False))

    data = {
        'schoolInfo': schoolInfo
    }
    return data


@school_blue.route('/sgData',methods =['get','post'])
def sgData():
    data = json.loads(request.get_data())
    sg_id = data['sg_id']
    print('校群ID',sg_id)

    sql = '''
    	SELECT school_id from sg_j_group_school where sg_id = {}
    '''.format(sg_id)
    school_id = mysql_connect(sql)['school_id'].to_list()

    # 教师任务数据查询
    class_subject_date_teacher_stat_index = 'class_subject_date_teacher_stat'
    body = '''
        {
      "query": {
        "bool": {
          "must": [
            {
              "terms": {
                "dc_school_id": %s
              }
            },
            {
              "range": {
                "date": {
                  "gte": "2023-01-15"
                }
              }
            }
          ]
        }
      },
      "aggs": {
        "groupby": {
          "terms": {
            "field": "teacher_user_id",
            "size": 1000
          },
          "aggs": {
            "sum_course_num": {
              "sum": {
                "field": "course_num"
              }
            },
            "sum_task_num": {
              "sum": {
                "field": "task_num"
              }
            }
          }
        }
      },
      "size": 0
    }
        ''' % (school_id)
    res1 = es_formal_connect(body, class_subject_date_teacher_stat_index)
    data1 = res1['aggregations']['groupby']['buckets']
    df_list1 = []
    for i in data1:
        df = pd.DataFrame.from_dict(i, orient='index').T
        df['sum_task_num'] = i['sum_task_num']['value']
        df['sum_course_num'] = i['sum_course_num']['value']
        df_list1.append(df)
    res_df1 = pd.concat(df_list1, axis=0, ignore_index=True)
    res_df1 = res_df1.drop(['doc_count'], axis=1)

    # 教师资源浏览数据查询
    teacher_date_stat_index = 'teacher_date_stat'
    body = '''
    {
      "query": {
        "bool": {
          "must": [
            {
              "terms": {
                "dc_school_id": %s
              }
            },
            {
              "range": {
                "date": {
                  "gte": "2023-01-15"
                }
              }
            }
          ]
        }
      },
      "aggs": {
        "groupby": {
          "terms": {
            "field": "user_id",
            "size": 1000
          },
          "aggs": {
            "group_upload_res_num": {
              "sum": {
                "field": "upload_res_num"
              }
            },
            "group_view_res_num": {
              "sum": {
                "field": "view_res_num"
              }
            },
            "group_download_res_num": {
              "sum": {
                "field": "download_res_num"
              }
            },
            "group_collection_res_distinct_num": {
              "sum": {
                "field": "collection_res_distinct_num"
              }
            }
          }
        }
      },
      "size": 0
    }
    ''' % (school_id)
    res2 = es_formal_connect(body, teacher_date_stat_index)
    data2 = res2['aggregations']['groupby']['buckets']
    df_list2 = []
    for i in data2:
        df = pd.DataFrame.from_dict(i, orient='index').T
        df['group_upload_res_num'] = i['group_upload_res_num']['value']
        df['group_download_res_num'] = i['group_download_res_num']['value']
        df['group_view_res_num'] = i['group_view_res_num']['value']
        df['group_collection_res_distinct_num'] = i['group_collection_res_distinct_num']['value']
        df_list2.append(df)
    res_df2 = pd.concat(df_list2, axis=0, ignore_index=True)
    res_df2 = res_df2.drop(['doc_count'], axis=1)

    # 合并表格
    df = pd.merge(res_df1, res_df2, on='key', how='outer')
    df = df.rename(columns={'key': 'user_id'})
    df['user_id'] = df['user_id'].astype('int')
    user_id_lsit = df['user_id'].to_list()
    # 查询教师真实姓名
    sql = '''
    select u.user_id,t.teacher_name,s.name  from user_info u,teacher_info t,school_info s   where u.ref = t.user_id and s.school_id = u.dc_school_id  and u.user_id in {}
    '''.format(tuple(user_id_lsit))
    tea_name = mysql_connect(sql)
    # 合并
    df = pd.merge(tea_name, df, on='user_id', how='outer')
    df = df.fillna(0)
    df.columns = ['用户ID', '教师姓名', '学校名称', '任务总数', '课程总数', '上传资源次数', '下载资源次数', '浏览次数', '收藏资源数']

    sg_data = json.loads(df.to_json(orient='records', force_ascii=False))
    data = {
        'sg_data':sg_data
    }
    return data