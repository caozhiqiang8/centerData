var padLicense = new Vue({
    el: '#padLicense',
    delimiters: ['[[', ']]'],
    data: {
        activeName: 'first',
        pad_license_0:'0',
        pad_license_1: '0',
        pad_license_8: '0',
        pad_license_7: '0',
        pad_license_sum: '0',
        padLicense: [],

    },
    methods: {
        handleClick(tab, event) {
            console.log(tab.name, event);
            if (tab.name === 'first') {
                this.getPadLicense()
            }
            if (tab.name === 'second') {

            }
            if (tab.name === 'third') {

            }
            if (tab.name === 'fourth') {

            }

        },
        getPadLicense() {
            axios.get('/padLicenseInfo')
                .then(data => {
                    console.log(data.data.pad_license)
                    this.padLicense = data.data.pad_license
                    this.pad_license_0 = data.data.pad_license_count[0]
                    this.pad_license_1 = data.data.pad_license_count[1]
                    this.pad_license_8 = data.data.pad_license_count[8]
                    this.pad_license_7 = data.data.pad_license_count[7]
                    this.pad_license_sum = this.pad_license_0 + this.pad_license_1 + this.pad_license_8 + this.pad_license_7
                })
                .catch(err => (console.log((err))))
        },
    },
    mounted() {
        this.getPadLicense();
    }

})
