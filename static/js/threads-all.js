// Update vote counts for all threads
async function updateVoteCount() {
    for (let element of document.querySelectorAll(".vote-count")) {
        // Get thread ID from element's HTML ID
        let threadId = element.id.replace(/^vote-count-+/i, '');
        // Get number of up and down votes
        let upVotesResponse = await axios.get("/api/threads/" + threadId + "/vote-count/up");
        let downVotesResponse = await axios.get("/api/threads/" + threadId + "/vote-count/down");
        let upVotes = upVotesResponse.data.number_of_up_votes;
        let downVotes = downVotesResponse.data.number_of_down_votes;
        // Display net number of votes
        element.innerText = upVotes - downVotes;
    }
}

// Function to get comment count of review thread
async function updateCommentCount() {
    for (let element of document.querySelectorAll(".comment-count")) {
        // Get thread ID from element's HTML ID
        let threadId = (element.id.replace(/^comment-count-+/i, ''));
        // Get comments count from API endpoint
        let commentsCountResponse = await axios.get("/api/threads/" + threadId + "/comments/count");
        element.innerHTML =  String.raw`<i class="fa fa-comments" aria-hidden="true"></i> ` + commentsCountResponse.data.comments;
    }
}

window.addEventListener('load', async () => {
    await updateVoteCount();
    await updateCommentCount();
});