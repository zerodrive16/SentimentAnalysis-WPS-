function toggleDarkmode() {
    const body = document.body;
    const isDarkMode = body.classList.toggle("dark-mode");

    // Update button text
    this.textContent = isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode";
    console.log("Toggle Dark Mode");
}
document.getElementById("theme-toggle").addEventListener("click", toggleDarkmode);


async function createNewComment(){
    const author = document.getElementById("createCommentAuthor").value;
    const postId = document.getElementById("checkPostId").value;
    const comment_body = document.getElementById("createCommentContent").value;
    const timestamp = document.getElementById("createTimestamp").textContent;
    const personalLabel = document.getElementById("createCommentLabel").value;
    let comment_id = 0;
    comment_id++;
    const comment_body_adjusted = commentRegex(comment_body);

    let dataset;
    try {
        dataset = await retrieveDataFromServer();
        if(!dataset){
            console.error("Dataset is not retrieved");
            return;
        }
    } catch(error) {
        console.error("Error retrieving dataset: ", error);
        return;
    }

    // data preparation
    const data = {
        post_id: postId,
        post_author: dataset.post_author,
        post_title: dataset.post_title,
        post_created: dataset.post_created,
        post_up_votes: dataset.post_up_votes,
        c_id: dataset.c_id,
        comment_id: comment_id,
        comment_author: author,
        comment_body: comment_body,
        comment_body_adjusted: comment_body_adjusted,
        comment_created: timestamp,
        comment_up_votes: 1,
        subreddit: "AskReddit",
        comment_personal_labels: personalLabel,
        comment_bert_labels: "pass"
    };

    // Check if any of the above attributes exists
    for(const key in data){
        if(data.hasOwnProperty(key)){
            const value = data[key];
            if(value === null || value === undefined || value === ""){
                return null;
            }
        }
    }
    console.log(data);

    // Clear everything
    document.getElementById("createCommentAuthor").value = "";
    document.getElementById("checkPostId").value = "";
    document.getElementById("createCommentContent").value = "";
    document.getElementById("createCommentLabel").value = "";
}
document.getElementById("createComment").addEventListener("click", function(){
    createNewComment();
});

function commentRegex(comment_body){
    // Remove emojis and non-printable characters
    let regexComment = comment_body.replace(/[^\x00-\x7F]+/g, '');
    // Remove special characters, keeping only letters, numbers and some punctuation like , !, etc...
    regexComment = regexComment.replace(/[^a-zA-Z0-9\s'!,.\?+\-]/g, '');
    // Remove spaces
    regexComment = regexComment.replace(/\s+/g, ' ').trim();
    return regexComment;
}

async function retrieveDataFromServer(){
    try {
        const response = await fetch("/dataset/");
        const data = await response.json();
        const getRow = data.find(item => item.comment_id === "lyewszs");
        if(getRow) {
            return getRow;
        } else {
            console.log("Row doesn't exist");
        }
    } catch(error) {
        console.error("Error in fetching data!", error);
        return null;
    }
}




