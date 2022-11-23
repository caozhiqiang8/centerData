import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from urllib import parse

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
print(text)

