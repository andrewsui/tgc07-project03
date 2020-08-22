async function vote(threadId, upOrDown) {
    let url = "/api/threads/" + threadId + "/vote-" + upOrDown;
    console.log(url)
    await axios.patch(url);
}

let voteUpElements = document.querySelectorAll(".vote-up");
let voteDownElements = document.querySelectorAll(".vote-down");

for (let element of voteUpElements) {
    element.addEventListener("click", ()=> {
      let threadId = (element.id.replace(/^up-+/i, ''));
      vote(threadId, "up");
    })
  }

  for (let element of voteDownElements) {
    element.addEventListener("click", ()=> {
      let threadId = (element.id.replace(/^down-+/i, ''));
      vote(threadId, "down");
    })
  }
