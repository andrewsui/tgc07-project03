async function displaySubCategories(subCategoriesUrl) {
    let response = await axios.get(subCategoriesUrl);
    let parentElement = document.querySelector("#sub_categories");
    parentElement.innerText = "";
    // console.log(response.data.results[0].sub_categories);
    for (let subCategory of response.data.results[0].sub_categories) {
        // console.log(subCategory.category)
        // console.log(subCategory._id.$oid)
        // console.log(this.value)
        let newElement = document.createElement("option");
        newElement.value = subCategory._id.$oid;
        newElement.id = subCategory._id.$oid;
        newElement.className = "category-1";
        newElement.innerText = subCategory.category;
        parentElement.appendChild(newElement);
    }
}

$("#categories").on("click", ".category-0", async function() {
    let subCategoriesUrl = "/api/sub-categories/" + this.id;
    await displaySubCategories(subCategoriesUrl);
    // let response = await axios.get(subCategoriesUrl);
    // let parentElement = document.querySelector("#sub_categories");
    // parentElement.innerText = "";
    // console.log(response.data.results[0].sub_categories);
    // for (let subCategory of response.data.results[0].sub_categories) {
    //     console.log(subCategory.category)
    //     console.log(subCategory._id.$oid)
    //     console.log(this.value)
    //     let newElement = document.createElement("option");
    //     newElement.value = subCategory._id.$oid;
    //     newElement.id = subCategory._id.$oid;
    //     newElement.className = "category-1";
    //     newElement.innerText = subCategory.category;
    //     parentElement.appendChild(newElement);
    // }
})

window.addEventListener('load', async (event) => {
    let subCategoriesElement = document.querySelector("#categories");
    let subCategoriesUrl = "/api/sub-categories/" + subCategoriesElement.value;
    await displaySubCategories(subCategoriesUrl);
    let previousSubCategoryId = document.querySelector("#previous_sub_categories").value;
    previousSubCategoryId ? document.getElementById(previousSubCategoryId).selected = true : null;
    // let response = await axios.get(subCategoriesUrl);
    // let parentElement = document.querySelector("#sub_categories");
    // parentElement.innerText = "";
    // console.log(response.data.results[0].sub_categories);
    // for (let subCategory of response.data.results[0].sub_categories) {
    //     console.log(subCategory.category)
    //     console.log(subCategory._id.$oid)
    //     console.log(this.value)
    //     let newElement = document.createElement("option");
    //     newElement.value = subCategory._id.$oid;
    //     newElement.id = subCategory._id.$oid;
    //     newElement.className = "category-1";
    //     newElement.innerText = subCategory.category;
    //     parentElement.appendChild(newElement);
    // }
})