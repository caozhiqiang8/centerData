import datetime

def cost_time(fun):

    def wrapper(*args,**kwargs):
        b_time = datetime.datetime.now()
        print('===================================================')
        print('{}开始执行时间：'.format(fun.__name__), b_time.strftime('%Y-%m-%d %H:%M:%S'))
        result =fun(*args,**kwargs)
        e_time = datetime.datetime.now()
        lenth_time = (e_time - b_time)

        print('{}结束执行时间：'.format(fun.__name__), e_time.strftime('%Y-%m-%d %H:%M:%S'))
        print('{}总用时长：'.format(fun.__name__), lenth_time)
        print('===================================================')

    return wrapper