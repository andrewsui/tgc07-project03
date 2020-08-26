async function displaySubCategories(subCategoriesUrl) {
    let response = await axios.get(subCategoriesUrl);
    let parentElement = document.querySelector("#sub_categories");
    parentElement.innerText = "";
    let wildCardSubCategory = document.createElement("option");
        wildCardSubCategory.value = "";
        wildCardSubCategory.id = "";
        wildCardSubCategory.className = "category-1";
        wildCardSubCategory.innerText = "Sub-categories";
        parentElement.appendChild(wildCardSubCategory);
    for (let subCategory of response.data.results[0].sub_categories) {
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
})

window.addEventListener('load', async (event) => {
    let subCategoriesElement = document.querySelector("#categories");
    if (subCategoriesElement.value) {
        let subCategoriesUrl = "/api/sub-categories/" + subCategoriesElement.value;
        await displaySubCategories(subCategoriesUrl);
        let previousSubCategoryId = document.querySelector("#previous_sub_categories").value;
        previousSubCategoryId ? document.getElementById(previousSubCategoryId).selected = true : null;
    }
})