let voteUpElements = document.querySelectorAll(".vote-up");
let voteDownElements = document.querySelectorAll(".vote-down");

async function vote(threadId, upOrDown) {
  let url = "/api/threads/" + threadId + "/vote-" + upOrDown;
  await axios.patch(url);
}

async function voteRemove(threadId, upOrDown) {
  let url = "/api/threads/" + threadId + "/vote-" + upOrDown + "-remove";
  await axios.patch(url);
  let thumbsBtn = document.querySelector("#" + upOrDown + "-" + threadId);
  thumbsBtn.classList.remove("fa-thumbs-" + upOrDown );
  thumbsBtn.classList.add("fa-thumbs-o-" + upOrDown );
}

window.addEventListener('load', async (event) => {
  for (let element of voteUpElements) {
    let threadId = (element.id.replace(/^up-+/i, ''));
    let voteCheckUrl = "/api/threads/" + threadId + "/vote-" + "up" + "-check";
    let response = await axios.get(voteCheckUrl);
    if (response.data.response) {
      element.classList.remove("fa-thumbs-o-up");
      element.classList.add("fa-thumbs-up");
    };
    element.addEventListener("click", async () => {
      let response = await axios.get(voteCheckUrl);
      if (response.data.response) {
        voteRemove(threadId, "up");
      } else {
        vote(threadId, "up");
        element.classList.remove("fa-thumbs-o-up");
        element.classList.add("fa-thumbs-up");
        voteRemove(threadId, "down");
      }
    });
  }
  for (let element of voteDownElements) {
    let threadId = (element.id.replace(/^down-+/i, ''));
    let voteCheckUrl = "/api/threads/" + threadId + "/vote-" + "down" + "-check";
    let response = await axios.get(voteCheckUrl);
    if (response.data.response) {
      element.classList.remove("fa-thumbs-o-down");
      element.classList.add("fa-thumbs-down");
    };
    element.addEventListener("click", async () => {
      let response = await axios.get(voteCheckUrl);
      if (response.data.response) {
        voteRemove(threadId, "down");
      } else {
        vote(threadId, "down");
        element.classList.remove("fa-thumbs-o-down");
        element.classList.add("fa-thumbs-down");
        voteRemove(threadId, "up");
      }
    });
  }
});

