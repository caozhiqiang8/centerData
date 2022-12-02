import json
from flask import  render_template, request
from public.db_con import  sqlite_connect
from task import task_blue

# 作业分析路由
@task_blue.route('/task', methods=['get'])
def task():
    return render_template('task.html')


# 平台每日作业情况
@task_blue.route('/getTaskCount', methods=['get'])
def getTaskCount():
    schoolId = request.args.get('schoolId')
    print(schoolId)
    if schoolId:
        sql = '''
               select date,xzy,tl,wkc,yb,zbk,dtk,gxh,xs,axp,hp,zp,dtk_lxc,dtk_fj,dtk_sj,zuoye_count,task_count from day_school_task  where date >='2022-07-15' and school_id = {}
        order by date
                '''.format(schoolId)
        task = sqlite_connect(sql)
        taskCount = task.groupby(['date'], as_index=False).sum()
        x_date = taskCount['date'].to_list()
        y_list = []
        for i in (taskCount.columns.to_list())[1:]:
            y_list.append(taskCount['{}'.format(i)].to_list())
        type_name = ['学资源', '讨论', '微课程', '一般任务', '直播课', '答题卡', '个性化', '先声', '爱学派归档', '答题卡互批', '答题卡自批',
                     '答题卡练习册', '答题卡附件', '答题卡试卷', '作业总数']
        data = {
            'x_date': x_date,
            'y_list': y_list,
            'type_name': type_name,
            'msg': 'ok'
        }
        return data

    else:
        sql = '''
        select date,xzy,tl,wkc,yb,zbk,dtk,gxh,xs,axp,hp,zp,dtk_lxc,dtk_fj,dtk_sj,zuoye_count,task_count from day_school_task  where date >='2021-07-15'
        order by date
        '''
        task = sqlite_connect(sql)

        taskCount = task.groupby(['date'], as_index=False).sum()
        x_date = taskCount['date'].to_list()
        y_list = []
        for i in (taskCount.columns.to_list())[1:]:
            y_list.append(taskCount['{}'.format(i)].to_list())
        type_name = ['学资源', '讨论', '微课程', '一般任务', '直播课', '答题卡', '个性化', '先声', '爱学派归档', '答题卡互批', '答题卡自批',
                     '答题卡练习册', '答题卡附件', '答题卡试卷', '作业总数']
        data = {
            'x_date': x_date,
            'y_list': y_list,
            'type_name': type_name,
            'msg': 'ok'
        }
        return data


# 学校每日作业情况
@task_blue.route('/getSchoolTaskCount', methods=['get'])
def getSchoolTaskCount():
    code = request.values.get('code')
    # 学校作业情况
    if code == '1':
        sql = '''
        select * from day_school_task  where date >= '2022-07-15'
        order by date
        '''
        task = sqlite_connect(sql)
        schoolTaskCount = task.groupby(['school_id', 'name'], as_index=False).sum().sort_values(by='zuoye_count',
                                                                                                ascending=False)
        schoolCount = schoolTaskCount['school_id'].count()
        schoolTaskCount = json.loads(schoolTaskCount.to_json(orient='records', force_ascii=False))

        data = {
            'schoolTaskCount': schoolTaskCount,
            'schoolCount': '{}'.format(schoolCount),
            'msg': 'ok'
        }
        return data

    #  一周内学校作业情况
    elif code == '2':
        sql = '''
               select  * from day_school_task where date >=datetime('now','start of day','-7 day') AND date<datetime('now','start of day','+0 day')
            ORDER BY date
               '''
        task = sqlite_connect(sql)

        schoolWeekTaskCount = task.groupby(['school_id', 'name'], as_index=False).sum().sort_values(by='zuoye_count',
                                                                                                    ascending=False)
        schoolCount = schoolWeekTaskCount['school_id'].count()
        schoolWeekTaskCount = json.loads(schoolWeekTaskCount.to_json(orient='records', force_ascii=False))
        data = {
            'schoolWeekTaskCount': schoolWeekTaskCount,
            'schoolCount': '{}'.format(schoolCount),
            'msg': 'ok'
        }

        return data
