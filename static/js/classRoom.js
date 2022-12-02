var classRoom = new Vue({
    el: '#classRoom',
    delimiters: ['[[', ']]'],
    data: {
        activeName: 'first',
        axpSchool: [],
        axpClassCount: 0,
        axpClassRenewCount: 0,
        axpClassNewCount: 0,
        axpClass: [],
        axpSchoolShow: true,
        axpClassShow: false,


    },
    methods: {
        handleClick(tab, event) {
            console.log(tab.name, event);
            if (tab.name === 'first') {
                this.getClassRoomInfo();
                this.axpSchoolShow = true
                this.axpClassShow = false
            }
            if (tab.name === 'second') {
                this.getAxpClass();
                this.axpSchoolShow = false
                this.axpClassShow = true
            }
            if (tab.name === 'third') {

            }
            if (tab.name === 'fourth') {

            }

        },
        getClassRoomInfo() {
            axios.get('/classRoomInfo?code=1')
                .then(data => {
                    this.axpSchool = data.data.axpSchool
                    this.axpClassCount = data.data.axpClassCount
                    this.axpClassRenewCount = data.data.axpClassRenewCount
                    this.axpClassNewCount = data.data.axpClassNewCount

                })
                .catch(err => (console.log((err))))
        },
        getAxpClass() {
            axios.get('/classRoomInfo?code=2')
                .then(data => {
                    this.axpClass = data.data.axpClass

                })
                .catch(err => (console.log((err))))

        }

    },
    mounted() {
        this.getClassRoomInfo();
    }

})
