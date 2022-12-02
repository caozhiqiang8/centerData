from login import  login_blue
from flask import Flask, render_template, request, session




# 登录
@login_blue.route('/', methods=['get', 'post'])
@login_blue.route('/login', methods=['get', 'post'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        data = request.get_json()
        print(data)

        if data['userName'] == 'admin' and data['passWord'] == '1111':
            data = {
                'code': '0',
            }
            session['userName'] = 'admin'
            session['passWord'] = '1111'
            return data
        else:
            data = {
                'code': '1',
                'masg': '帐号密码错误'

            }
            return data
