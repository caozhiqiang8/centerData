var tabs = new Vue({
    el: '#task',
    delimiters: ['[[', ']]'],
    data: {
        activeName: 'first',
        schoolTaskCount: [],
        taskCountShow: true,
        schoolTaskShow: false,
        loading: true,
        pageHeader: false,
        windowsHeight: '200px',
        pageHeaderName: '',
    },
    methods: {
        handleClick(tab, event) {
            console.log(tab.name, event);
            if (tab.name === 'first') {
                this.getTaskCount()
                this.taskCountShow = true
                this.schoolTaskShow = false
                this.loading = false
                this.pageHeader = false
            }
            if (tab.name === 'second') {
                this.getSchoolTask()
                this.taskCountShow = false
                this.schoolTaskShow = true
                this.pageHeader = false
                this.windowsHeight = document.documentElement.clientHeight - 190
            }

        },

        //获取平台每日作业情况数据
        getTaskCount() {
            axios.get('/getTaskCount')
                .then(data => {
                    this.echartsNames = data.data.type_name
                    this.echartslineX = data.data.x_date
                    this.echartsValue = data.data.y_list
                    this.$options.methods.taskCountEycharts(this.echartsNames, this.echartslineX, this.echartsValue)
                })
                .catch(err => (console.log(err)))
        },
        //获取 学校每天作业情况
        getSchoolTask() {
            axios.get('/getSchoolTaskCount')
                .then(data => {
                    this.schoolTaskCount = data.data.schoolTaskCount
                })
                .catch(err => (console.log(err)))
        },
        // 获取学校每日作业情况数据
        getSchoolDayTask(school_id, name) {
            console.log(school_id, name)
            // window.location.href = '/task?schoolId=' + school_id
            this.pageHeaderName = name
            axios.get('/getTaskCount?schoolId=' + school_id)
                .then(data => {
                    this.taskCountShow = true
                    this.schoolTaskShow = false
                    this.pageHeader = true
                    this.echartsNames = data.data.type_name
                    this.echartslineX = data.data.x_date
                    this.echartsValue = data.data.y_list
                    this.$options.methods.taskCountEycharts(this.echartsNames, this.echartslineX, this.echartsValue)
                })
                .catch(err => (console.log(err)))
        },
        // 平台每日作业情况数据----折线图
        taskCountEycharts(echartsNames, echartslineX, echartsValue) {
            var myChart = echarts.init(document.getElementById('main'));
            var charts = {
                unit: '',
                names: echartsNames,
                lineX: echartslineX,
                value: echartsValue,
            };
            var color = [
                'rgb(231,88,64)',
                'rgb(165,101,239)',
                'rgb(98,140,238)',
                'rgb(235,147,88)',
                'rgb(208,92,124)',
                'rgb(187,96,178)',
                'rgb(67,62,124)',
                'rgb(244,122,117)',
                'rgb(0,157,178)',
                'rgb(2,75,81)',
                'rgb(7,128,207)',
                'rgb(118,80,5)',
                'rgb(80,196,143)',
                'rgb(38,204,216)',
                'rgb(54,133,254)',
                'rgb(153,119,239)',
                'rgb(245,97,111)',
                'rgb(247,177,63)',
                'rgb(249,226,100)',
                'rgb(244,122,117)',
            ];
            var lineY = [];

            for (var i = 0; i < charts.names.length; i++) {
                var x = i;
                if (x > color.length - 1) {
                    x = color.length - 1;
                }
                var data = {
                    name: charts.names[i],
                    type: 'line',
                    color: color[x],
                    itemStyle: {normal: {label: {show: true}}},
                    smooth: false,
                    symbol: 'circle',
                    symbolSize: 5,
                    data: charts.value[i],
                    markLine: {
                        data: [
                            {type: 'average', name: '平均值'}
                        ]
                    },
                    markPoint: {
                        label: {
                            normal: {
                                textStyle: {
                                    color: '#fff'
                                }
                            }
                        },
                        data: [{
                            type: 'max',
                            name: '最大值',

                        }, {
                            type: 'min',
                            name: '最小值'
                        }]
                    },
                };
                lineY.push(data);
            }

            var option = {
                backgroundColor: '#fff',
                title: {
                    show: false,
                    text: '每日任务趋势',
                    textStyle: {
                        fontWeight: 'normal',
                        fontSize: 16,
                        color: '#000',
                    },
                    left: '6%',
                    top: '4%',
                },
                tooltip: {
                    trigger: 'axis',
                },

                    // 工具箱
                    toolbox: {
                        show: true,
                        feature: {
                            dataZoom: {
                                yAxisIndex: 'none'
                            },
                            dataView: {readOnly: false},
                            magicType: {type: ['line', 'bar']},
                            restore: {},
                            saveAsImage: {}
                        },
                        top:50
                    },

                legend: {
                    top: '2%',
                    itemStyle: {
                        opacity: 0
                    },
                    lineStyle: {
                        height: 2
                    },
                    data: charts.names,
                    textStyle: {
                        fontSize: 14,
                        color: '#000',
                    },
                    selected: {
                        '学资源': false,
                        '讨论': false,
                        '单题': false,
                        '测验': false,
                        '微课程': false,
                        '一般任务': false,
                        '直播课': false,
                        '答题卡': false,
                        '个性化': false,
                        '先声': false,
                        '爱学派归档': false,
                        '答题卡互批': false,
                        '答题卡自批': false,
                        '答题卡练习册': false,
                        '答题卡附件': false,
                        '答题卡试卷': false,
                        '新答题卡': false,
                        '作业总数': true,
                    }
                },
                dataZoom: [{
                    show: true,
                    height: 30,
                    xAxisIndex: [0],
                    bottom: 30,
                    "start": 85,
                    "end": 100,
                    handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
                    handleSize: '110%',
                    handleStyle: {
                        color: "#5B3AAE",

                    },
                    textStyle: {
                        color: "rgba(204,187,225,0.5)",

                    },
                    fillerColor: "rgba(67,55,160,0.4)",
                    borderColor: "rgba(204,187,225,0.5)",

                }, {
                    type: "inside",
                    show: true,
                    height: 15,
                    start: 1,
                    end: 35
                }],
                grid: {
                    top: '15%',
                    left: '4%',
                    right: '4%',
                    bottom: '10%',
                    containLabel: true,
                },
                xAxis: {
                    show: true,
                    type: 'category',
                    boundaryGap: false,
                    data: charts.lineX,
                    axisTick: {
                        show: false,
                    },
                    axisLabel: {
                        interval: 0,//代表显示所有x轴标签显示
                        rotate: 60,
                        textStyle: {
                            color: '#000',
                        },
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#000',
                        },
                    },
                },
                yAxis: {
                    show: true,
                    splitArea: {
                        show: true,
                        areaStyle: {
                            color: 'transparent',
                        },
                    },
                    name: charts.unit,
                    type: 'value',
                    axisLabel: {
                        formatter: '{value}',
                        textStyle: {
                            color: '#000',
                        },
                    },
                    splitLine: {
                        show: true,
                        lineStyle: {
                            color: '#eee',
                        },
                    },
                    axisLine: {
                        show: false,
                        lineStyle: {
                            color: '#000',
                        },
                    },
                },
                series: lineY,
            };
            setInterval(() => {
                myChart.setOption({
                    legend: {
                        selected: {
                            出口: false,
                            入口: false,
                        },
                    },
                });
                myChart.setOption({
                    legend: {
                        selected: {
                            出口: true,
                            入口: true,
                        },
                    },
                });
            }, 10000);
            myChart.setOption(option);
        },

    },
    mounted() {
        this.getTaskCount();
    }

})
