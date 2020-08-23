let voteUpElements = document.querySelectorAll(".vote-up");
let voteDownElements = document.querySelectorAll(".vote-down");

async function vote(threadId, upOrDown) {
  let url = "/api/threads/" + threadId + "/vote-" + upOrDown;
  await axios.patch(url);
}

// async function voteCheck(threadId, upOrDown) {
//   let url = "/api/threads/" + threadId + "/vote-" + upOrDown + "-check";
//   let response = await axios.get(url);
//   response.data.response ? console.log(response.data.response) : console.log(response.data.response)
// }

async function voteRemove(threadId, upOrDown) {
  let url = "/api/threads/" + threadId + "/vote-" + upOrDown + "-remove";
  await axios.patch(url);
}

window.addEventListener('load', async (event) => {
  for (let element of voteUpElements) {
    let threadId = (element.id.replace(/^up-+/i, ''));
    let url = "/api/threads/" + threadId + "/vote-" + "up" + "-check";
    let response = await axios.get(url);
    if (response.data.response) {
      element.classList.remove("fa-thumbs-o-up");
      element.classList.add("fa-thumbs-up");
    }
    element.addEventListener("click", () => {
      vote(threadId, "up");
      element.classList.remove("fa-thumbs-o-up");
      element.classList.add("fa-thumbs-up");
      voteRemove(threadId, "down");
      let thumbsDownBtn = document.querySelector("#down-"+threadId);
      thumbsDownBtn.classList.remove("fa-thumbs-down");
      thumbsDownBtn.classList.add("fa-thumbs-o-down");
    })
  }
  for (let element of voteDownElements) {
    let threadId = (element.id.replace(/^down-+/i, ''));
    let url = "/api/threads/" + threadId + "/vote-" + "down" + "-check";
    let response = await axios.get(url);
    if (response.data.response) {
      element.classList.remove("fa-thumbs-o-down");
      element.classList.add("fa-thumbs-down");
    }
    element.addEventListener("click", () => {
      vote(threadId, "down");
      element.classList.remove("fa-thumbs-o-down");
      element.classList.add("fa-thumbs-down");
      voteRemove(threadId, "up");
      let thumbsUpBtn = document.querySelector("#up-"+threadId);
      thumbsUpBtn.classList.remove("fa-thumbs-up");
      thumbsUpBtn.classList.add("fa-thumbs-o-up");
    })
  }
});

// for (let element of voteUpElements) {
//   let threadId = (element.id.replace(/^up-+/i, ''));
//   element.addEventListener("click", () => {
//     vote(threadId, "up");
//     element.classList.remove("fa-thumbs-o-up");
//     element.classList.add("fa-thumbs-up");
//     voteRemove(threadId, "down");
//     let thumbsDownBtn = document.querySelector("#down-"+threadId);
//     thumbsDownBtn.classList.remove("fa-thumbs-down");
//     thumbsDownBtn.classList.add("fa-thumbs-o-down");
//   })
// }

// for (let element of voteDownElements) {
//   let threadId = (element.id.replace(/^down-+/i, ''));
//   element.addEventListener("click", () => {
//     vote(threadId, "down");
//     element.classList.remove("fa-thumbs-o-down");
//     element.classList.add("fa-thumbs-down");
//     voteRemove(threadId, "up");
//     let thumbsUpBtn = document.querySelector("#up-"+threadId);
//     thumbsUpBtn.classList.remove("fa-thumbs-up");
//     thumbsUpBtn.classList.add("fa-thumbs-o-up");
//   })
// }
