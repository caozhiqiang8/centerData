import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

exam_id = '4498462562376'

# 对比考试的列表
compareExamArray = ''

# 对比类型  1=区域四率  2=区域百分位  3=学校四率  4=学校百分位
compareType = '2'

# -1=区域  0=本校  1=行政班  2=行政班群  3=分层班  4=分层班群
objectTypes = '-1,0,2,4'
# 学科
examSubjectId = -2

# 定义X轴刻度截取，，需要注意定义的数值不能大于竖线最小值
NUM = 315

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXRhaWwiOnsidXNlcklkIjoyOTUxNjM1LCJ1c2VyTmFtZSI6IuWkp-i_nua1i-ivlTAwMSIsInBhc3N3b3JkIjoiIiwidXNlcklkZW50aXR5IjoxLCJlbmFibGUiOjEsInNjaG9vbFVzZXJJZCI6MzY3Njg2LCJzY2hvb2xJZCI6NTAwNDMsInNjaG9vbFVzZXJSZWYiOiJmYzI4Y2IwYi1lMDRmLTQ0ODUtOTQ4Yi02M2Q0NTU2ZmNlNGEiLCJzY2hvb2xHcm91cElkIjo3LCJyb2xlcyI6WzE2LDE3LDIsMjEsNiw5LDEzLDE1XSwidXJsTGlzdCI6bnVsbH0sImV4cCI6MTYyMDY0NjgwOSwidXNlcl9uYW1lIjoi5aSn6L-e5rWL6K-VMDAxIiwianRpIjoiM2MzYTBmYzEtNGIwYi00ODllLWI2YTYtNjg4ZDM5OGI5MGUwIiwiY2xpZW50X2lkIjoiRkE5RTIxNUJFNTY2RUU5MjYxNEZCQzExQUJFREY5NjgiLCJzY29wZSI6WyJhbGwiLCJ3ZWIiLCJtb2JpbGUiXX0.3-ey4CzNjlU4QsYEIWFoZI5vfaXf2V6unmzSU6K2Exk'

get_url = 'https://school-cloud.etiantian.com/school-statistics/exam-analysis/school-area-score-multiple-line?examId={}&compareType={}&compareExamArray={}&objectTypes={}&r=0.2526140433758095&examSubjectId={}&token={}'.format(
        exam_id, compareType,compareExamArray, objectTypes, examSubjectId, token)
res = requests.get(get_url)
text = json.loads(res.text)
print(text)

# 过程线
workLines = text['data']['workLines']
workLines_list = []
for i in workLines:
        workLines_list.append(i['workLineX'])
print('过程线：\n',workLines_list)

# 过程线
workLineName_list = []
for i in workLines:
        workLineName_list.append(i['workLineName'])
print('过程线名字：\n',workLineName_list)

# 5分段
polyLines = text['data']['polyLines']
pointXList  = text['data']['pointXList']
print('5分段：\n',pointXList)

exam_dict = {}
exam_dict['5分段'] = pointXList
for i in polyLines:
        name_list = []
        value_list = []

        for p in i['pointArray']:
                name_list.append(p['name'])
                value_list.append(p['value'])
        # 占比和人数
        print('{}人数：\n'.format(i['objectDisplayName']),name_list)
        # print('{}占比'.format(i['objectName']),value_list)
        exam_dict['{}'.format(i['objectDisplayName'])] = name_list

exam_df = pd.DataFrame(exam_dict)
# 把5分段[500,495]  转成 500
df_split = exam_df['5分段'].str.split('[ [ | ,]',expand=True)[1]
exam_df = pd.concat([exam_df,df_split],axis=1)
exam_df = exam_df.iloc[:,1:]
# 人数转为数值
exam_df.iloc[:,:-1] = (exam_df.iloc[:,:-1]).astype('int')

# 计算总人数
sum = (exam_df.iloc[:,:-1].apply(lambda x:sum(x),axis=0)).to_list()
print('总人数：\n',sum)


# NUM 分数在第几行
index = exam_df[exam_df[1].isin(['{}'.format(NUM)])].index.values[0]
print('数值所在的行:\n',index)

# 表格拆分， 1分值上半部分 和 2 分值下半部分
exam_df_1 = exam_df.iloc[:index+1,:]
exam_df_2 = exam_df.iloc[index+1:,:]

# 计算NUM后的总数
exam_df_2.loc['sum'] = exam_df_2.iloc[:,:-1].sum(axis=0)
exam_df_2 = exam_df_2.loc['sum',:]
exam_df_2 = pd.DataFrame(exam_df_2)
exam_df_2 = exam_df_2.T

# 2 求和  拼接到1
exam_df = pd.concat([exam_df_1,exam_df_2],axis=0)
exam_df_columns = exam_df.columns.tolist()

# 计算人数占比
for i in range(len(exam_df_columns)-1):
        exam_df['{}占比'.format(exam_df_columns[i])] = exam_df[exam_df_columns[i]].div(sum[i]).mul(100)

# 修改index
exam_df_infex = exam_df.index.tolist()
exam_df_infex[-1] = '{}'.format(index+1)
exam_df.index = exam_df_infex

# 修改columns
exam_df_columns = exam_df.columns.tolist()
new_lists =['5分段' if i ==1 else i for i in exam_df_columns]
exam_df.columns = new_lists

# 只保留分段和占比
exam_df = exam_df.loc[:,'5分段':]
print(exam_df)
exam_df_columns = exam_df.columns.tolist()[1:]

# 准备X Y 轴数据
x1 = exam_df['5分段'].to_list()
x1[-1] = '低于{}'.format(NUM)
y_list = []
for i in exam_df_columns:
        y_list.append(exam_df['{}'.format(i)].to_list())
print('5分段：\n',x1)
print('Y轴：\n',y_list)

# 显示中文标签
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

fig, ax1 = plt.subplots(nrows=1, ncols=1,sharey="row",figsize=((20, 10)))
# 让2个子图的y轴一样，同时创建副坐标轴。
ax2 = ax1.twiny()

for i in y_list:
        print(i)
        ax1.plot(x1,i,linestyle="-",marker="o")
# ax1.plot(x1,y2, color='#ED7D31',linestyle="-",marker="o")
# ax1.plot(x1, y2, color='#5B9BD5',label="x1",linestyle="-",marker="o")

# 添加数值显示
for i in range(len(y_list)):
        for x, y in zip(x1[:-1], y_list[i][:-1]):
                plt.text(int(x), y, "%.2f" % (y) + '%', verticalalignment='top', horizontalalignment='center')


# 绘制副轴 X轴
begin = int(x1[0])
end = int(x1[-2]) -5 -1
print(begin,end)
x2 = [i for i in range(begin, end, -1)]
y3 = [0 for i in range(begin, end, -1)]
ax2.plot(x2, y3, color='#000')

# 绘制竖线
for i in workLines_list[:-1]:
        ax2.axvline(i, color='#ED7D31',ls='--')

#  合并,,invert_xaxis逆转X轴
plt.gca().invert_xaxis()

# 设置图表图例在右上角
ax1.legend(loc='upper left',labels=exam_df_columns)

# Y轴最小值
plt.ylim(ymin=0)

# 指定上X轴显示
plt.xticks(ticks =workLines_list[:-1],labels=workLineName_list[:-1],rotation=30, fontsize=15)
ax1.grid( ls = '-.', lw = 0.25)  # 生成网格

plt.show()