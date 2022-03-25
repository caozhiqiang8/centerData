var login = new Vue({
    el: '#login',
    delimiters: ['[[', ']]'],
    data: {
        form: {
            userName: '',
            passWord: ''
        },
        masg: ''

    },
    methods: {
        login() {
            axios.post('/login', {'userName': this.form.userName, 'passWord': this.form.passWord})
                .then(data => {
                    console.log(data.data)

                    if (data.data.code == '0') {
                        window.location = '/index'
                    } else {
                        this.form.userName = ''
                        this.form.passWord = ''
                        this.masg = data.data.masg

                    }
                })
                .catch(err => (console.log(err)))
        }
    }

})