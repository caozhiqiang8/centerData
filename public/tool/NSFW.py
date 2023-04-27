import os,shutil
from PIL import Image
from  public.db_con  import mysql_connect

dir_path = r'F:\9、测试\nsfw\pic-porn'
file_name_list = os.listdir(dir_path)

# yellow_path = r'F:\9、测试\机器挑出来的\pic\yellow'
#
# for file_name in file_name_list:
#     file_path = os.path.join(dir_path, file_name)
#     try:
#         img = Image.open(file_path).convert('YCbCr')
#         w, h = img.size
#         data = img.getdata()
#         cnt = 0
#         for i, ycbcr in enumerate(data):
#             y, cb, cr = ycbcr
#             if 86 <= cb <= 117 and 140 <= cr <= 168:
#                 cnt += 1
#         if cnt > w * h * 0.2:
#             print('%s 是 黄图:' %file_name)
#             shutil.copy(file_path,yellow_path)
#         else:
#             pass
#     except:
#         pass
#
# print('分类完毕')
#

# print(file_name_list)

file_path = []
for i in file_name_list:
    file_path.append( (i.replace(',','/'))[11:-11] )
# print(file_path)

sql = '''
SELECT DISTINCT user_id  from rs_resource_info where file_path in {}

'''.format(tuple(file_path))
user_id = mysql_connect(sql)['user_id'].to_list()
print(user_id )
