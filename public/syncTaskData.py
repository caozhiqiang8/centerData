import sqlite3
import pandas as pd
import datetime
from functools import reduce
from public.sqlDB import mysqlDB, sqliteDB


def taskToSqlite(time):
    '''  1=资源  2=讨论  3=单个试题  4=测验（试卷）  5=自测  6=微课程  789=一般任务（语音）  10=直播课   11=奇异单项（酷蒙）  13=答题卡  14=个性化任务  15=先声任务 '''
    task_type = [1, 2, 3, 4, 6, 7, 10, 13, 14, 15, 100, 101, 102, 103, 104, 105]
    column = ['date', 'school_id', 'name', 'province', 'city', 'xzy', 'tl', 'dt', 'cy', 'wkc', 'yb', 'zbk', 'dtk',
              'gxh', 'xs', 'axp', 'dtk_hp', 'dtk_zp', 'dtk_lxc', 'dtk_fj', 'dtk_sj']
    task_df_all = []

    con = sqlite3.connect('F:\\PythonObject\\DataCenterDB.sqlite3')
    rs = con.cursor()

    for i in task_type:
        if i == 7:
            sql = '''
                SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as time,fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'yb'
                FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
                WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1  {}
                and fr.school_type in (3,4) and tt.task_type in (7,8,9)  and tt.classroom_id is null and s.school_id = fr.school_id  and tt.c_time is not null
                GROUP BY time,fr.school_id
                '''.format(time)
            task = mysqlDB(sql)
            task_df_all.append(task)
        elif i == 6:
            sql = '''
                SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as time,fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'wkc'
                FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
                WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 
                and tc.LOCAL_STATUS = 1 and tt.c_time is not null and fr.school_type in (3,4) and ( ( tt.task_type =13 
                and video_id is not  null) or tt.task_type =6)   and tt.classroom_id is null and s.school_id = fr.school_id  {}
                GROUP BY time,fr.school_id
                '''.format(time)
            task = mysqlDB(sql)
            task_df_all.append(task)
        elif i == 13:
            sql = '''
                SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as time,fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'dtk'
                FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
                WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0  and tc.LOCAL_STATUS = 1 and tt.c_time is not null
                and fr.school_type in (3,4) and tt.task_type =13 and tt.video_id is null  and tt.classroom_id is null and s.school_id = fr.school_id {}
                GROUP BY time,fr.school_id
                '''.format(time)
            task = mysqlDB(sql)
            task_df_all.append(task)
        elif i == 100:
            sql = '''
                SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as time,fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'axp'
                FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
                WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0  and tc.LOCAL_STATUS = 1 and tt.c_time is not null
                and fr.school_type in (3,4)  and tt.classroom_id is not  null and s.school_id = fr.school_id {}
                GROUP BY time,fr.school_id
                '''.format(time)
            task = mysqlDB(sql)
            task_df_all.append(task)
        elif i == 101:
            sql = '''
            SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as time,fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'hp'
                FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
                WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1 and tt.c_time is not null
                and fr.school_type in (3,4)  and tt.classroom_id is null  and  tt.correct_model = 1  and s.school_id = fr.school_id {}
                GROUP BY time,fr.school_id
            '''.format(time)
            task = mysqlDB(sql)
            task_df_all.append(task)
        elif i == 102:
            sql = '''
            SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as time,fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'zp'
                FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
                WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1 and tt.c_time is not null
                and fr.school_type in (3,4)  and tt.classroom_id is null  and  tt.correct_model = 2  and s.school_id = fr.school_id  {}
                GROUP BY time,fr.school_id
            '''.format(time)
            task = mysqlDB(sql)
            task_df_all.append(task)
        elif i == 103:
            sql = '''
            select DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as time,fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'dtk_lxc' 
            from tp_task_info  tt ,as_answer_sheet_info aasi,tp_course_info tc,franchised_school_info fr,school_info s
            where tt.task_type =13 and tt.TASK_VALUE_ID = aasi.paper_id  and aasi.practice_book_id is not null and tt.publish_status  =1 and tt.c_time is not null
            and tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1 and fr.school_type in (3,4)  
            and tt.classroom_id is null and s.school_id = fr.school_id  {}
            GROUP BY time,fr.school_id
            '''.format(time)
            task = mysqlDB(sql)
            task_df_all.append(task)
        elif i == 104:
            sql = '''
            select DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as time,fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'dtk_fj' 
            from tp_task_info  tt ,as_answer_sheet_info aasi,tp_course_info tc,franchised_school_info fr,school_info s
            where tt.task_type =13 and tt.TASK_VALUE_ID = aasi.paper_id   and aasi.meta_type = 1 and tt.publish_status  =1  and tt.video_id is null and tt.c_time is not null
            and tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1 and fr.school_type in (3,4)  
            and tt.classroom_id is null and s.school_id = fr.school_id {}
            GROUP BY time,fr.school_id
            '''.format(time)
            task = mysqlDB(sql)
            task_df_all.append(task)
        elif i == 105:
            sql = '''
            select DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as time,fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as 'dtk_sj' 
            from tp_task_info  tt ,as_answer_sheet_info aasi,tp_course_info tc,franchised_school_info fr,school_info s
            where tt.task_type =13 and tt.TASK_VALUE_ID = aasi.paper_id   and aasi.meta_type = 3 and tt.publish_status  =1  and tt.video_id is null and tt.c_time is not null
            and tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1 and fr.school_type in (3,4)  
            and tt.classroom_id is null and s.school_id = fr.school_id {}
            GROUP BY time,fr.school_id
            '''.format(time)
            task = mysqlDB(sql)
            task_df_all.append(task)
        else:
            sql = '''
                SELECT DATE_FORMAT(tt.c_time,'%%Y-%%m-%%d') as time,fr.school_id,fr.name,s.province,s.city,count(tt.task_id) as '{0}'
                FROM tp_task_info tt ,tp_course_info tc,franchised_school_info fr,school_info s
                WHERE tc.DC_SCHOOL_ID = fr.school_id  and tc.course_id = tt.COURSE_ID  and fr.school_id >50000 and fr.enable = 0 and tc.LOCAL_STATUS = 1  and tt.c_time is not null
                and fr.school_type in (3,4) and tt.task_type = {0}  and tt.classroom_id is null and s.school_id = fr.school_id {1}
                GROUP BY time,fr.school_id       
                '''.format(i,time)
            task = mysqlDB(sql)
            task_df_all.append(task)

    if time == '':
        every_task_all = reduce(
            lambda left, right: pd.merge(left, right, on=['time', 'name', 'school_id', 'province', 'city'], how='outer'),
            task_df_all)

        every_task_all.columns = column
        every_task_all = every_task_all.fillna(0)
        # 新增两列新答题卡和 任务总数
        every_task_all['new_dtk'] = every_task_all['cy'] + every_task_all['dtk'] + every_task_all['dt']
        every_task_all['zuoye_count'] = every_task_all['xzy'] + every_task_all['tl'] + every_task_all['wkc'] + \
                                        every_task_all['yb'] + every_task_all['zbk'] + every_task_all['gxh'] + \
                                        every_task_all['xs'] + every_task_all['new_dtk']
        every_task_all['task_count'] = every_task_all['zuoye_count'] + every_task_all['axp']

        every_task_all.to_sql(name='every_day_task', con=con, if_exists='replace', index=False)
        return  '初始化数据完成'
    else:
        every_task = reduce(
            lambda left, right: pd.merge(left, right, on=['time', 'name', 'school_id', 'province', 'city'],
                                         how='outer'), task_df_all)
        every_task.columns = column
        every_task = every_task.fillna(0)

        # 删除数据学期数据 和 空 数据
        del_sql = ''' 
        DELETE from every_day_task where date >='2022-07-15'
        '''
        rs.execute(del_sql)
        con.commit()

        del_sql = ''' 
        DELETE from every_day_task where date ='0'
        '''
        rs.execute(del_sql)
        con.commit()

        # 新增两列新答题卡和 任务总数
        every_task['new_dtk'] = every_task['cy'] + every_task['dtk'] + every_task['dt']
        every_task['zuoye_count'] = every_task['xzy'] + every_task['tl'] + every_task['wkc'] + every_task['yb'] + \
                                    every_task['zbk'] + every_task['gxh'] + every_task['xs'] + every_task['new_dtk']
        every_task['task_count'] = every_task['zuoye_count'] + every_task['axp']

        # 重新插入新数据
        every_task.to_sql(name='every_day_task', con=con, if_exists='append', index=False)
        return '本学期数据计算完成'




if __name__ =='__main__':
    b_time = datetime.datetime.now()
    print('开始时间：',b_time.strftime('%Y-%m-%d %H:%M:%S'))

    c_time = "and tt.c_time >= '2022-07-15 00:00:00'"
    taskToSqlite(time=c_time)

    e_time = datetime.datetime.now()
    lenth_time = (e_time - b_time)

    print('结束时间：',e_time.strftime('%Y-%m-%d %H:%M:%S'))
    print('总用时长：',lenth_time)