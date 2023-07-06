from elasticsearch import Elasticsearch
import json
import pandas as pd
from public.db_con import mysql_connect
from datetime import  datetime

def esConnect(index,body):

    es_hosts = str("69.230.239.155,43.192.117.34").split(",")
    es = Elasticsearch(es_hosts)
    res = es.search(index=index, body=body)
    res = json.loads(json.dumps(res))
    return  res

index = "two_month_action_logs"
mounth = '2023-03'
# b_time = "{}-01 00:00:00".format(mounth)
# e_time = "{}-30 23:59:59".format(mounth)

b_time = "2023-03-05 00:00:00"
e_time = "2023-05-30 23:59:59"

school_id = 100002530

body = '''{
  "query": {
    "bool": {
      "must": [
      {
         "wildcard": {
           "url.keyword": "*tpres/resource/infos*"
         }
        },{
          "term": {
            "school_id": {
              "value": "%s"
            }
          }
        },
        {
          "range": {
            "c_time": {
              "gte":"%s",
              "lte": "%s"
            }
          }
        }
      ]
    }
  },
  "size": 0,"aggs": {
    "groupBy": {
      "terms": {
        "field": "jid",
        "size": 2000
      }
    }
  }
}'''%(school_id,b_time,e_time)

res = esConnect(index,body)
res = res['aggregations']['groupBy']['buckets']
df = pd.DataFrame(res)


body2 = '''
{
  "query": {
    "bool": {
      "must": [
      {
         "wildcard": {
           "url.keyword": "*/tpres/video/line*"
         }
        },{
          "term": {
            "school_id": {
              "value": "%s"
            }
          }
        },
        {
          "range": {
            "c_time": {
              "gte": "%s",
              "lte": "%s"
            }
          }
        }
      ]
    }
  },
  "size": 0,"aggs": {
    "groupBy": {
      "terms": {
        "field": "jid",
        "size": 2000
      }
    }
  }
}

'''%(school_id,b_time,e_time)
res2 = esConnect(index,body2)
res2 = res2['aggregations']['groupBy']['buckets']
df2 = pd.DataFrame(res2)


df.columns = ['JID','资源总数']
df2.columns = ['JID','微课总数']

df_merge = pd.merge(df,df2,on='JID',how='outer')
print(df_merge)

sql = '''
SELECT c.class_grade,c.class_name ,s.stu_name,u.ett_user_id as 'JID'  
from class_info c, j_class_user jc , student_info s,user_info u  
where c.dc_school_id = {} and c.year = '2022~2023' and c.class_id = jc.class_id and jc.user_id = s.user_id   and u.ref = s.user_id 
'''.format(school_id)
stu_info = mysql_connect(sql)
stu_res = pd.merge(stu_info,df_merge,on='JID',how='left')
stu_res = stu_res.fillna(0)

print(stu_res)
stu_res.to_excel(r'C:\Users\caozhiqiang\Desktop\{}月份{}学生资源使用数据.xlsx'.format(mounth,school_id))
print('导出成功')