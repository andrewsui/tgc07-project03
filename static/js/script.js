$('#categories').on('click', ".category-0", async function() {
    console.log(this.id)
    let response = await axios.get('http://localhost:8080/api/categories')
    // console.log(response.data)
    for (let category of response.data.categories) {
        if (category.category===this.id) {
            // console.log(category.sub_categories)
            for (let sub_category of category.sub_categories) {
                console.log(sub_category.category)
            }
        }
    }
})
