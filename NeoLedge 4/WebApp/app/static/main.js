const { createApp } = Vue

const ImageApp = {
    data() {
        return {
            images: [],
            selectedImage: null
        }
    },
    async created() {
        await this.getImages()
    },
    methods: {
        async sendRequest(url, method, data) {
            const myHeaders = new Headers({
                'X-Requested-With': 'XMLHttpRequest'
            })
            const response = await fetch(url, {
                method: method,
                headers: myHeaders,
                body: data
            })
            return response 
        },

        async getImages() {
            const response = await this.sendRequest(window.location, 'get')
            this.images = await response.json()
        },
        onImageSelected(event) {
            this.selectedImage = event.target.files[0]
        },
        async uploadImage() {
            if (this.selectedImage) {
                const formData = new FormData()
                formData.append('image', this.selectedImage)
                await fetch(window.location + 'upload', {
                    method: 'post',
                    body: formData
                })
                this.selectedImage = null
                await this.getImages()
            } else {
                alert('Please select an image to upload.')
            }
        }
    },
    delimiters: ['{', '}']
}

createApp(ImageApp).mount('#app')
