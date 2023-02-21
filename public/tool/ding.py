import urllib.parse
from dingtalkchatbot.chatbot import DingtalkChatbot
import time
import hmac
import urllib
import hashlib
import base64
import requests
import  json


def jokes():
    url = "https://eolink.o.apispace.com/xhdq/common/joke/getJokesByRandom"

    payload = {"pageSize": 1}

    headers = {
        "X-APISpace-Token": "f0t8kj66vhwtaz4ygd5zauxfnyy0520k",
        "Authorization-Type": "apikey",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.text


# 获取链接,填入urlToken 和 secret
def getSIGN():
    timestamp = str(round(time.time() * 1000))
    urlToken = r"https://oapi.dingtalk.com/robot/send?access_token=5d1bc1f624eaa769adec05af8b5839a8938e40baa71212cb64b961ffdd3bd903"
    secret = 'SEC754805d52d707cd5f3dc7bfaa39fd422869ea7259f2f570b7bce9fb7a8ff2d87'
    secret_enc = secret.encode('utf-8')
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
    xiaoDing.send_text(msg='{}'.format(msg),is_at_all=False)
    return '发送成功'


r = json.loads(jokes())['result'][0]['content']

print(r)
dingText(r)


# def 发送图片():
#     """第二:发送图片
#     send_image(self, pic_url):
#         pic_url: "图片地址"
#     """
#     xiaoDing.send_image("http://rrd.me/gE93L")
#
#
# def 发送link():
#     """第三:发送link
#     send_link(self, title, text, message_url, pic_url='')
#         title:标题    text:内容,太长会自动截取
#         message_url:跳转的url  pic_url:添加的图片的url(可选)
#     """
#     xiaoDing.send_link(title="今天是星期8", text="牵你的手，朝朝暮暮，牵你的手，等待明天，牵你的手，走过今生，牵你的手，生生世世",
#                        message_url="https://baidu.com",
#                        pic_url="http://rrd.me/gE93L")
#
#
# def 发送markdown():
#     """第四:发送markdown
#     send_markdown(self,title,text,is_at_all=False,at_mobiles=[],at_dingtalk_ids=[],is_auto_at=True)
#         title:标题    text:内容
#         is_at_all: @所有人时：true，否则为：false（可选）
#         at_mobiles: 被@人的手机号（默认自动添加在text内容末尾，可取消自动化添加改为自定义设置，可选）
#         at_dingtalk_ids: 被@人的dingtalkId（可选）
#         is_auto_at: 是否自动在text内容末尾添加@手机号，默认自动添加，可设置为False取消（可选）
#     """
#     xiaoDing.send_markdown(title="我是标题",text="我是内容,啊哈哈哈哈哈",is_at_all=True)
#
#
# def 发送图片超链接():
#     # send_feed_card(links)
#     """
#         links是一个列表a,列表里每个元素又是列表b
#         列表b的属性:
#             title:标题    message_url:点开后跳转的URL   pic_url:图片的地址
#     Returns:
#
#     """
#     feedlink1 = FeedLink(title="猫1", message_url="https://www.badiu.com/",
#                          pic_url="http://rrd.me/gE9zB")
#     feedlink2 = FeedLink(title="猫2", message_url="https://www.badiu.com/",
#                          pic_url="http://rrd.me/gE9zN")
#     feedlink3 = FeedLink(title="猫3", message_url="https://www.badiu.com/",
#                          pic_url="http://rrd.me/gE9zV")
#     feedlin4k = FeedLink(title="猫4", message_url="https://www.badiu.com/",
#                          pic_url="http://rrd.me/gE92a")
#
#     links = [feedlink1, feedlink2, feedlink3, feedlin4k]
#     xiaoDing.send_feed_card(links)
#
