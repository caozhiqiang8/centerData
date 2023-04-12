import json
from elasticsearch import Elasticsearch
from sqlalchemy import create_engine
import pandas as pd
import sqlite3
import  os,sys

# 链接ES
def es_connect(index, body):
    es_hosts = str("69.230.239.155,43.192.117.34").split(",")
    es = Elasticsearch(es_hosts)
    res = es.search(index=index, body=body)
    res = json.loads(json.dumps(res))
    return res


# 链接mysql -----dataFrame
def mysql_connect(sql):
    engine = create_engine(
        'mysql+pymysql://schu:slavep@123.103.75.152:3306/school')
    result = pd.read_sql_query(sql=sql, con=engine)
    return result

sqllite_path =r'F:\PythonObject\DataCenterDB.sqlite3'
# sqllite_path =r'D:\DataCenterDB.sqlite3'

# 链接sqlite---dataFrame
def sqlite_connect(sql):
    # sqllite_path = os.path.abspath('DataCenterDB.sqlite3')
    engine = create_engine('sqlite:///{}'.format(sqllite_path))
    result = pd.read_sql(sql=sql, con=engine)
    return result


#  插入数据
def write_Sqlite(df, table_name, if_exists):
    # if_exists: replace  清空后添加，，append  追加
    # sqllite_path = os.path.abspath('DataCenterDB.sqlite3')
    con = sqlite3.connect(sqllite_path)
    rs = con.cursor()
    if table_name == 'day_school_task':
        if if_exists == 'append':
            # 删除数据学期数据 和 空 数据
            del_sql = ''' 
                    DELETE from day_school_task where date >='2023-01-15'
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
        df['zuoye_count'] = df['xzy'] + df['tl'] + df['wkc'] + df['yb'] + df['zbk'] + df['gxh'] + df['xs'] + df[
            'new_dtk']
        df['task_count'] = df['zuoye_count'] + df['axp']

    df.to_sql(name=table_name, con=con, if_exists=if_exists, index=False)

    print('插入数据库完成')


if __name__ == '__main__':

    print(sys.argv[0])
    print(os.path.abspath('..\\DataCenterDB.sqlite3'))
    print(os.path.abspath(__file__))
