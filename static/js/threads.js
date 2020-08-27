let voteUpElements = document.querySelectorAll(".vote-up");
let voteDownElements = document.querySelectorAll(".vote-down");

// Function to cast up or down vote via API endpoint
async function vote(threadId, upOrDown) {
  let url = "/api/threads/" + threadId + "/vote-" + upOrDown;
  await axios.patch(url);
}

// Function to remove vote via API endpoint
async function voteRemove(threadId, upOrDown) {
  let url = "/api/threads/" + threadId + "/vote-" + upOrDown + "-remove";
  await axios.patch(url);
  let thumbsBtn = document.querySelector("#" + upOrDown + "-" + threadId);
  thumbsBtn.classList.remove("fa-thumbs-" + upOrDown );
  thumbsBtn.classList.add("fa-thumbs-o-" + upOrDown );
}

window.addEventListener('load', async (event) => {
  // After page loaded, iterate over vote-up buttons
  for (let element of voteUpElements) {
    // Get thread ID from element's HTML ID
    let threadId = (element.id.replace(/^up-+/i, ''));
    // Check if user has an existing vote on this thread
    let voteCheckUrl = "/api/threads/" + threadId + "/vote-" + "up" + "-check";
    let response = await axios.get(voteCheckUrl);
    // If user has existing vote on this thread, then update button to show vote
    if (response.data.response) {
      element.classList.remove("fa-thumbs-o-up");
      element.classList.add("fa-thumbs-up");
    };
    // When up-vote button is clicked:
    element.addEventListener("click", async () => {
      // Check if user has an existing vote on this thread
      let response = await axios.get(voteCheckUrl);
      if (response.data.response) {
        // If user has existing vote, remove vote
        await voteRemove(threadId, "up");
      } else {
        // Otherwise, cast vote
        await vote(threadId, "up");
        element.classList.remove("fa-thumbs-o-up");
        element.classList.add("fa-thumbs-up");
        await voteRemove(threadId, "down");
      }
      // Update vote count tally element
      await updateVoteCount();
    });
  }
  // After page loaded, iterate over vote-down buttons
  for (let element of voteDownElements) {
    // Get thread ID from element's HTML ID
    let threadId = (element.id.replace(/^down-+/i, ''));
    // Check if user has an existing vote on this thread
    let voteCheckUrl = "/api/threads/" + threadId + "/vote-" + "down" + "-check";
    let response = await axios.get(voteCheckUrl);
    // If user has existing vote on this thread, then update button to show vote
    if (response.data.response) {
      element.classList.remove("fa-thumbs-o-down");
      element.classList.add("fa-thumbs-down");
    };
    // When down-vote button is clicked:
    element.addEventListener("click", async () => {
      // Check if user has an existing vote on this thread
      let response = await axios.get(voteCheckUrl);
      if (response.data.response) {
        // If user has existing vote, remove vote
        await voteRemove(threadId, "down");
      } else {
        // Otherwise, cast vote
        await vote(threadId, "down");
        element.classList.remove("fa-thumbs-o-down");
        element.classList.add("fa-thumbs-down");
        await voteRemove(threadId, "up");
      }
      // Update vote count tally element
      await updateVoteCount();
    });
  }
});

