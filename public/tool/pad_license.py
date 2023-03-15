import pandas as pd
import requests
import json


b_time = '2023-03-08 00:00:00'
e_time = '2023-03-09 00:00:00'
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
        "interval": "1h"
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
'''%(b_time,e_time)
HEADERS = {
     'Content-Type': 'application/json',
     'kbn-xsrf': 'true',
}
index= 'message_log'
url = 'http://52.82.30.42:5601/api/console/proxy?path={}/_search&method=POST'.format(index)

res = requests.post(url=url,verify='path',auth=('kibana','etiantian2018!'),data=body,headers = HEADERS)
res = json.loads(res.text)
print(res['aggregations']['distinctjId']['value'])

data = res['aggregations']['group_by_time']['buckets']

df_list = []
for i in data :
    df =pd.DataFrame.from_dict(i, orient='index').T
    df['disJid'] = i['disjId']['value']
    df_list.append(df)
res_df = pd.concat(df_list,axis=0,ignore_index=True)
print(res_df)

