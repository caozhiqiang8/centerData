var monitor = new Vue({
    el: '#monitor',
    delimiters: ['[[', ']]'],
    data: {
        activeName: 'five',
        // 用户行为
        jid: '',
        userActionShow: false,
        userAction: '',
        //接口调用
        date: '',
        urlData: '',
        urlDataShow: false,
        //url分析
        urlBox: [],
        urlBoxShow: false,
        //响应时长
        time: '',
        x_data: '',
        y_data: '',
        model_name: '',
        urlCostTimeShow: false,
        loading: false,
        //视频审核
        videoReviewData: '',
        videoReviewShow: true,
        videoCount: 0,
        userId: '',
        schoolId: '',
        token: '',
        dateVideo: '',
        multipleSelection: [],
        dialogVisible: false,
        resId: '',
        // 默认显示第几页
        currentPage: 1,
        // 默认每页显示的条数（可修改）
        PageSize: 25,
        // 个数选择器（可修改）
        pageSizes: [10, 25, 50, 100, 150, 200,400,600],

    },
    methods: {
        handleClick(tab, event) {
            console.log(tab.name, event);
            if (tab.name === 'first') {
                this.userActionShow = true
                this.urlDataShow = false
                this.urlBoxShow = false
                this.urlCostTimeShow = false
                this.videoReviewShow = false

            }
            if (tab.name === 'second') {
                this.userActionShow = false
                this.urlDataShow = true
                this.urlBoxShow = false
                this.urlCostTimeShow = false
                this.videoReviewShow = false

            }
            if (tab.name === 'third') {
                this.urlBoxEycharts()
                this.userActionShow = false
                this.urlDataShow = false
                this.urlBoxShow = true
                this.urlCostTimeShow = false
                this.videoReviewShow = false

            }
            if (tab.name === 'fourth') {
                this.userActionShow = false
                this.urlDataShow = false
                this.urlBoxShow = false
                this.urlCostTimeShow = true
                this.videoReviewShow = false

            }
            if (tab.name === 'five') {
                this.userActionShow = false
                this.urlDataShow = false
                this.urlBoxShow = false
                this.urlCostTimeShow = false
                this.videoReviewShow = true

            }
        },
        //用户行为日志
        onSubmit() {
            this.loading = true
            axios.post('/userAction', {'jid': this.jid})
                .then(data => {
                    this.userAction = data.data.userAction
                    this.loading = false

                })
                .catch(err => (console.log((err))))
        },
        //获取接口调用
        getUrlData() {
            this.loading = true
            axios.post('/urlCall', {'date': this.date})
                .then(data => {
                    this.urlData = data.data.model_name_agg
                    this.loading = false

                })
                .catch(err => (console.log((err))))
        },
        //url箱型盒子
        getUrlBox() {
            axios.get('/urlBox')
                .then(data => {
                    this.urlBox = data.data.urlBox

                })
                .catch(err => (console.log((err))))
        },
        // url箱型盒子
        urlBoxEycharts() {
            var myChart = echarts.init(document.getElementById('urlBox'));
            var option = {
                title: [
                    {
                        text: 'url响应时长',
                        left: 'center'
                    },

                ],
                dataset: [
                    {
                        // prettier-ignore
                        source: [
                            [842, 842, 2849, 650, 650, 3939, 1730, 3914, 746, 698, 698, 752, 1711, 746, 1916, 69, 3311, 2627, 893,
                                2303, 893, 2303, 1907, 2667, 794, 794, 794, 794, 794, 794, 69, 2927, 794, 794, 794, 1827, 7619, 650, 2551,
                                794, 794, 2705, 1422, 6924, 1678, 842, 1766, 794, 18470, 748, 748, 1580, 1585, 1825, 69, 1609, 1988, 844,
                                701, 69, 13777, 1422, 650, 69, 3644, 7793, 890, 2358, 69, 1832, 794, 794, 1741, 14252, 842, 2343, 1852,
                                2930, 1518, 3308, 1748, 891, 4045, 891, 16359, 749, 1936, 1730, 650, 747, 1516, 3306, 16359, 1786, 794,
                                554, 1540, 794, 794, 1783, 1660, 748, 1832, 2255, 1728, 69, 794, 1507, 1763, 650, 746, 69, 1337, 746,
                                1524, 2801, 795, 650, 1910, 795, 746, 69, 795, 746, 746, 746, 1884, 1820, 650, 650, 1684, 1701, 2934,
                                1943, 2896, 1409, 1823, 650, 1422, 1804, 2935, 1771, 650, 650, 842, 650, 843, 843, 12458, 1578, 6621,
                                1802, 794, 17816, 1821, 699, 3537, 1674, 2562, 845, 2612, 845, 17284, 1854, 1801, 1801, 746, 650, 746,
                                3697, 5536, 8509, 1786, 1955, 1609, 1502, 3936, 2963, 1337, 843, 843, 843, 843, 844, 1684, 1809, 1422,
                                2497, 2900, 842, 69, 1823, 1959, 2459, 700, 9996, 698, 698, 650, 650]
                        ]
                    },
                    {
                        transform: {
                            type: 'boxplot',
                            config: {itemNameFormatter: '异常值 {value}'}
                        }
                    },
                    {
                        fromDatasetIndex: 1,
                        fromTransformResult: 1
                    }
                ],
                tooltip: {
                    trigger: 'item',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                grid: {
                    left: '10%',
                    right: '10%',
                    bottom: '15%'
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: true,
                    nameGap: 30,
                    splitArea: {
                        show: false
                    },
                    splitLine: {
                        show: false
                    }
                },
                yAxis: {
                    type: 'value',
                    name: '毫秒',
                    splitArea: {
                        show: true
                    }
                },
                series: [
                    {
                        name: 'boxplot',
                        type: 'boxplot',
                        datasetIndex: 1,
                        tooltip: {formatter: formatter}
                    },
                    {
                        name: 'outlier',
                        type: 'scatter',
                        datasetIndex: 2
                    }
                ]
            };

            function formatter(param) {
                return [
                    '上边界: ' + param.data[0],
                    '下四分位数: ' + param.data[1],
                    '中位数: ' + param.data[2],
                    '上四分位数: ' + param.data[3],
                    '下边界: ' + param.data[4]
                ].join('<br/>')
            }

            myChart.setOption(option);

        },
        //接口响应时长
        getConstTimeData() {
            this.loading = true
            if (this.date == '') {
                alert('请选择日期')
            } else if (this.time == '') {
                alert('请选择时间')
            } else {
                axios.post('/userAction', {'date': this.date, 'time': this.time})
                    .then(data => {
                        this.model_name = data.data.model_name
                        this.x_data = data.data.x_data
                        this.y_data = data.data.y_data
                        this.urlCostTimeEycharts(this.model_name, this.x_data, this.y_data)
                        this.loading = false

                        // this.$options.methods.urlCostTimeEycharts()

                    })
                    .catch(err => (console.log(err)))
            }

        },
        //获取资源
        getVideoReview() {
            if (this.dateVideo != '' || this.userId != '' || this.schoolId != '') {
                this.loading = true
                axios.post('/videoReview', {'date': this.dateVideo, 'userId': this.userId, 'schoolId': this.schoolId})
                    .then(data => {
                        this.videoReviewData = data.data.videoReviewData
                        this.token = data.data.user_token
                        this.videoCount = data.data.videoCount
                        console.log(data.data.videoCount)
                        this.loading = false
                        this.currentPage = 1
                    })
                    .catch(err => (console.log((err))))
            }


        },
        //删除资源
        delVideo(res_id, index, rows) {
            axios.get('https://school-cloud.ai-classes.com/api-service-resource/resources/delete-res?resId=' + res_id)
                .then(data => {
                    console.log(data.data)
                    if (data.data.code == 1) {
                        rows.splice(index, 1)
                        this.videoCount = this.videoCount - 1
                        this.$notify({
                            title: '成功',
                            message: '删除成功',
                            type: 'success'
                        });

                    }

                })
                .catch(err => (console.log((err))))
        },
        //跳转地址
        toVideo(res_id) {
            window.open('https://school-web.ai-classes.com/ecampus/resourcepreview/index.html?resId=' + res_id + '&token=' + this.token)
        },
        //拉黑用户
        blackUser(user_id) {
            axios.get('https://school-cloud.ai-classes.com/business-service-resource/file-uploads/black-user-insert?userId=' + user_id)
                .then(data => {
                    console.log(data.data)
                    if (data.data.code == 1) {
                        this.$notify({
                            title: '成功',
                            message: '拉黑成功',
                            type: 'success'
                        });

                    }

                })
                .catch(err => (console.log((err))))
        },
        //强改密
        remindUser(user_id) {
            axios.get('https://school-cloud.ai-classes.com/api-service-general/users/remind-user-password?userId=' + user_id)
                .then(data => {
                    console.log(data.data)
                    if (data.data.code == 1) {
                        this.$notify({
                            title: '成功',
                            message: '已强制改密码',
                            type: 'success'
                        });

                    }

                })
                .catch(err => (console.log((err))))
        },
        //表格复选
        toggleSelection(rows) {
            if (rows) {
                rows.forEach(row => {
                    this.$refs.multipleTable.toggleRowSelection(row);
                });
            } else {
                this.$refs.multipleTable.clearSelection();
            }
        },
        handleSelectionChange(val) {
            this.multipleSelection = val;
        },
        // 获取复选框中的资源列表ID
        getResIdList() {
            this.dialogVisible = true
            var resIdList = new Array()
            this.multipleSelection.map((item) => {
                resIdList.push(item.res_id)
            });
            resIdList = resIdList.join(',')
            this.resId = resIdList

        },
        //缓存列表状态
        getRowKeys(row) {
            return row.res_id;
        },
        handleClose(done) {
            this.dialogVisible = false
        },
        // 每页显示的条数
        handleSizeChange(val) {
            console.log(`每页 ${val} 条`);
            // 改变每页显示的条数
            this.PageSize = val
            // 注意：在改变每页显示的条数时，要将页码显示到第一页
            this.currentPage = 1
        },
        // 显示第几页
        handleCurrentChange(val) {

            this.currentPage = val
            console.log(`当前页: ${val}`);
        },
        // 响应时长散点图
        urlCostTimeEycharts(model_name, x_data, y_data) {

            var myChart = echarts.init(document.getElementById('urlCostTime'));
            var color = []
            for (var i = 0; i < model_name.length; i++) {
                let r, g, b
                r = Math.floor(Math.random() * 256)
                g = Math.floor(Math.random() * 256)
                b = Math.floor(Math.random() * 256)
                rgb = 'rgb(' + r + ',' + g + ',' + b + ')'
                color.push(rgb)

            }
            let series_data = []
            for (var i = 0; i < model_name.length; i++) {
                let data = {
                    symbolSize: 6,
                    name: model_name[i],
                    color: color[i],
                    data: y_data[i],
                    type: 'scatter',
                }
                series_data.push(data)

            }
            var option = {
                textStyle: {
                    color: '#545454',
                    fontFamily: 'Source Han Sans',
                    fontWeight: 'lighter'

                },
                tooltip: {
                    trigger: 'item',
                    axisPointer: {
                        type: 'cross',
                        crossStyle: {
                            color: '#999'
                        }
                    }
                },
                legend: {
                    data: model_name
                    ,
                    left: '5%',
                    top: 10,
                    itemWidth: 10,
                    itemHeight: 10,
                    type: "scroll",

                },
                xAxis: {
                    type: 'category',
                    data: x_data

                },
                yAxis: {

                    axisLabel: {
                        formatter: '{value} ms'
                    }
                },
                dataZoom: [
                    {
                        type: 'slider',  //   inside：鼠标滚动   slider：区间缩放条
                        show: true,
                        xAxisIndex: [0],
                        start: 0,
                        end: 100
                    },
                    {
                        type: 'slider',
                        show: true,
                        yAxisIndex: [0],
                        left: '93%',
                        start: 0,
                        end: 100
                    },
                    {
                        type: 'inside',
                        xAxisIndex: [0],
                        start: 0,
                        end: 100
                    },
                    {
                        type: 'inside',
                        yAxisIndex: [0],
                        start: 0,
                        end: 100
                    }
                ],

                // 工具箱
                toolbox: {
                    show: true,
                    showTitle: true,
                    feature: {
                        dataZoom: {
                            yAxisIndex: 'none'
                        },
                        restore: {},
                        saveAsImage: {}
                    },
                    top: 30
                },
                series: series_data
            }

            myChart.setOption(option);
        }

    },
})
