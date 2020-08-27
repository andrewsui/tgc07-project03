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
        await voteRemove(threadId, "up");
      } else {
        await vote(threadId, "up");
        element.classList.remove("fa-thumbs-o-up");
        element.classList.add("fa-thumbs-up");
        await voteRemove(threadId, "down");
      }
      await updateVoteCount();
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
        await voteRemove(threadId, "down");
      } else {
        await vote(threadId, "down");
        element.classList.remove("fa-thumbs-o-down");
        element.classList.add("fa-thumbs-down");
        await voteRemove(threadId, "up");
      }
      await updateVoteCount();
    });
  }
});

