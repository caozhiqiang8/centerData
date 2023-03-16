from     public.syncTaskData  import pad_license_dau


if __name__ == '__main__':

    b_time = '2023-02-15 00:00:00'
    e_time = '2023-03-16 00:00:00'

    index = 'message_log'
    pad_license_dau(b_time=b_time, e_time=e_time, group_by_time='1h', index=index, table_name='pad_license_dau_h',if_exists='replace')
    pad_license_dau(b_time=b_time, e_time=e_time, group_by_time='1d', index=index, table_name='pad_license_dau',if_exists='replace')

    print("---------------------初始化数据完成---------------------")
