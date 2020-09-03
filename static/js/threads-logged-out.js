let voteBtns = document.querySelectorAll(".vote-btn")

for (let btn of voteBtns) {
    btn.addEventListener("click", () => {
        toastr.info("Please sign up or log in to vote");
    })
}