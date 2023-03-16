var padLicense = new Vue({
    el: '#padLicense',
    delimiters: ['[[', ']]'],
    data: {
        activeName: 'second',
        pad_license_0:'0',
        pad_license_1: '0',
        pad_license_8: '0',
        pad_license_7: '0',
        pad_license_sum: '0',
        firstShow:false,
        secondShow:true,
        padLicense: [],

    },
    methods: {
        handleClick(tab, event) {
            console.log(tab.name, event);
            if (tab.name === 'first') {
                this.getPadLicense()
                this.firstShow = true
                this.secondShow = false
            }
            if (tab.name === 'second') {
                this.getPadLicensePau()
                this.firstShow = false
                this.secondShow = true
            }
            if (tab.name === 'third') {
                this.getPadLicensePauH()
                this.firstShow = false
                this.secondShow = true
            }
            if (tab.name === 'fourth') {

            }

        },
        getPadLicense() {
            axios.get('/padLicenseInfo')
                .then(data => {
                    console.log(data.data.pad_license)
                    this.padLicense = data.data.pad_license
                    this.pad_license_0 = data.data.pad_license_count[0]
                    this.pad_license_1 = data.data.pad_license_count[1]
                    this.pad_license_8 = data.data.pad_license_count[8]
                    this.pad_license_7 = data.data.pad_license_count[7]
                    this.pad_license_sum = this.pad_license_0 + this.pad_license_1 + this.pad_license_8 + this.pad_license_7
                })
                .catch(err => (console.log((err))))
        },
        getPadLicensePau(){
            axios.get('/padLicenseDau?res=0')
                .then(data =>{
                    console.log(data.data)
                    this.echartsNames = ['活跃次数','活跃人数']
                    this.echartslineX = data.data.data_x
                    this.echartsValue = data.data.data_y
                    this.$options.methods.eycharts(this.echartsNames, this.echartslineX, this.echartsValue)

                })
                .catch(err =>(console.log(err)))
        },
        getPadLicensePauH(){
            axios.get('/padLicenseDau?res=1')
                .then(data =>{
                    console.log(data.data)
                    this.echartsNames = ['活跃次数','活跃人数']
                    this.echartslineX = data.data.data_x
                    this.echartsValue = data.data.data_y
                    this.$options.methods.eycharts(this.echartsNames, this.echartslineX, this.echartsValue)

                })
                .catch(err =>(console.log(err)))
        },
        eycharts(echartsNames, echartslineX, echartsValue) {
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
                    top: 50
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
                        '活跃次数': false,

                    }

                },
                dataZoom: [{
                    show: true,
                    height: 30,
                    xAxisIndex: [0],
                    bottom: 30,
                    "start": 0,
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
        this.getPadLicensePau();
    }

})
