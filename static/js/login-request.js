let voteBtns = document.querySelectorAll(".vote-btn")

for (let btn of voteBtns) {
    btn.addEventListener("click", () => {
        alert("Please login");
    })
}