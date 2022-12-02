from public.db_con import sqlite_connect, write_Sqlite
from public.df_merge import df_merge
import numpy as np
from public.record_time import cost_time

TASK = 30
# 加一个学期 str_type 就要加一个
terms = {

    'term_22_1': ['2022-07-15', '2023-01-15'],

    'term_21_2': ['2022-01-15', '2022-07-15'],
    'term_21_1': ['2021-07-15', '2022-01-15'],

    'term_20_2': ['2021-01-15', '2021-07-15'],
    'term_20_1': ['2020-07-15', '2021-01-15'],

    'term_19_2': ['2020-01-15', '2020-07-15'],
    'term_19_1': ['2019-07-15', '2020-01-15'],

    'term_18_2': ['2019-01-15', '2019-07-15'],
    'term_18_1': ['2018-07-15', '2019-01-15'],

    'term_17_2': ['2018-01-15', '2018-07-15'],
    'term_17_1': ['2017-07-15', '2018-01-15'],

    'term_16_2': ['2017-01-15', '2017-07-15'],
    'term_16_1': ['2016-07-15', '2017-01-15'],

    'term_15_2': ['2016-01-15', '2016-07-15'],
    'term_15_1': ['2015-07-15', '2016-01-15'],

    'term_14_2': ['2015-001-15', '2015-7-15'],
    'term_14_1': ['2014-07-15', '2015-01-15'],

}

def str_type(type):
    if type[0] == '0' and '1' in type[1:]:
        return '流失学校'
    elif type[0] == '1' and type[1:] == '0' * (len(type) - 1):
        return '新开学校'
    elif type == '0' * (len(type)):
        return '僵尸学校'
    elif type[:1] == '1' and type[1:2] == '0' and '1' in type[3:]:
        return '回归学校'
    elif type[:2] == '1' * len(type[:2]) and type[2:] == '0' * len(type[2:]):
        return '使用了2个学期'
    elif type[:3] == '1' * len(type[:3]) and type[3:] == '0' * len(type[3:]):
        return '使用了3个学期'
    elif type[:4] == '1' * len(type[:4]) and type[4:] == '0' * len(type[4:]):
        return '使用了4个学期'
    elif type[:5] == '1' * len(type[:5]) and type[5:] == '0' * len(type[5:]):
        return '使用了5个学期'
    elif type[:6] == '1' * len(type[:6]) and type[6:] == '0' * len(type[6:]):
        return '使用了6个学期'
    elif type[:7] == '1' * len(type[:7]) and type[7:] == '0' * len(type[7:]):
        return '使用了7个学期'
    elif type[:8] == '1' * len(type[:8]) and type[8:] == '0' * len(type[8:]):
        return '使用了8个学期'
    elif type[:9] == '1' * len(type[:9]) and type[9:] == '0' * len(type[9:]):
        return '使用了9个学期'
    elif type[:10] == '1' * len(type[:10]) and type[10:] == '0' * len(type[10:]):
        return '使用了10个学期'
    elif type[:11] == '1' * len(type[:11]) and type[11:] == '0' * len(type[11:]):
        return '使用了11个学期'
    elif type[:12] == '1' * len(type[:12]) and type[12:] == '0' * len(type[12:]):
        return '使用了12个学期'
    elif type[:13] == '1' * len(type[:13]) and type[13:] == '0' * len(type[13:]):
        return '使用了13个学期'
    elif type[:14] == '1' * len(type[:14]) and type[14:] == '0' * len(type[14:]):
        return '使用了14个学期'
    elif type[:15] == '1' * len(type[:15]) and type[15:] == '0' * len(type[15:]):
        return '使用了15个学期'
    elif type[:16] == '1' * len(type[:16]) and type[16:] == '0' * len(type[16:]):
        return '使用了16个学期'
    elif type[:17] == '1' * len(type[:17]) and type[16:] == '0' * len(type[17:]):
        return '使用了17个学期'
    else:
        return '回归学校'


@cost_time
def school_crm():
    term_school = []

    # 所有学校列表
    school_sql = '''
    SELECT school_id ,name  from school_info
    '''
    term_school.append(sqlite_connect(school_sql))

    # 计算每个学期学校数量
    for k, v in terms.items():
        sql = '''
         select school_id,name,task_count from day_school_task  where date >= '{}' and date < '{}'
        order by date DESC 
         '''.format(v[0], v[1])
        data = sqlite_connect(sql)
        data = data.groupby(['school_id'], as_index=False).sum()
        data.columns = ['school_id', '{}'.format(k)]
        term_school.append(data)
    school_term_task = df_merge(on=['school_id'], how='left', df=term_school)

    # 学校每个学期的数量转化为 1 0
    column = school_term_task.columns[2:]
    for i in range(len(column)):
        school_term_task['{}'.format(i + 1)] = np.where(school_term_task[column[i]] >= TASK, 1, 0)
    # 合并 1 0
    for i in range(len(column) - 1):
        if i == 0:
            school_term_task['type'] = school_term_task['{}'.format(i + 1)].map(str) + school_term_task[
                '{}'.format(i + 2)].map(str)
        else:
            school_term_task['type'] = school_term_task['type'].map(str) + school_term_task['{}'.format(i + 2)].map(str)
    # 删除没用的列
    school_term_task = school_term_task.drop(axis=1, columns=school_term_task.columns[19:-1].tolist())
    # 调用 1 0 转化
    school_term_task['type'] = school_term_task['type'].apply(lambda x: str_type(x))
    # 插入数据库
    write_Sqlite(df=school_term_task, table_name='school_crm', if_exists='replace')


if __name__ == '__main__':
    school_crm()
