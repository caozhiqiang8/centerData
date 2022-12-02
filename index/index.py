from index import  index_blue
from flask import  render_template
from public.db_con import  sqlite_connect


@index_blue.route('/index', methods=['get'])
def index():
    return render_template('index.html')


# 首页地图接口
@index_blue.route('/getMap', methods=['get'])
def getMap():
    sql = '''
            select * from year_province_data 
            '''
    colmuns = sqlite_connect(sql).columns[1:]
    province_data = []
    year_data = []

    for i in colmuns:
        sql = '''
            select province,{} from year_province_data 
            '''.format(i)
        data = sqlite_connect(sql)
        data = data.set_index('province')
        count = data['{}'.format(i)].sum()
        year_data.append(count)
        data = data.to_dict(orient='dict')['{}'.format(i)]
        province_data.append(data)

    data = {
        'y22_23': province_data[0],
        'y21_22': province_data[1],
        'y20_21': province_data[2],
        'y19_20': province_data[3],
        'y18_19': province_data[4],
        'y17_18': province_data[5],
        'yearCount': year_data[::-1],
    }
    return data
