// Function to populate sub-categories select option elements
async function displaySubCategories(subCategoriesUrl) {
    // Get sub-categories of specified category
    let response = await axios.get(subCategoriesUrl);
    let parentElement = document.querySelector("#sub_categories");
    // Reset all options within select tag element
    parentElement.innerText = "";
    // Add a wildcard option labelled "Sub-categories" if user doesn't want to select a sub-category
    let wildCardSubCategory = document.createElement("option");
        wildCardSubCategory.value = "";
        wildCardSubCategory.id = "";
        wildCardSubCategory.className = "form-control category-1";
        wildCardSubCategory.innerText = "Sub-categories";
        parentElement.appendChild(wildCardSubCategory);
    // Iterate over sub-category results and add option elements to select tag parent
    for (let subCategory of response.data.results[0].sub_categories) {
        let newElement = document.createElement("option");
        newElement.value = subCategory._id.$oid;
        newElement.id = subCategory._id.$oid;
        newElement.className = "form-control category-1";
        newElement.innerText = subCategory.category;
        parentElement.appendChild(newElement);
    }
}

$( document ).ready(async function() {
    let subCategoriesElement = document.querySelector("#categories");
    // After page loads, if a category is selected then populate sub-categories
    if (subCategoriesElement.value) {
        let subCategoriesUrl = "/api/sub-categories/" + subCategoriesElement.value;
        await displaySubCategories(subCategoriesUrl);
        let previousSubCategoryId = document.querySelector("#previous_sub_categories").value;
        previousSubCategoryId ? document.getElementById(previousSubCategoryId).selected = true : null;
    }
    // Add on-click event listeners to all select category HTML tag's child elements
    $('#categories').change(async function(e){
        // If category option CHANGES, populate its sub-categories (do NOT use on click, because doesn't work on Chrome)
        let subCategoriesUrl = "/api/sub-categories/" + $(this).val();
        await displaySubCategories(subCategoriesUrl);
    })
    // $("#categories").on("click", ".category-0", async function() {
    //     // If category option is clicked, populate its sub-categories
    //     let subCategoriesUrl = "/api/sub-categories/" + this.id;
    //     await displaySubCategories(subCategoriesUrl);
    // })
})