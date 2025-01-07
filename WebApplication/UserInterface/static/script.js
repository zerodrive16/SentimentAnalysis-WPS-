function toggleDarkmode() {
  const body = document.body;
  const isDarkMode = body.classList.toggle("dark-mode");
  console.log("Theme toggled:", isDarkMode ? "Dark Mode" : "Light Mode");

  // Update button icon
  var icon = document.getElementById("s1");

  if (isDarkMode) {
    icon.classList.remove("bi-moon");
    icon.classList.add("bi-brightness-high");
  } else {
    icon.classList.remove("bi-brightness-high");
    icon.classList.add("bi-moon");
  }
}
document
  .getElementById("theme-toggle")
  .addEventListener("click", toggleDarkmode);

// Create a new Comment
async function createNewComment() {
  const author = document.getElementById("createCommentAuthor").value;
  const postId = document.getElementById("checkPostId").value;
  const comment_body = document.getElementById("createCommentContent").value;
  const timestamp = document.getElementById("createTimestamp").textContent;
  const personalLabel = document.getElementById("createCommentLabel").value;
  const comment_id = incrementCommentId();
  const comment_body_adjusted = commentRegex(comment_body);

  let dataset;
  try {
    dataset = await retrieveDataFromServer(postId);
    if (!dataset) {
      console.error("Dataset is not retrieved");
      return;
    }
  } catch (error) {
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
    comment_bert_labels: -1,
  };

  // Check if any of the above attributes exists
  for (const key in data) {
    if (data.hasOwnProperty(key)) {
      const value = data[key];
      if (value === null || value === undefined || value === "") {
        return null;
      }
    }
  }
  await sendToPythonScript(data);

  // Clear everything
  document.getElementById("createCommentAuthor").value = "";
  document.getElementById("checkPostId").value = "";
  document.getElementById("createCommentContent").value = "";
  document.getElementById("createCommentLabel").value = "";
}
document.getElementById("createComment").addEventListener("click", function () {
  createNewComment();
});

// Regex for Comment Body
function commentRegex(comment_body) {
  // Remove emojis and non-printable characters
  let regexComment = comment_body.replace(/[^\x00-\x7F]+/g, "");
  // Remove special characters, keeping only letters, numbers and some punctuation like , !, etc...
  regexComment = regexComment.replace(/[^a-zA-Z0-9\s'!,.\?+\-]/g, "");
  // Remove spaces
  regexComment = regexComment.replace(/\s+/g, " ").trim();
  return regexComment;
}

// Retrieving the Dataset from JavaScript to Python
async function retrieveDataFromServer(postId) {
  try {
    const response = await fetch("/dataset/");
    const data = await response.json();
    const getRow = data.find((item) => item.post_id === postId);
    if (getRow) {
      return getRow;
    } else {
      if (getRow.post_id !== postId) {
        showAlert("The PostId is wrong. Give a proper Id!");
      }
      console.log("Row doesn't exist");
    }
  } catch (error) {
    console.error("Error in fetching data!", error);
    return null;
  }
}

// Sending data with API to Python Script
async function sendToPythonScript(data) {
  try {
    const csrfToken = getCSRFToken();
    const response = await fetch("/api/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(data),
    });
    if (response.ok) {
      const result = await response.json();
      console.log("The API call worked with these result: ", result);
    } else {
      const errorResult = await response.text();
      console.error("Error in sending the data to the Script:", errorResult);
    }
  } catch (error) {
    console.log("Error in sending to Python Script");
  }
}

// Get CSRF Token to share resources
function getCSRFToken() {
  const name = "csrftoken";
  const cookies = document.cookie.split("; ");
  for (let cookie of cookies) {
    const [key, ...valueParts] = cookie.split("=");
    if (key === name) {
      return valueParts.join("=");
    }
  }
  return null;
}

// Incrementing the CommentId to keep uniqueness
function incrementCommentId() {
  let commentCounter = parseInt(
    localStorage.getItem("commentCounter") || "0",
    10
  );
  commentCounter++;
  localStorage.setItem("commentCounter", commentCounter);
  return commentCounter;
}

function showAlert(message) {
  // Create a div element for the alert
  const alertElement = document.createElement("div");
  alertElement.style.position = "fixed";
  alertElement.style.top = "20px";
  alertElement.style.left = "50%";
  alertElement.style.transform = "translateX(-50%)";
  alertElement.style.backgroundColor = "#f8d7da";
  alertElement.style.color = "#721c24";
  alertElement.style.padding = "10px 20px";
  alertElement.style.border = "1px solid #f5c6cb";
  alertElement.style.borderRadius = "5px";
  alertElement.style.zIndex = "9999";
  alertElement.style.fontSize = "16px";
  alertElement.style.boxShadow = "0 2px 10px rgba(0, 0, 0, 0.1)";
  alertElement.textContent = message;

  // Append the alert to the body
  document.body.appendChild(alertElement);

  // Remove the alert after 5 seconds
  setTimeout(() => {
    alertElement.remove();
  }, 5000);
}

// PHI
function retrieveDataFromServer() {
  try {
    const response = fetch("/retrieval/");
    const data = response.json();
    id = data.post_id;
    console.log(data);
  } catch (error) {
    console.error("Error in fetching data!", error);
    return null;
  }
}

function createPost(postAuthor, postId, postText, comments) {
  // Create the main post card
  const postCard = document.createElement("div");
  postCard.className = "card mb-3";

  // Post header
  const postHeader = document.createElement("div");
  postHeader.className =
    "card-body ms-2 p-2 d-flex justify-content-between align-items-center";
  postHeader.innerHTML = `
      <h6 class="card-title">${postAuthor}</h6>
      <span class="text">Post ID: ${postId}</span>
    `;

  // Post content
  const postContent = document.createElement("div");
  postContent.className = "card-body ms-2 p-2";
  postContent.innerHTML = `<p class="card-text">${postText}</p>`;

  // Comments section
  const postFooter = document.createElement("div");
  postFooter.className = "card-footer";

  // Comments header
  const commentsHeader = document.createElement("h6");
  commentsHeader.className = "text";
  commentsHeader.textContent = "Comments";

  postFooter.appendChild(commentsHeader);

  // Loop through comments and add them to the comments section
  comments.forEach((comment, index) => {
    const commentCard = document.createElement("div");
    commentCard.className = "card mb-2";

    const commentHeader = document.createElement("div");
    commentHeader.className =
      "card-body p-2 d-flex justify-content-between align-items-center";
    commentHeader.innerHTML = `
        <strong>${comment.author}:</strong>
        <span class="text">Comment #${index + 1}</span>
      `;

    const commentBody = document.createElement("div");
    commentBody.className = "card-body p-2";
    commentBody.innerHTML = `<p class="mb-0">${comment.text}</p>`;

    commentCard.appendChild(commentHeader);
    commentCard.appendChild(commentBody);
    postFooter.appendChild(commentCard);
  });

  // Assemble the post card
  postCard.appendChild(postHeader);
  postCard.appendChild(postContent);
  postCard.appendChild(postFooter);

  // Append the post card to a container on your page
  document.getElementById("post-feed").appendChild(postCard);
}

createPost("KeshaEUW", 2, "WE WIN THOOOOOOOOOOSE!!!!", [
  { author: "T1 Gumayusi", text: "Great post!" },
  { author: "T1 Faker", text: "I totally agree with your post!" },
]);
