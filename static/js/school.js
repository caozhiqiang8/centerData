var tabs = new Vue({
    el: '#task',
    delimiters: ['[[', ']]'],
    data: {
        activeName: 'second',
        schooldata: [],
        schoolTypeShow: false,
        schoolInfoShow: true,
        tableColumns: [
            {
                prop: "school_id",
                label: "学校ID",
            },
            {
                prop: "name",
                label: "学校名称",
            },
            {
                prop: "province",
                label: "省",
            },
            {
                prop: "city",
                label: "市",
            },
            {
                prop: "c_time",
                label: "创建时间",
            },
            {
                prop: "validity_time",
                label: "到期时间",
            },
            {
                prop: "ip",
                label: "地址",
            },
            {
                prop: "user_name",
                label: "用户名",
            },
            {
                prop: "password",
                label: "密码",
            },

        ],
        school_name: '',
        school_id: '',
        schoolSgShow: false,
        sg_id: '',
        sgData: '',
    },
    methods: {
        handleClick(tab, event) {
            console.log(tab.name, event);
            if (tab.name === 'second') {
                this.schoolInfoShow = true
                this.schoolSgShow = false

            }
            if (tab.name === 'first') {
                this.schoolInfoShow = false
                this.schoolSgShow = true

            }
        },
        schooType() {
            axios.get('/schoolCRM')
                .then(data => {
                    data = data.data.school_crm
                    this.$options.methods.pie(data)

                })
                .catch(err => (console.log(err)))

        },
        pie(data) {
            var myChart = echarts.init(document.getElementById('schoolType'));
            let bgColor = '#fff';
            let title = '总量';
            let color = ['#2ca1ff', '#0adbfa', '#febe13', '#65e5dd', '#7b2cff', '#fd5151', '#f071ff', '#85f67a', '#0baefd', '#fdcd0b', '#0bfdab', '#ff5353', '#ff72cb', '#8488ff',];
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

        },
        schoolInfo() {
            if (this.school_name == '' || this.school_id == '') {
                console.log('请输入学校名称或id')
            } else {
                axios.post('/schoolInfo', {'school_name': this.school_name, 'school_id': this.school_id})
                    .then(data => {
                            this.schooldata = data.data.schoolInfo
                        }
                    )
                    .catch(err => (console.log(err)))
            }

        },
        sgSchoolData() {
            if (this.sg_id != '') {
                axios.post('/sgData', {'sg_id': this.sg_id})
                    .then(data => {
                        this.sgData = data.data.sg_data
                    })
                    .catch(err => (console.log(err)))
            }

        }

    },
    mounted() {

    }

})
