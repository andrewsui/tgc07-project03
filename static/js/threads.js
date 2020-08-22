let voteUpElements = document.querySelectorAll(".vote-up");
let voteDownElements = document.querySelectorAll(".vote-down");

async function vote(threadId, upOrDown) {
    let url = "/api/threads/" + threadId + "/vote-" + upOrDown;
    // console.log(url);
    await axios.patch(url);
}

for (let element of voteUpElements) {
    element.addEventListener("click", () => {
      let threadId = (element.id.replace(/^up-+/i, ''));
    //   vote(threadId, "up");
    //   element.classList.remove("fa-thumbs-o-up");
    //   element.classList.add("fa-thumbs-up");
    })
  }

  for (let element of voteDownElements) {
    element.addEventListener("click", () => {
      let threadId = (element.id.replace(/^down-+/i, ''));
    //   vote(threadId, "down");
    //   element.classList.remove("fa-thumbs-o-down");
    //   element.classList.add("fa-thumbs-down");
    })
  }
