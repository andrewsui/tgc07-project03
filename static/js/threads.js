let voteUpElements = document.querySelectorAll(".vote-up");
let voteDownElements = document.querySelectorAll(".vote-down");

async function vote(threadId, upOrDown) {
  let url = "/api/threads/" + threadId + "/vote-" + upOrDown;
  await axios.patch(url);
}

async function voteCheck(threadId, upOrDown) {
  let url = "/api/threads/" + threadId + "/vote-" + upOrDown + "-check";
  let response = await axios.get(url);
  // console.log(response.data.response);
  response.data.response ? console.log(true) : console.log(false)
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
