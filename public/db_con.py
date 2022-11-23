import json
from functools import reduce
from elasticsearch import Elasticsearch
from sqlalchemy import create_engine
import pandas as pd
import sqlite3


#链接ES
def esConnect(index,body):
    es_hosts = str("52.82.47.234,52.83.95.66").split(",")
    es = Elasticsearch(es_hosts)
    res = es.search(index=index, body=body)
    res = json.loads(json.dumps(res))
    return res

# 链接mysql -----dataFrame
def mysqlDB(sql):
    engine = create_engine(
        'mysql+pymysql://schu:slavep@123.103.75.152:3306/school')
    result = pd.read_sql_query(sql=sql, con=engine)
    return result


# 链接sqlite---dataFrame
def sqliteDB(sql):
    engine = create_engine('sqlite:///F:\\PythonObject\\DataCenterDB.sqlite3')
    result = pd.read_sql(sql=sql, con=engine)
    return result


class SqliteDb(object):

    def __init__(self, sql):
        self.sql = sql

    def connectDb(self):
        engine = create_engine('sqlite:///F:\\PythonObject\\DataCenterDB.sqlite3')
        result = pd.read_sql(sql=self.sql, con=engine)
        return result

    def toJson(self, df):
        result = json.loads(df.to_json(orient='records', force_ascii=False))
        return result

#  插入数据
def toSqlite(df, table_name, if_exists ):
    con = sqlite3.connect('F:\\PythonObject\\DataCenterDB.sqlite3')
    rs = con.cursor()
    if table_name =='day_school_task':
        if if_exists == 'append':
            # 删除数据学期数据 和 空 数据
            del_sql = ''' 
                    DELETE from day_school_task where date >='2022-07-15'
                    '''
            rs.execute(del_sql)
            con.commit()
            del_sql = ''' 
                    DELETE from day_school_task where date ='0'
                    '''
            rs.execute(del_sql)
            con.commit()
            print('删除数据学期数据和空数据完成')

        df['new_dtk'] = df['cy'] + df['dtk'] + df['dt']
        df['zuoye_count'] = df['xzy'] + df['tl'] + df['wkc'] + df['yb'] + df['zbk'] + df['gxh'] + df['xs'] + df['new_dtk']
        df['task_count'] = df['zuoye_count'] + df['axp']

    df.to_sql(name=table_name, con=con, if_exists=if_exists, index=False)

    print('插入数据库完成')


def yearSchoolCount(df, beginTime, endTime):
    provinceInfo = pd.DataFrame(
        data=['台湾', '黑龙江', '内蒙古', "吉林", '北京', "辽宁", "河北", "天津", "山西", "陕西", "甘肃", "宁夏", "青海", "新疆", "西藏", "四川", "重庆",
              "山东", "河南", "江苏", "安徽", "湖北", "浙江", "福建", "江西", "湖南", "贵州", "云南", "广东", "广西", "海南", '上海'], columns=['province'])

    data = (df[(df['date'] >= beginTime) & (df['date'] < endTime)]).groupby(['school_id', 'name', 'province'], as_index=False).sum().groupby( by=['province'], as_index=False).count().iloc[:, 0:2]
    data = reduce(lambda left, right: pd.merge(left, right, on=['province'], how='left'), [provinceInfo, data])
    data = data.set_index('province')
    data = data.fillna(0)
    count = data['school_id'].sum()
    data = data.to_dict(orient='dict')['school_id']
    print('完成')
    return data, count


if __name__ == '__main__':
#     body = '''
#     {"query": {
#   "bool": {
#     "must": [
#       {"range": {
#         "responseSize": {
#           "gt": 0
#         }
#       }}
#     ]
#   }
# }
#   , "size": 5000
# }
#     '''
#     data = esConnect(index = 'action_logs_20220923',body=body)
#     data = json.loads(json.dumps(data))
#     data = data['hits']['hits']

#     res = []
#     for i in data:
#         res.append(i['_source'])
#     data = pd.DataFrame(res)
#     print('导出完成')
#
#     data.to_excel(r'C:\Users\caozhiqiang\Desktop\行为.xlsx')

    #显示所有列
    pd.set_option('display.max_columns', None)
    #显示所有行
    # pd.set_option('display.max_rows', None)
    #设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth',100)

    res = pd.read_excel(r'C:\Users\caozhiqiang\Desktop\行为.xlsx')[:1]
    model_name = (res.groupby(['model_name']).nunique()).index.tolist()
    # model_name = ['business-service-answersheet','getStatus.do','business-service-general']
    print(model_name)
    x_data = res['process_time'].tolist()
    print(x_data)
    y_data = []

    # res1 = res[res['model_name'] == 'getStatus.do']
    # df_merge = pd.merge(res,res1,on='process_time',how='left')
    # print(df_merge)
    # y_list = df_merge['responseSize_y'].tolist()
    # print(y_list)

    for i in model_name:
        res1 = res[res['model_name'] == '{}'.format(i)]
        df_merge = pd.merge(res,res1,on='process_time',how='left')
        y_list = df_merge['responseSize_y'].tolist()
        y_data.append(y_list)

    print(y_data)