var tabs = new Vue({
    el: '#task',
    delimiters: ['[[', ']]'],
    data: {
        activeName: 'first',
    },
    methods: {
        handleClick(tab, event) {
            console.log(tab.name, event);
            if (tab.name === 'first') {
                this.schooType()
            }
            if (tab.name === 'second') {

            }
        },
        schooType() {
            axios.get('/schoolCRM')
                .then(data => {
                    console.log(data.data.school_crm)
                    data = data.data.school_crm

                    this.$options.methods.pie(data)

                })
                .catch(err => (console.log(err)))

        },
        pie(data) {
            var myChart = echarts.init(document.getElementById('schoolType'));
            let bgColor = '#fff';
            let title = '总量';
            let color = ['#2ca1ff','#0adbfa','#febe13','#65e5dd','#7b2cff','#fd5151','#f071ff', '#85f67a','#0baefd','#fdcd0b','#0bfdab','#ff5353','#ff72cb','#8488ff',];
            let echartData = data;

            let formatNumber = function (num) {
                let reg = /(?=(\B)(\d{3})+$)/g;
                return num.toString().replace(reg, ',');
            }
            let total = echartData.reduce((a, b) => {
                return a + b.value * 1
            }, 0);

            option = {
                backgroundColor: bgColor,
                color: color,
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    show: true,
                },
                title: [{
                    text: '{name|' + title + '}\n{val|' + formatNumber(total) + '}',
                    top: 'center',
                    left: 'center',
                    textStyle: {
                        rich: {
                            name: {
                                fontSize: 14,
                                fontWeight: 'normal',
                                color: '#000',
                                padding: [10, 0]
                            },
                            val: {
                                fontSize: 32,
                                fontWeight: 'bolder',
                                color: '#000',
                            }
                        }
                    }
                }, {
                    text: '单位：个',
                    top: 20,
                    left: 20,
                    textStyle: {
                        fontSize: 14,
                        color: '#666666',
                        fontWeight: 400
                    },
                    show: false
                }],
                series: [{
                    type: 'pie',
                    roseType: 'radius',
                    radius: ['25%', '60%'],
                    center: ['50%', '50%'],
                    data: echartData,
                    hoverAnimation: false,
                    itemStyle: {
                        normal: {
                            borderColor: bgColor,
                            borderWidth: 2
                        }
                    },
                    labelLine: {
                        normal: {
                            length: 20,
                            length2: 12,
                            lineStyle: {
                                // color: '#e6e6e6'
                            }
                        }
                    },
                    label: {
                        normal: {
                            formatter: params => {
                                return (
                                    '{icon|●}{name|' + params.name + '}{value|' +
                                    formatNumber(params.value) + '}'
                                );
                            },
                            // padding: [0 , -100, 25, -100],
                            rich: {
                                icon: {
                                    fontSize: 16,
                                    color: 'inherit'
                                },
                                name: {
                                    fontSize: 14,
                                    padding: [0, 0, 0, 10],
                                    color: '#000'
                                },
                                value: {
                                    fontSize: 18,
                                    fontWeight: 'bolder',
                                    padding: [0, 0, 0, 10],
                                    color: 'inherit'
                                    // color: '#333333'
                                }
                            }
                        }
                    },
                }]
            };

            myChart.setOption(option);

        }

    },
    mounted() {
        this.schooType()
    }

})
