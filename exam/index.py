import pandas as pd
from flask import  render_template
from exam import exam_blue

# 考试试题柱状图
@exam_blue.route('/examQues', methods=['get'])
def examQues():
    ques = pd.read_excel(r'F:\8、考试数据分析\理工附中数据\初一21~22第二学期期末\整理文件\人工\试题聚类分析.xlsx', sheet_name='数学')
    xdata = ques['题号'].tolist()
    legend = ques.columns.tolist()[3:]
    # qu_y_data = ques['{}'.format(legend[0])].tolist()
    school_y_data = ques['{}'.format(legend[1])].tolist()
    max_y_data = ques['{}'.format(legend[2])].tolist()
    min_y_data = ques['{}'.format(legend[3])].tolist()

    # 知识板块和能力板块合并
    title_list = []
    title_kenow = ques['知识板块'].unique()
    for i in title_kenow:
        title_list.append(i)
    title_ability = ques['能力板块'].unique()
    for i in title_ability:
        title_list.append(i)

    # 计算出知识板块和能力板块的索引位置
    knowblock_list = []
    for i in title_kenow:
        knowblock_list.append((ques[ques['知识板块'] == '{}'.format(i)]).index.tolist())
    for i in title_ability:
        knowblock_list.append((ques[ques['能力板块'] == '{}'.format(i)]).index.tolist())

    # 把知识板块和能力板块的索引所在的替换成蓝色
    y_data_bar_list = []
    for knowblock in knowblock_list:
        list = []
        for k, v in enumerate(school_y_data):
            if k in knowblock:
                dic = {'value': v,
                       'itemStyle': {
                           'color': '#5876D1'
                       }}
                list.append(dic)
            else:
                list.append(v)
        y_data_bar_list.append(list)

    data = {
        'title': title_list,
        'xdata': xdata,
        'legend': legend,
        'ydata': [y_data_bar_list, school_y_data, max_y_data, min_y_data],
    }

    return render_template('examQues.html', data=data)


# 考试桑基流量图
@exam_blue.route('/examSankey', methods=['get'])
def examSankey():
    return render_template("examSankey.html")


# 考试5分段
@exam_blue.route('/examLine', methods=['get'])
def examLine():
    return render_template('examLine.html')
