from public.db_con import mysql_connect
import requests,json

#  down文件
sql = '''
    SELECT  rs.res_id ,res_name,ROUND(rs.file_size/1024/1024/1024,2) "file_size",DATE_FORMAT(rs.c_time,'%%Y-%%m-%%d %%H:%%i:%%S') as c_time ,CONCAT("https://cdn1-school.ai-classes.com/fpupload/",file_path,"001_pre.jpg") "img_url",file_path  ,u.user_name ,u.user_id ,u.ett_user_id  ,u.dc_school_id ,s.name ,ti.teacher_name , si.STU_NAME
    from rs_resource_info rs LEFT JOIN user_info u on u.user_id = rs.user_id
    LEFT JOIN  school_info s on u.dc_school_id  = s.school_id
    left JOIN  student_info si on si.user_id = u.ref
    left JOIN  teacher_info ti on ti.user_id = u.ref
    where rs.res_id < 0  and s.school_id != 51286 and rs.FILE_SUFFIXNAME = '.mp4' and u.user_id = '307513619'
    ORDER BY  u.dc_school_id  ,u.user_id,rs.c_time desc
     '''
data = mysql_connect(sql)

data_img = data.loc[:,['res_id','img_url']]
data_img = json.loads(data_img.to_json(orient='records'))
# print(data_img)
for i in data_img:
    print(i)
    response  = requests.get(r'{}'.format(i['img_url'])).content
    newSaveImagePath  = r'F:\PythonObject\DataCenter\nwsf\{}.jpg'.format(i['res_id'])
    with open(newSaveImagePath,'wb') as f:
        f.write(response)
print('保存成功')
