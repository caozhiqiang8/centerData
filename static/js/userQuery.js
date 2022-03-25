var userQuery = new Vue({
    el: '#userQuery',
    delimiters: ['[[', ']]'],
    data: {
        form: {
            teaName: '',
            stuName: '',
        },
        msg: '',
        usrInfo:[],
    },
    methods: {
        getUser() {
            console.log(this.form.teaName,this.form.stuName);
            if (this.form.teaName != '' || this.form.stuName != '') {
                axios.post('/userQuery', {'teaName': this.form.teaName,'stuName': this.form.stuName})
                    .then(data => {
                        console.log(data.data.usrInfo);
                        this.form.teaName = ''
                        this.form.stuName = ''
                        this.msg = ''
                        this.usrInfo = data.data.usrInfo
                    })
                    .catch(err => (console.log(err)))
            } else {
                this.msg = '不能为空'
            }

        }
    }

})