async function updateVoteCount() {
    for (let element of document.querySelectorAll(".vote-count")) {
        let threadId = element.id.replace(/^count-+/i, '');
        let upVotesResponse = await axios.get("/api/threads/" + threadId + "/vote-count/up");
        let downVotesResponse = await axios.get("/api/threads/" + threadId + "/vote-count/down");
        let upVotes = upVotesResponse.data.number_of_up_votes;
        let downVotes = downVotesResponse.data.number_of_down_votes;
        element.innerText = upVotes - downVotes;
    }
}

window.addEventListener('load', async (event) => await updateVoteCount());