from functools import reduce

from sqlalchemy import create_engine
import pandas as pd


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


def yearSchoolCount(df, beginTime, endTime):
    provinceInfo = pd.DataFrame(
        data=['台湾', '黑龙江', '内蒙古', "吉林", '北京', "辽宁", "河北", "天津", "山西", "陕西", "甘肃", "宁夏", "青海", "新疆", "西藏", "四川", "重庆",
              "山东", "河南",
              "江苏", "安徽", "湖北", "浙江", "福建", "江西", "湖南", "贵州", "云南", "广东", "广西", "海南", '上海'], columns=['province'])

    data = (df[(df['date'] >= beginTime )& (df['date'] < endTime)]).groupby(['school_id', 'name', 'province'],as_index=False).sum().groupby(by=['province'],
                                                                                      as_index=False).count().iloc[:,0:2]
    data = reduce(lambda left, right: pd.merge(left, right, on=['province'], how='left'), [provinceInfo, data])
    data = data.set_index('province')
    data = data.fillna(0)
    count = data['school_id'].sum()
    data = data.to_dict(orient='dict')['school_id']

    return  data,count
