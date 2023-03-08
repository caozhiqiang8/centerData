import time
from public.db_con import es_connect
import  json
import  pandas as pd

body = '''
    {
      "query": {
        "bool": {
          "must": [
            {
              "term": {
                "url.keyword": {
                  "value": "http://school-api.ai-classes.com/app-common-service/checkAppVersionWithCache.do"
                }
              }
            }
          ]
        }
      },
      "size": 0
    }
    '''

hits_list = []
b_num = 0
e_num = 10000
while True:
    body = '''
    {
      "query": {
        "bool": {
          "must": [
            {
              "term": {
                "url.keyword": {
                  "value": "http://school-api.ai-classes.com/app-common-service/checkAppVersionWithCache.do"
                }
              }
            }
          ]
        }
      },
      "from":%s,
      "size": %s
    }
    '''%(b_num,e_num)
    index = 'action_logs_20230223'

    data = es_connect(index=index, body=body)
    total = data['hits']['total']
    if total < b_num:
        break
    else:
        hits = data['hits']['hits']
        hits_list.extend(hits)

    b_num+=10000
    e_num+=10000
    print(b_num)
    time.sleep(1)

df_list = []

for i in hits_list:
    sourse_data = i['_source']
    sourse_data_df = pd.json_normalize(sourse_data)

    param_json = json.loads(sourse_data['param_json'])
    param_json_df = pd.json_normalize(param_json)
    df = pd.merge(sourse_data_df,param_json_df,how='left')
    df_list.append(df)

df = pd.concat(df_list,axis=0,ignore_index=True)
df.to_excel(r'F:\软件下载\文件.xlsx')
print(df)
