import requests
import json
import pandas as pd

exam_id = '854694727066'

# 对比考试的列表
compareExamArray = ''

# 对比类型  1=区域四率  2=区域百分位  3=学校四率  4=学校百分位
compareType = '2'

# -1=区域  0=本校  1=行政班  2=行政班群  3=分层班  4=分层班群
objectTypes = '-1,0,2,4'

examSubjectId = -2
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXRhaWwiOnsidXNlcklkIjoyOTUxNjM1LCJ1c2VyTmFtZSI6IuWkp-i_nua1i-ivlTAwMSIsInBhc3N3b3JkIjoiIiwidXNlcklkZW50aXR5IjoxLCJlbmFibGUiOjEsInNjaG9vbFVzZXJJZCI6MzY3Njg2LCJzY2hvb2xJZCI6NTAwNDMsInNjaG9vbFVzZXJSZWYiOiJmYzI4Y2IwYi1lMDRmLTQ0ODUtOTQ4Yi02M2Q0NTU2ZmNlNGEiLCJzY2hvb2xHcm91cElkIjo3LCJyb2xlcyI6WzE2LDE3LDIsMjEsNiw5LDEzLDE1XSwidXJsTGlzdCI6bnVsbH0sImV4cCI6MTYyMDY0NjgwOSwidXNlcl9uYW1lIjoi5aSn6L-e5rWL6K-VMDAxIiwianRpIjoiM2MzYTBmYzEtNGIwYi00ODllLWI2YTYtNjg4ZDM5OGI5MGUwIiwiY2xpZW50X2lkIjoiRkE5RTIxNUJFNTY2RUU5MjYxNEZCQzExQUJFREY5NjgiLCJzY29wZSI6WyJhbGwiLCJ3ZWIiLCJtb2JpbGUiXX0.3-ey4CzNjlU4QsYEIWFoZI5vfaXf2V6unmzSU6K2Exk'

get_url = 'https://school-cloud.etiantian.com/school-statistics/exam-analysis/school-area-score-multiple-line?examId={}&compareType={}&compareExamArray=&objectTypes={}&r=0.2526140433758095&examSubjectId={}&token={}'.format(
        exam_id, compareType, objectTypes, examSubjectId, token)
res = requests.get(get_url)
text = json.loads(res.text)

polyLines = text['data']['polyLines']
pointXList  = text['data']['pointXList']
# print('5分段',pointXList)

exam_dict = {}
exam_dict['5分段'] = pointXList
for i in polyLines:
        name_list = []
        value_list = []

        for p in i['pointArray']:
                name_list.append(p['name'])
                value_list.append(p['value'])

        # print('{}人数'.format(i['objectName']),name_list)
        # print('{}占比'.format(i['objectName']),value_list)
        exam_dict['{}'.format(i['objectName'])] = name_list

exam_df = pd.DataFrame(exam_dict)
df_split = exam_df['5分段'].str.split('[ [ | ,]',expand=True)[1]
# df2 = df1[0].str.split('[',expand=True)
# df = exam_df.append(df2,ignore_index=True)
exam_df = pd.concat([exam_df,df_split],axis=1)
exam_df.iloc[1:-3,:] = exam_df.iloc[1:3,:].astype('int')
exam_df.loc["sum"]=exam_df.apply(lambda x:sum(x),axis=0)
print(exam_df)

NUM = 205


index = exam_df[exam_df[1].isin(['205'])].index.values[0]
print(index)

exam_df = exam_df[:index+1]
print(exam_df)

#
# exam_df['本校'] = exam_df['本校'].astype('int')
# exam_df['区域'] = exam_df['区域'].astype('int')
# x = exam_df[1].to_list()
# y1 = exam_df['本校'].to_list()
# y2 = exam_df['区域'].to_list()
# print(x[:48])
# print(y1[:48])
# print(y2[:48])
# print(len(x))

workLines = text['data']['workLines']
workLines_list = []
for i in workLines:
        workLines_list.append(i['workLineX'])
print('过程线',workLines_list)

