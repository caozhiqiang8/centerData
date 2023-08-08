var map = new Vue({
    el: '#map',
    delimiters: ['[[', ']]'],
    data: {
        loading: true
    },
    methods: {
        getMap() {
            axios.get('/getMap')
                .then(data => {
                    this.loading = true
                    this.data = data.data
                    this.$options.methods.mapEcharts(this.data)
                    this.loading = false
                })
                .catch(err => (console.log(err)))
        },
        mapEcharts(data) {
            //数据来源：国家统计局，本数据不包含香港，澳门，台湾地区
            var myChart = echarts.init(document.getElementById('main'));
            var uploadedDataURL = "static/js/publicJs/data-1528971808162-BkOXf61WX.json";
            var geoCoordMap = {
                '北京': [116.40, 40.40],
                '天津': [117.04, 39.52],
                '河北': [115.21, 38.44],
                '山西': [111.95, 37.65],
                '内蒙古': [112.17, 42.81],
                '辽宁': [123.42, 41.29],
                '吉林': [126.32, 43.38],
                '黑龙江': [128.34, 47.05],
                '上海': [121.46, 31.28],
                '江苏': [120.26, 32.54],
                '浙江': [120.15, 29.28],
                '安徽': [117.28, 31.86],
                '福建': [118.31, 26.07],
                '江西': [115.89, 27.97],
                '山东': [118.01, 36.37],
                '河南': [113.46, 34.25],
                '湖北': [112.29, 30.98],
                '湖南': [112.08, 27.79],
                '广东': [113.98, 22.82],
                '广西': [108.67, 23.68],
                '海南': [110.03, 19.33],
                '重庆': [107.51, 29.63],
                '四川': [103.36, 30.65],
                '贵州': [106.91, 26.67],
                '云南': [101.71, 24.84],
                '西藏': [89.13, 30.66],
                '陕西': [108.94, 34.46],
                '甘肃': [103.82, 36.05],
                '青海': [97.07, 35.62],
                '宁夏': [106.27, 36.76],
                '新疆': [86.61, 40.79],
            };

            var d12 = data.y23_24_1;
            var d11 = data.y22_23_2;
            var d10 = data.y22_23_1;
            var d9 = data.y21_22_2;
            var d8 = data.y21_22_1;
            var d7 = data.y20_21_2;
            var d6 = data.y20_21_1;
            var d5 = data.y19_20_2;
            var d4 = data.y19_20_1;
            var d3 = data.y18_19_2;
            var d2 = data.y18_19_1;
            var d1 = data.y17_18_2;


            var colors = [
                ["#1DE9B6", "#FFFF00", "#04B9FF", "#5DBD32", "#FFC809", "#FB95D5", "#BDA29A", "#6E7074", "#E690D1", "#C4CCD3", "#1DE9B6", "#04B9FF", "#FFC809", "#FB95D5", "#C4CCD3", "#1DE9B6", "#04B9FF", "#FFC809", "#FB95D5"],
                ["#37A2DA", "#FFFF00", "#32C5E9", "#5DBD32", "#FFDB5C", "#FF9F7F", "#FB7293", "#E062AE", "#546570", "#E7BCF3", "#9D96F5", "#8378EA", "#8378EA", "#37A2DA", "#fde8cd", "#32C5E9", "#FFDB5C", "#FF9F7F", "#E7BCF3", "#9D96F5", "#8378EA"],
                ["#DD6B66", "#FFFF00", "#E69D87", "#8DC1A9", "#EA7E53", "#EEDD78", "#73A373", "#73B9BC", "#7289AB", "#91CA8C", "#F49F42", "#73A373", "#73B9BC", "#7289AB", "#91CA8C", "#F49F42", "#DD6B66", "#E69D87", "#EA7E53", "#EEDD78"],
            ];
            var colorIndex = 1;
            $(function () {
                var year = [ "y17_18下", "y18_19上", "y18_19下", "y19_20上", "y19_20下", "y20_21上", "y20_21下", "y21_22上", "y21_22下", "y22_23上", "y22_23下","y23_24上"];
                var mapData = [
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                ];

                /*柱子Y名称*/
                var categoryData = [];
                var barData = [];

                for (var key in geoCoordMap) {
                    mapData[0].push({
                        "year": year[0],
                        "name": key,
                        "value": d1[key],
                    });
                    mapData[1].push({
                        "year": year[1],
                        "name": key,
                        "value": d2[key],
                    });
                    mapData[2].push({
                        "year": year[2],
                        "name": key,
                        "value": d3[key],
                    });
                    mapData[3].push({
                        "year": year[3],
                        "name": key,
                        "value": d4[key],
                    });
                    mapData[4].push({
                        "year": year[4],
                        "name": key,
                        "value": d5[key],
                    });
                    mapData[5].push({
                        "year": year[5],
                        "name": key,
                        "value": d6[key],
                    });
                    mapData[6].push({
                        "year": year[6],
                        "name": key,
                        "value": d7[key],
                    });
                    mapData[7].push({
                        "year": year[7],
                        "name": key,
                        "value": d8[key],
                    });
                    mapData[8].push({
                        "year": year[8],
                        "name": key,
                        "value": d9[key],
                    });
                    mapData[9].push({
                        "year": year[9],
                        "name": key,
                        "value": d10[key],
                    });
                    mapData[10].push({
                        "year": year[10],
                        "name": key,
                        "value": d11[key],
                    });
                    mapData[11].push({
                        "year": year[11],
                        "name": key,
                        "value": d12[key],
                    });

                }

                for (var i = 0; i < mapData.length; i++) {
                    mapData[i].sort(function sortNumber(a, b) {
                        return a.value - b.value
                    });
                    barData.push([]);
                    categoryData.push([]);
                    for (var j = 0; j < mapData[i].length; j++) {
                        barData[i].push(mapData[i][j].value);
                        categoryData[i].push(mapData[i][j].name);
                    }
                }

                $.getJSON(uploadedDataURL, function (geoJson) {

                    echarts.registerMap('china', geoJson);
                    var convertData = function (data) {
                        var res = [];
                        for (var i = 0; i < data.length; i++) {
                            var geoCoord = geoCoordMap[data[i].name];
                            if (geoCoord) {
                                res.push({
                                    name: data[i].name,
                                    value: geoCoord.concat(data[i].value)
                                });
                            }
                        }
                        return res;
                    };
                    optionXyMap01 = {
                        timeline: {// 时间轴
                            data: year,
                            axisType: 'category',
                            autoPlay: true,
                            playInterval: 5000,
                            left: '5%',
                            right: '15%',
                            bottom: '1%',
                            width: '65%',
                            label: {
                                normal: {
                                    textStyle: {
                                        color: '#777'
                                    }
                                },
                                emphasis: {
                                    textStyle: {
                                        color: '#777'
                                    }
                                }
                            },
                            symbolSize: 10,
                            lineStyle: {
                                color: '#555'
                            },
                            checkpointStyle: {
                                borderColor: '#777',
                                borderWidth: 2
                            },
                            controlStyle: {
                                showNextBtn: true,
                                showPrevBtn: true,
                                normal: {
                                    color: '#666',
                                    borderColor: '#666'
                                },
                                emphasis: {
                                    color: '#aaa',
                                    borderColor: '#aaa'
                                }
                            },

                        },
                        baseOption: {
                            animation: true,
                            animationDuration: 1000,
                            animationEasing: 'cubicInOut',
                            animationDurationUpdate: 1000,
                            animationEasingUpdate: 'cubicInOut',
                            grid: {
                                right: '2%',
                                top: '15%',
                                bottom: '5%',
                                width: '20%'
                            },
                            tooltip: {
                                trigger: 'axis', // hover触发器
                                axisPointer: { // 坐标轴指示器，坐标轴触发有效
                                    type: 'shadow', // 默认为直线，可选为：'line' | 'shadow'
                                    shadowStyle: {
                                        color: 'rgba(50,150,150,0.1)' //hover颜色
                                    }
                                }
                            },

                            geo: {
                                show: true,
                                map: 'china',
                                roam: true,
                                zoom: 1.1,
                                center: [113.83531246, 34.0267395887],
                                label: {
                                    emphasis: {
                                        show: false
                                    }
                                },
                                itemStyle: {
                                    normal: {
                                        borderColor: 'rgba(17, 235, 248, 1)',
                                        borderWidth: 1,
                                        areaColor: {
                                            type: 'radial',
                                            x: 0.5,
                                            y: 0.5,
                                            r: 0.8,
                                            colorStops: [{
                                                offset: 0,
                                                color: 'rgba(147, 25, 28, 0)' // 0% 处的颜色
                                            }, {
                                                offset: 1,
                                                color: 'rgba(147, 235, 248, .2)' // 100% 处的颜色
                                            }],
                                            globalCoord: false // 缺省为 false
                                        },
                                        shadowColor: 'rgba(18, 27, 28, 1)',
                                        shadowOffsetX: -2,
                                        shadowOffsetY: 2,
                                        shadowBlur: 10
                                    },
                                }
                            },
                        },
                        options: []

                    };
                    for (var n = 0; n < year.length; n++) {
                        optionXyMap01.options.push({
                            backgroundColor: '#013954',
                            title: [{
                                text: '2017至今学年各省有效学校数(发过任务就算有效)',
                                left: '50%',
                                top: '3%',
                                textStyle: {
                                    color: '#fff',
                                    fontSize: 20
                                }
                            },
                                {
                                    id: 'statistic',
                                    text: year[n] + "学年有效学校数---学校总数：" + data.yearCount[n],
                                    left: '80%',
                                    top: '8%',
                                    textStyle: {
                                        color: '#fff',
                                        fontSize: 18
                                    }
                                }
                            ],

                            xAxis: {
                                type: 'value',
                                scale: true,
                                position: 'top',
                                min: 0,
                                // max: 50,
                                boundaryGap: false,
                                splitNumber: 4,
                                splitLine: {
                                    show: false
                                },
                                axisLine: {
                                    show: false
                                },
                                axisTick: {
                                    show: false
                                },
                                axisLabel: {
                                    margin: 2,
                                    textStyle: {
                                        color: '#aaa'
                                    }

                                },
                            },
                            yAxis: {
                                type: 'category',
                                nameGap: 16,
                                axisLine: {
                                    show: true,
                                    lineStyle: {
                                        color: '#ddd'
                                    }
                                },
                                axisTick: {
                                    show: false,
                                    lineStyle: {
                                        color: '#ddd'
                                    }
                                },
                                axisLabel: {
                                    interval: 0,
                                    textStyle: {
                                        color: '#ddd'
                                    }
                                },
                                data: categoryData[n]
                            },

                            series: [
                                //地图
                                {
                                    type: 'map',
                                    map: 'china',
                                    geoIndex: 0,
                                    aspectScale: 0.8, //长宽比
                                    showLegendSymbol: false, // 存在legend时显示
                                    label: {
                                        normal: {
                                            show: false
                                        },
                                        emphasis: {
                                            show: false,
                                            textStyle: {
                                                color: '#fff'
                                            }
                                        }
                                    },
                                    roam: true,
                                    itemStyle: {
                                        normal: {
                                            areaColor: '#2B91C7',
                                            borderColor: '#FFFFFF',
                                        },
                                        emphasis: {
                                            areaColor: '#2B91B7'
                                        }
                                    },
                                    animation: false,
                                    data: mapData
                                },
                                {
                                    name: 'Top 5',
                                    type: 'scatter',
                                    coordinateSystem: 'geo',
                                    symbol: 'pin',
                                    symbolSize: [50, 50],
                                    label: {
                                        normal: {
                                            show: true,
                                            textStyle: {
                                                color: '#fff',
                                                fontSize: 9,
                                            },
                                            formatter(value) {
                                                return value.data.value[2]
                                            }
                                        }
                                    },
                                    itemStyle: {
                                        normal: {
                                            color: '#D8BC37', //标志颜色
                                        }
                                    },
                                    data: convertData(mapData[n].sort(function (a, b) {
                                        return b.value - a.value;
                                    }).slice(0, 35)),
                                    showEffectOn: 'render',
                                    rippleEffect: {
                                        brushType: 'stroke'
                                    },
                                    hoverAnimation: true,
                                    zlevel: 1
                                },
                                //柱状图
                                {
                                    zlevel: 1.5,
                                    type: 'bar',
                                    barMaxWidth: 10,
                                    symbol: 'none',
                                    itemStyle: {
                                        normal: {
                                            color: colors[colorIndex][n]
                                        }
                                    },
                                    data: barData[n]
                                }
                            ]
                        })
                    }
                    myChart.setOption(optionXyMap01);
                });
            });

        }
    },
    mounted() {
        this.getMap()
    },
})