var userQuery = new Vue({
    el: '#userQuery',
    delimiters: ['[[', ']]'],
    data: {
        activeName: 'first',//二级导航
        userQuery: true,
        schoolQuery: false,
        form: {
            teaName: '',
            stuName: '',
        },
        usrInfo: [],
        schoolInfo: [],
        options: [{
            value: '1',
            label: '教师'
        }, {
            value: '2',
            label: '学生'
        },],
        schoolId: '',
        value: '',
        tableColumns: [
            {
                prop: "jid",
                label: "jid",
            },
            {
                prop: "user_id",
                label: "user_id",
            },
            {
                prop: "name",
                label: "姓名",
            },
            {
                prop: "user_name",
                label: "用户名",
            },
            {
                prop: "password",
                label: "密码",
            },
            {
                prop: "stu_no",
                label: "学号",
            },
            {
                prop: "stu_district_no",
                label: "区考号",
            },
            {
                prop: "class_grade",
                label: "年级",
            },
            {
                prop: "class_name",
                label: "班级",
            },
        ],

    },
    methods: {
        handleClick(tab, event) {
            console.log(tab.name, event);
            if (tab.name === 'first') {
                this.userQuery = true
                this.schoolQuery = false
            }
            if (tab.name === 'second') {
                this.userQuery = false
                this.schoolQuery = true

            }

        },
        getUser() {
            console.log(this.form.teaName, this.form.stuName);
            if (this.form.teaName != '' || this.form.stuName != '') {
                axios.post('/userQuery', {'teaName': this.form.teaName, 'stuName': this.form.stuName})
                    .then(data => {
                        console.log(data.data.usrInfo);
                        this.form.teaName = ''
                        this.form.stuName = ''
                        this.msg = ''
                        this.usrInfo = data.data.usrInfo
                    })
                    .catch(err => (console.log(err)))
            } else {
                console.log('不能为空')
            }

        },
        getSchool() {
            if (this.value != '' || this.schoolId != '') {
                axios.post('/schoolQuery', {'code': this.value, 'schoolId': this.schoolId})
                    .then(data => {
                        this.schoolInfo = data.data.schoolInfo
                    })
                    .catch(err => (console.log(err)))

            } else {
                console.log('不能为空')
            }
        },
        download() {
            axios.post('/download',{'data':this.schoolInfo},{responseType:'blob'})
                .then(data => {
                    let file = data.data;
                    const blob = new Blob([file], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; charset=utf-8'})
                    let link = document.createElement('a')
                    link.href = window.URL.createObjectURL(blob)
                    link.download = this.schoolId + '学校帐号密码.xlsx'
                    link.click()

                })
                .catch(err => (console.log(err)))
        }

    }

})