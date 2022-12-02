var book = new Vue({
    el: '#book',
    delimiters: ['[[', ']]'],
    data: {
        activeName: 'first',
        bookInfo: [],
        bookCount: 0,
        bookPaperCount: 0,
        schoolCount:0,
        bookGradeSubject: [],
        bookSchool: [],
        schoolBook: [],
        bookInfoShow: true,
        bookGradeSubjectShow: false,
        bookSchoolShow: false,
        schoolBookShow: false,

    },
    methods: {
        handleClick(tab, event) {
            console.log(tab.name, event);
            if (tab.name === 'first') {
                this.getBookInfo()
                this.bookInfoShow = true
                this.bookGradeSubjectShow = false
                this.bookSchoolShow = false
                this.schoolBookShow = false
            }
            if (tab.name === 'second') {
                this.getBookGradeSubject()
                this.bookInfoShow = false
                this.bookGradeSubjectShow = true
                this.bookSchoolShow = false
                this.schoolBookShow = false
            }
            if (tab.name === 'third') {
                this.getbookSchool()
                this.bookInfoShow = false
                this.bookGradeSubjectShow = false
                this.bookSchoolShow = true
                this.schoolBookShow = false
            }
            if (tab.name === 'fourth') {
                this.getschoolBook()
                this.bookInfoShow = false
                this.bookGradeSubjectShow = false
                this.bookSchoolShow = false
                this.schoolBookShow = true
            }

        },
        getBookInfo() {
            axios.get('/bookInfo?code=1')
                .then(data => {
                    this.bookInfo = data.data.bookInfo
                    this.bookCount = data.data.bookCount
                    this.bookPaperCount = data.data.bookPaperCount
                    this.schoolCount = data.data.schoolCount
                })
                .catch(err => (console.log((err))))
        },
        getBookGradeSubject() {
            axios.get('/bookInfo?code=2')
                .then(data => {
                    this.bookGradeSubject = data.data.bookGradeSubject
                })
                .catch(err => (console.log((err))))
        },
        getbookSchool() {
            axios.get('/bookInfo?code=3')
                .then(data => {
                    this.bookSchool = data.data.bookSchool
                })
                .catch(err => (console.log((err))))
        },
        getschoolBook() {
            axios.get('/bookInfo?code=4')
                .then(data => {
                    this.schoolBook = data.data.schoolBook
                })
                .catch(err => (console.log((err))))
        },

    },
    mounted() {
        this.getBookInfo();
    }


})
