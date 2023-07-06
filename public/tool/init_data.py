from     public.syncTaskData  import pad_license_dau,day_school_task,year_province_count,school_info
import datetime
import pandas as pd

if __name__ == '__main__':
    c_time = "and tt.c_time >= '2022-07-15 00:00:00'"
    day_school_task(c_time)
    year_province_count()
    school_info()

    now_time = pd.to_datetime(datetime.datetime.now())
    b_time = '2023-02-15 00:00:00'
    e_time = now_time.strftime("%Y-%m-%d 00:00:00")

    index = 'message_log'
    pad_license_dau(b_time=b_time, e_time=e_time, group_by_time='1h', index=index, table_name='pad_license_dau_h',if_exists='replace')
    pad_license_dau(b_time=b_time, e_time=e_time, group_by_time='1d', index=index, table_name='pad_license_dau',if_exists='replace')

    print("---------------------初始化数据完成---------------------")
