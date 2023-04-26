import pandas as pd
from public.db_con import  mysql_connect,es_formal_connect

sg_id = 35
sql = '''
	SELECT school_id from sg_j_group_school where sg_id = {}
'''.format(sg_id)
school_id = mysql_connect(sql)['school_id'].to_list()
print(school_id)

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
    '''%(school_id)
res1 = es_formal_connect(body,class_subject_date_teacher_stat_index)
data1 = res1['aggregations']['groupby']['buckets']
df_list1 = []
for i in data1:
    df = pd.DataFrame.from_dict(i, orient='index').T
    df['sum_task_num'] = i['sum_task_num']['value']
    df['sum_course_num'] = i['sum_course_num']['value']
    df_list1.append(df)
res_df1 = pd.concat(df_list1, axis=0, ignore_index=True)
res_df1 = res_df1.drop(['doc_count'],axis=1)

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
'''%(school_id)
res2 = es_formal_connect(body,teacher_date_stat_index)
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
res_df2 = res_df2.drop(['doc_count'],axis=1)

df = pd.merge(res_df1,res_df2,on='key',how = 'outer')
df = df.rename(columns={'key':'user_id'})
df['user_id'] = df['user_id'].astype('int')
user_id_lsit = df['user_id'].to_list()

sql = '''
select u.user_id,t.teacher_name,s.name  from user_info u,teacher_info t,school_info s   where u.ref = t.user_id and s.school_id = u.dc_school_id  and u.user_id in {}
'''.format(tuple(user_id_lsit))
tea_name  = mysql_connect(sql)

df = pd.merge(tea_name,df,on='user_id',how = 'outer')
df = df.fillna(0)
df.columns = ['用户ID','教师姓名','学校名称','任务总数','课程总数','上传资源次数','下载资源次数','浏览次数','收藏资源数']

df.to_excel(r'C:\Users\caozhiqiang\Desktop\数据.xlsx',index=False)
print('导出成功')