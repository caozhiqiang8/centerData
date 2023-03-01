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
        'y22_23_2': province_data[0],
        'y22_23_1': province_data[1],
        'y21_22_2': province_data[2],
        'y21_22_1': province_data[3],
        'y20_21_2': province_data[4],
        'y20_21_1': province_data[5],
        'y19_20_2': province_data[6],
        'y19_20_1': province_data[7],
        'y18_19_2': province_data[8],
        'y18_19_1': province_data[9],
        'y17_18_2': province_data[10],
        'y17_18_1': province_data[11],
        'yearCount': year_data[::-1],
    }
    return data
