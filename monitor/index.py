import json
import pandas as pd
from flask import render_template, request
from public.db_con import es_connect, mysql_connect
from monitor import monitor_blue
from public.token import token


# 数据监控路由
@monitor_blue.route('/monitor', methods=['get'])
def monitor():
    return render_template('monitor.html')


#  用户行为
@monitor_blue.route('/userAction', methods=['post'])
def userAction():
    data = json.loads(request.get_data())
    if 'jid' in data:
        user_id = data['jid']
        print('请求参数jid：' + user_id)
        body = '''{
                  "query": {
                    "bool": {
                      "must": [
                        {
                          "term": {
                            "jid": {
                              "value": %s
                            }
                          }
                        }
                      ]
                    }
                  },"sort": [
                    {
                      "c_time": {
                        "order": "desc"
                      }
                    }
                  ],
                  "from":1,
                  "size":10000
                    }''' % user_id
        res = es_connect(index="two_month_action_logs", body=body)
        res = json.loads(json.dumps(res))
        res = res['hits']['hits']
        userAction = []
        for i in res:
            userAction.append(i['_source'])
        data = {
            'msg': '1',
            'userAction': userAction
        }
        print('加载完成')
        return data
    elif 'time' in data:
        date = data['date']
        time = data['time']
        btime = time[0]
        etime = time[1]
        date_btime = '{}-{}-{} {}'.format(date[:4], date[4:6], date[6:], btime)
        date_etime = '{}-{}-{} {}'.format(date[:4], date[4:6], date[6:], etime)
        print('请求参数：', date, date_btime, date_etime)

        body = '''
             {
              "query": {
                "bool": {
                  "must": [
                    {
                      "range": {
                        "cost_time": {
                          "gt": 0
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
                    },
                    {
                      "term": {
                        "project_name.keyword": {
                          "value": "gateway-service"
                        }
                      }
                    }
                  ]
                }
              },
              "size": 30000,
                "sort": [
                    {
                      "process_time": {
                        "order": "asc"
                      }
                    }
                ]
            }
            ''' % (date_btime, date_etime)
        data = es_connect(index='action_logs_{}'.format(date), body=body)
        data = json.loads(json.dumps(data))
        data = data['hits']['hits']
        res = []
        for i in data:
            res.append(i['_source'])
        res = pd.DataFrame(res)
        model_name = (res.groupby(['model_name']).nunique()).index.tolist()
        x_data = res['process_time'].tolist()
        y_data = []

        for i in model_name:
            res1 = res[res['model_name'] == '{}'.format(i)]
            df_merge = pd.merge(res, res1, on='process_time', how='left')
            df_merge['responseSize_y'] = df_merge['responseSize_y'].fillna('-')
            y_list = df_merge['responseSize_y'].tolist()
            y_data.append(y_list)
        data = {
            'model_name': model_name,
            'x_data': x_data,
            'y_data': y_data,
        }
        print('加载完成')
        return data

    else:
        return render_template('monitor.html')


# url 访问
@monitor_blue.route('/urlCall', methods=['post'])
def urlCall():
    date = json.loads(request.get_data())
    date = date['date']
    print('请求参数：' + date)

    body = '''
            {
          "query": {
            "bool": {
              "must": [
                {
                  "range": {
                    "responseSize": {
                      "gt": 0
                    }
                  }
                }
              ]
            }
          },
          "size": 0,
          "aggs": {
            "model_name_agg": {
              "terms": {
                "field": "url.keyword",
                "size": 100,
                "order": {
                  "sum_time": "desc"
                }
              },
              "aggs": {
                "avg_time": {
                  "avg": {
                    "field": "cost_time"
                  }
                },
                "sum_time": {
                  "sum": {
                    "field": "cost_time"
                  }
                },
                "sum_user":{
                  "cardinality": {
                    "field": "jid"
                  }
                }
                ,
                "max_time": {
                  "percentiles": {
                    "field": "cost_time",
                    "percents": [
                      1,
                      5,
                      25,
                      50,
                      75,
                      95,
                      99
                    ]
                  }
                }
              }
            }
          }
        }
    '''
    res = es_connect(index="action_logs_{}".format(date), body=body)
    res = json.loads(json.dumps(res))
    model_name_agg = res['aggregations']['model_name_agg']['buckets']
    print('加载完成')
    data = {
        "model_name_agg": model_name_agg

    }

    return data


# 箱型图
@monitor_blue.route('/urlBox', methods=['get'])
def urlBox():
    urlBox = [842, 842, 2849, 650, 650, 3939, 1730, 3914, 746, 698, 698, 752, 1711, 746, 1916, 69, 3311, 2627, 893,
              2303, 893, 2303, 1907, 2667, 794, 794, 794, 794, 794, 794, 69, 2927, 794, 794, 794, 1827, 7619, 650, 2551,
              794, 794, 2705, 1422, 6924, 1678, 842, 1766, 794, 18470, 748, 748, 1580, 1585, 1825, 69, 1609, 1988, 844,
              701, 69, 13777, 1422, 650, 69, 3644, 7793, 890, 2358, 69, 1832, 794, 794, 1741, 14252, 842, 2343, 1852,
              2930, 1518, 3308, 1748, 891, 4045, 891, 16359, 749, 1936, 1730, 650, 747, 1516, 3306, 16359, 1786, 794,
              554, 1540, 794, 794, 1783, 1660, 748, 1832, 2255, 1728, 69, 794, 1507, 1763, 650, 746, 69, 1337, 746,
              1524, 2801, 795, 650, 1910, 795, 746, 69, 795, 746, 746, 746, 1884, 1820, 650, 650, 1684, 1701, 2934,
              1943, 2896, 1409, 1823, 650, 1422, 1804, 2935, 1771, 650, 650, 842, 650, 843, 843, 12458, 1578, 6621,
              1802, 794, 17816, 1821, 699, 3537, 1674, 2562, 845, 2612, 845, 17284, 1854, 1801, 1801, 746, 650, 746,
              3697, 5536, 8509, 1786, 1955, 1609, 1502, 3936, 2963, 1337, 843, 843, 843, 843, 844, 1684, 1809, 1422,
              2497, 2900, 842, 69, 1823, 1959, 2459, 700, 9996, 698, 698, 650, 650]
    data = {
        "urlBox": urlBox

    }

    return data


# 视频审核
@monitor_blue.route('/videoReview', methods=['post'])
def videoReview():
    data = json.loads(request.get_data())
    date = data['date']
    user_id = data['userId']
    print('请求参数：' + date, user_id)

    if user_id:
        sql = '''
    SELECT  rs.res_id ,res_name,ROUND(rs.file_size/1024/1024/1024,2) "file_size",DATE_FORMAT(rs.c_time,'%%Y-%%m-%%d %%H:%%i:%%S') as c_time ,CONCAT("https://cdn1-school.ai-classes.com/fpupload/",file_path,"001_pre.jpg") "img_url",file_path  ,u.user_name ,u.user_id ,u.ett_user_id  ,u.dc_school_id ,s.name ,ti.teacher_name , si.STU_NAME
    from rs_resource_info rs LEFT JOIN user_info u on u.user_id = rs.user_id   
    LEFT JOIN  school_info s on u.dc_school_id  = s.school_id
    left JOIN  student_info si on si.user_id = u.ref 
    left JOIN  teacher_info ti on ti.user_id = u.ref
    where rs.res_id < 0  and s.school_id != 51286 and rs.FILE_SUFFIXNAME = '.mp4' and u.user_id = '{}'
    ORDER BY  u.dc_school_id  ,u.user_id,rs.c_time desc 
     '''.format(user_id)
        data_video = mysql_connect(sql)
    elif date:
        sql = '''
                SELECT  rs.res_id ,res_name,ROUND(rs.file_size/1024/1024/1024,2) "file_size",DATE_FORMAT(rs.c_time,'%%Y-%%m-%%d %%H:%%i:%%S') as c_time ,CONCAT("https://cdn1-school.ai-classes.com/fpupload/",file_path,"001_pre.jpg") "img_url",file_path  ,u.user_name ,u.user_id ,u.ett_user_id  ,u.dc_school_id ,s.name ,ti.teacher_name , si.STU_NAME
                from rs_resource_info rs LEFT JOIN user_info u on u.user_id = rs.user_id   
                LEFT JOIN  school_info s on u.dc_school_id  = s.school_id
                left JOIN  student_info si on si.user_id = u.ref 
                left JOIN  teacher_info ti on ti.user_id = u.ref
                where rs.res_id < 0  and s.school_id != 51286 and rs.FILE_SUFFIXNAME = '.mp4'  and rs.c_time >='{} 00:00:00' and rs.c_time <='{} 23:59:59'
                ORDER BY  u.dc_school_id  ,u.user_id,rs.c_time desc 
                '''.format(date, date)
        data_video = mysql_connect(sql)
    videoCount = int(data_video['res_id'].count())
    videoReviewData = json.loads(data_video.to_json(orient='records', force_ascii=False))

    user_token = token()
    data = {
        'videoReviewData': videoReviewData,
        'videoCount': videoCount,
        'user_token': user_token
    }
    return data
