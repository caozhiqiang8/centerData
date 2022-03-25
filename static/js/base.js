var navbar = new Vue({
    el: '#navbar',
    delimiters: ['[[', ']]'],
    data: {
        activeIndex: '',
    },
    methods: {
        handleSelect(key, keyPath) {
            console.log(key,keyPath)
            if (key == 1) {
                window.location = 'index'
            }
            if (key == 3) {
                window.location = 'userQuery'

            }
            if(key == 4){
                window.location = 'task'
            }
        }
    }

})

