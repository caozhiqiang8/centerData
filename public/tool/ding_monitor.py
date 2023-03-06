import urllib.parse
from dingtalkchatbot.chatbot import DingtalkChatbot
import time
import hmac
import urllib
import hashlib
import base64
import json
import pandas as pd
import datetime
from elasticsearch import Elasticsearch

# 显示所有行
pd.set_option("display.max_rows", None)
# 显示所有列
pd.set_option("display.max_columns", None)



# 链接ES
def es_connect(index, body):
    es_hosts = str("69.230.239.155,43.192.117.34").split(",")
    es = Elasticsearch(es_hosts)
    res = es.search(index=index, body=body)
    res = json.loads(json.dumps(res))
    return res

# 获取钉钉链接,填入urlToken 和 secret
def getSIGN():
    # 获取当前时间戳字符串
    timestamp = str(round(time.time() * 1000))

    # # 正式webhook
    # urlToken = r"https://oapi.dingtalk.com/robot/send?access_token=b05a57084bd9b1f9f5d78dae8237821c78c44890c799c23678c75e0c2aeae2e6"
    # # 正式secret
    # secret = 'SEC81159b69686e75d47b3bb0d9904e1ab19c5dbd7c641a4ad2ebc1b6848ec88e63'

    # 测试webhook
    urlToken = r"https://oapi.dingtalk.com/robot/send?access_token=5d1bc1f624eaa769adec05af8b5839a8938e40baa71212cb64b961ffdd3bd903"
    # 测试正式secret
    secret = 'SEC754805d52d707cd5f3dc7bfaa39fd422869ea7259f2f570b7bce9fb7a8ff2d87'

    secret_enc = secret.encode('utf-8')
    # 秘钥字符串
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    SignMessage = urlToken + "&timestamp=" + timestamp + "&sign=" + sign
    return SignMessage


def dingText(msg):
    """第一: 发送文本-->
    send_text(self,msg,is_at_all=False,at_mobiles=[],at_dingtalk_ids=[],is_auto_at=True)
        msg: 发送的消息
        is_at_all:是@所有人吗? 默认False,如果是True.会覆盖其它的属性
        at_mobiles:要@的人的列表,填写的是手机号
        at_dingtalk_ids:未知;文档说的是"被@人的dingtalkId（可选）"
        is_auto_at:默认为True.经过测试,False是每个人一条只能@一次,重复的会过滤,否则不然,测试结果与文档不一致
    """
    SignMessage = getSIGN()
    xiaoDing = DingtalkChatbot(SignMessage)  # 初始化机器人
    at_dingtalk_ids = ['qrkgfhs']
    xiaoDing.send_text(msg='{}'.format(msg), is_at_all=False)


def esSerch(body, index):
    res = es_connect(index=index, body=body)
    res = json.loads(json.dumps(res))
    model_name_agg = res['aggregations']['url_agg']['buckets']
    df = pd.json_normalize(model_name_agg)
    return df


# es查询条数
ES_SERCH_NUM = 100
# 超时倍数预警
COST_NUM = 1.5
# 接口访问倍数预警
URL_COUNT_NUM = 5
# 报错次数
ERR_NUM = 5
# datafram 切片数量
ILOC_NUM = 20
# 需要过滤的接口
filter_url_list = ['http://school-cloud.ai-classes.com/accesstoken-control/tokens']

while True:
    now_etime = pd.to_datetime(datetime.datetime.now())
    # now_etime = pd.Timestamp("2023-03-04 12:25:04")
    now_btime = now_etime - pd.to_timedelta(1, unit='h')
    before_btime = now_btime - pd.to_timedelta(7, unit='d')
    before_etime = now_etime - pd.to_timedelta(7, unit='d')

    now_index = "action_logs_{}".format(now_etime.strftime("%Y%m%d"))
    before_index = "action_logs_{}".format(before_btime.strftime("%Y%m%d"))
    now_week = now_btime.weekday()+1
    print( '{}---周{}'.format(now_btime,now_week))

    if now_etime.strftime("%H") >= '04' and now_etime.strftime("%H") <= '23':
        # 判断是不是周末
        if now_week < 6 :
            # 判断时间 如果 结束时间(当前时间)是 12:00 - 12:30   就从12：00开始
            if now_etime.strftime("%H") == '12' and now_etime.strftime("%M") < '30':
                now_btime = now_btime.strftime("%Y-%m-%d %H:%M:%S")
                now_etime = now_etime.strftime("%Y-%m-%d %H:00:00")
                before_btime = before_btime.strftime("%Y-%m-%d %H:%M:%S")
                before_etime = before_etime.strftime("%Y-%m-%d %H:00:00")
            # 判断时间 如果 开始时间是 12:00 - 12:30  就从 12：30 结束
            elif now_btime.strftime("%H") == '12' and now_btime.strftime("%M") < '30':
                now_btime = now_btime.strftime("%Y-%m-%d %H:30:00")
                now_etime = now_etime.strftime("%Y-%m-%d %H:%M:%S")
                before_etime = before_etime.strftime("%Y-%m-%d %H:%M:%S")
                before_btime = before_btime.strftime("%Y-%m-%d %H:30:00")
            else:
                now_btime = now_btime.strftime("%Y-%m-%d %H:%M:%S")
                now_etime = now_etime.strftime("%Y-%m-%d %H:%M:%S")
                before_btime = before_btime.strftime("%Y-%m-%d %H:%M:%S")
                before_etime = before_etime.strftime("%Y-%m-%d %H:%M:%S")
        else:
            now_btime = now_btime.strftime("%Y-%m-%d %H:%M:%S")
            now_etime = now_etime.strftime("%Y-%m-%d %H:%M:%S")
            before_btime = before_btime.strftime("%Y-%m-%d %H:%M:%S")
            before_etime = before_etime.strftime("%Y-%m-%d %H:%M:%S")
        print(now_btime,before_btime)
        print(now_etime,before_etime)
        print("---------------------{} 至 {}---------------------".format(now_btime, now_etime))

        # 系统响应时长 监控
        body1 = '''
                            {
                      "size": 0,
                      "query": {
                        "bool": {
                          "must": [
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
                      "aggs": {
                        "url_agg": {
                          "terms": {
                            "field": "url.keyword",
                            "size": %s,
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
                            "sum_user": {
                              "cardinality": {
                                "field": "jid"
                              }
                            },
                            "median_time": {
                              "percentiles": {
                                "field": "cost_time",
                                "percents": [
                                  50
                                ]
                              }
                            }
                          }
                        }
                      }
                    }
                        ''' % (now_btime, now_etime, ES_SERCH_NUM)
        df1 = esSerch(body1, now_index)
        df1.columns = ['url', '今日访问次数', '今日访问总时长', '今日中位数', '今日访问人数', '今日平均用时']
        url_list = str(df1['url'].to_list()).replace("'", "\"")

        body2 = '''
                {
                      "size": 0,
                      "query": {
                        "bool": {
                          "must": [
                            {
                              "range": {
                                "c_time": {
                                  "gte": "%s",
                                  "lte": "%s"
                                }
                              }
                            },
                            {"terms": {
                                  "url.keyword":%s
                                }}
                          ]
                        }
                      },
                      "aggs": {
                        "url_agg": {
                          "terms": {
                            "field": "url.keyword",
                            "size": %s,
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
                            "sum_user": {
                              "cardinality": {
                                "field": "jid"
                              }
                            },
                            "median_time": {
                              "percentiles": {
                                "field": "cost_time",
                                "percents": [
                                  50
                                ]
                              }
                            }
                          }
                        }
                      }
                    }
                        ''' % (before_btime, before_etime, url_list, ES_SERCH_NUM)
        df2 = esSerch(body2, before_index)
        df2.columns = ['url', '昨日访问次数', '昨日访问总时长', '昨日中位数', '昨日访问人数', '昨日平均用时']
        # 合并表格
        df_merge = pd.merge(df1, df2, on='url', how='left')
        df_merge = df_merge[['url', '今日平均用时', '昨日平均用时', '今日中位数', '昨日中位数', '今日访问次数','昨日访问次数', '今日访问总时长', '昨日访问总时长', '今日访问人数', '昨日访问人数']]
        df_merge = df_merge.fillna(0)
        df_merge = df_merge.sort_values(by='今日访问总时长', ascending=False)
        # 过滤不需要报警的接口
        df_merge = df_merge[ ~df_merge['url'].isin(filter_url_list)]
        # 超时预警计算
        cost_time = df_merge.iloc[:ILOC_NUM, :].loc[:, ['url', '今日平均用时', '今日中位数', '昨日平均用时', '昨日中位数']]
        cost_time_res = cost_time[(cost_time['今日平均用时'] > (cost_time['昨日平均用时'] * COST_NUM)) & cost_time['昨日平均用时'] > 0]
        cost_time_res_dict = cost_time_res.iloc[:, :].to_dict(orient='records')
        if len(cost_time_res_dict) > 0:
            ding_title = '{} 至 {} 接口超时{}倍 \n'.format(now_btime, now_etime, COST_NUM)
            for i in cost_time_res_dict:
                ding_text = ding_title + '{}\n'.format(i)
                # dingText(ding_text)
                print(ding_text)
                time.sleep(1)

        else:
            print('没有接口超时')

        # 接口访问次数 监控
        url_count = df_merge.iloc[:ILOC_NUM, :].loc[:, ['url', '今日访问次数', '昨日访问次数']]
        url_count_res = url_count[
            (url_count['今日访问次数'] > (url_count['昨日访问次数'] * URL_COUNT_NUM)) & url_count['昨日访问次数'] > 50]
        url_count_res_dict = url_count_res.iloc[:, :].to_dict(orient='records')
        if len(url_count_res_dict) > 0:
            ding_title = '{} 至 {} 接口访问次数暴增{}倍 \n'.format(now_btime, now_etime, URL_COUNT_NUM)
            for i in url_count_res_dict:
                ding_text = ding_title + '{}\n'.format(i)
                # dingText(ding_text)
                print(ding_text)
                time.sleep(1)

        else:
            print('没有接口访问次数增多')

        # 接口报错 监控
        try:
            url_err_body = '''
                {
                  "query": {
                    "bool": {
                      "must": [
                        {
                          "term": {
                            "status": {
                              "value": "500"
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
                  "aggs": {
                    "url_agg": {
                      "terms": {
                        "field": "url.keyword"
                      }
                    }
                  },
                  "size":0
                }
                ''' % (now_btime, now_etime)
            url_err = esSerch(url_err_body, now_index)
            url_err.columns = ['url', '报错次数']
            # 过滤不需要报警的接口
            url_err = url_err[~url_err['url'].isin(filter_url_list)]
            url_err = url_err[url_err['报错次数'] >= ERR_NUM]
            url_err_dict = url_err.iloc[:, :].to_dict(orient='records')
            if len(url_err_dict) > 0:
                for i in url_err_dict:
                    ding_title = '{} 至 {} 接口报错{}次以上 \n'.format(now_btime, now_etime, ERR_NUM)
                    ding_text = ding_title + '{}\n'.format(i)
                    # dingText(ding_text)
                    print(ding_text)
                    time.sleep(1)
            else:
                print('没有接口报错')
        except:
            print('没有接口报错')
    else:
        print('{} 系统休息'.format(now_etime))

    time.sleep(3600)
