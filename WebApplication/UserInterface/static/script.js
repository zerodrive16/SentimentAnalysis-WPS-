// Global variable to cache the post groups
let cachedPostGroups = null;

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
      return false;
    }
  } catch (error) {
    console.error("Error retrieving dataset: ", error);
    return false;
  }

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

  for (const key in data) {
    if (data.hasOwnProperty(key)) {
      const value = data[key];
      if (value === null || value === undefined || value === "") {
        console.error(`Invalid value for ${key}: ${value}`);
        return false;
      }
    }
  }

  try {
    await sendToPythonScript(data);
    return true; // Indicate success
  } catch (error) {
    console.error("Error sending to Python script:", error);
    return false;
  }
}

document.getElementById("createComment").addEventListener("click", async function () {
  const authorInput = document.getElementById("createCommentAuthor");
  const postIdInput = document.getElementById("checkPostId");
  const labelInput = document.getElementById("createCommentLabel");
  const contentTextarea = document.getElementById("createCommentContent");
  const errorMessageDiv = document.getElementById("error-message");

  // Helper function to display error messages
  function displayError(message) {
    errorMessageDiv.textContent = message;
    errorMessageDiv.style.display = message ? "block" : "none";
  }

  displayError("");

  // Check if cache is available
  if (!cachedPostGroups) {
    displayError("Data not loaded yet. Please try again in a moment.");
    return;
  }

const validPostIds = Object.keys(cachedPostGroups);

  const validations = [
    {
      condition: (
        !authorInput.value.trim() ||
        !postIdInput.value.trim() ||
        !labelInput.value.trim() ||
        !contentTextarea.value.trim()
      ),
      message: "All fields must be filled out!",
    },
    {
      condition: authorInput.value.length > 50,
      message: "Author name must be 50 characters or less!",
    },
    {
      condition: !validPostIds.includes(String(postIdInput.value.trim())),
      message: "Invalid Post ID! Please select a valid post.",
    },
    {
      condition: !["0", "1"].includes(labelInput.value.trim()),
      message: "Label must be either 0 or 1!",
    },
    {
      condition: contentTextarea.value.length > 500,
      message: "Comment content must be 500 characters or less!",
    },
  ];

for (const { condition, message } of validations) {
    if (condition) {
      displayError(message);
      return;
    }
  }

  const success = await createNewComment();
  if (success) {
    const newComment = {
      author: authorInput.value.trim(),
      text: contentTextarea.value.trim(),
    };
    updatePostFeed(postIdInput.value.trim(), newComment);

    authorInput.value = "";
    postIdInput.value = "";
    labelInput.value = "";
    contentTextarea.value = "";
    displayError("Comment added successfully!");

    const modalElement = document.getElementById("exampleModal");
    const modal = bootstrap.Modal.getInstance(modalElement);
    modal.hide();
  } else {
    displayError("Failed to create comment. Please try again.");
  }
});

// New function to update the post feed UI
function updatePostFeed(postId, comment) {
  const commentsSection = document.getElementById(`commentsSection${postId}`);

  if (!commentsSection) {
    console.error(`Post with ID ${postId} not found in the feed.`);
    return;
  }

  const existingComments = commentsSection.querySelectorAll(".card.mb-2");
  const commentIndex = existingComments.length + 1;

  const commentCard = document.createElement("div");
  commentCard.className = "card mb-2";

  const commentHeader = document.createElement("div");
  commentHeader.className =
    "card-body p-2 d-flex justify-content-between align-items-center";
  commentHeader.innerHTML = `
    <strong>${comment.author}:</strong>
    <span class="text">Comment #${commentIndex}</span>
  `;

  const commentBody = document.createElement("div");
  commentBody.className = "card-body p-2";
  commentBody.innerHTML = `<p class="mb-0">${comment.text}</p>`;

  commentCard.appendChild(commentHeader);
  commentCard.appendChild(commentBody);
  commentsSection.appendChild(commentCard);

  const toggleButton = commentsSection.previousElementSibling;
  if (toggleButton && toggleButton.getAttribute("aria-expanded") === "false") {
    toggleButton.click();
  }
}

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
    const id = data.id;
    console.log(id);
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

// retrieve Data to create post and comments
async function retrieveCommentsData() {
  try {
    const response = await fetch("/retrieval/");
    const data = await response.json();
    console.log(data);
    return data;
  } catch (error) {
    console.error("Error in fetching data!", error);
    return null;
  }
}

function createPost(postAuthor, postId, postText, comments) {
  // Create the main post card
  const postCard = document.createElement("div");
  postCard.className = "card animated-border mb-3";

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

  // Post footer with comment toggle button
  const postFooter = document.createElement("div");
  postFooter.className = "card-footer";

  // Create the toggle button for comments
  const toggleButton = document.createElement("button");
  toggleButton.className = "btn btn-link p-0 text-decoration-none";
  toggleButton.setAttribute("type", "button");
  toggleButton.setAttribute("data-bs-toggle", "collapse");
  toggleButton.setAttribute("data-bs-target", `#commentsSection${postId}`);
  toggleButton.setAttribute("aria-expanded", "false");
  toggleButton.setAttribute("aria-controls", `commentsSection${postId}`);
  toggleButton.textContent = "Show Comments";

  toggleButton.addEventListener("click", () => {
    const isExpanded = toggleButton.getAttribute("aria-expanded") === "true";
    toggleButton.textContent = isExpanded ? "Hide Comments" : "Show Comments";
  });

  // Create the comments section (initially collapsed)
  const commentsSection = document.createElement("div");
  commentsSection.className = "collapse mt-3";
  commentsSection.id = `commentsSection${postId}`;

  // Add comments header
  const commentsHeader = document.createElement("h6");
  commentsHeader.className = "text";
  commentsHeader.textContent = "Comments";
  commentsSection.appendChild(commentsHeader);

  // Loop through comments and add them
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
    commentsSection.appendChild(commentCard);
  });

  // Assemble the post card
  postFooter.appendChild(toggleButton);
  postFooter.appendChild(commentsSection);

  postCard.appendChild(postHeader);
  postCard.appendChild(postContent);
  postCard.appendChild(postFooter);

  // Append the post card to a container on the page
  document.getElementById("post-feed").appendChild(postCard);
}

function groupByPostId(data) {
  return data.reduce((acc, item) => {
    // Use post_id as the key
    const postId = item.post_id;
    if (!acc[postId]) {
      acc[postId] = []; // Initialize an array for this post_id
    }
    acc[postId].push(item); // Add the current item to the array
    return acc;
  }, {});
}

function getRandomSample(array, size) {
  const shuffled = array.slice().sort(() => Math.random() - 0.5);
  return shuffled.slice(0, size);
}

// Loop all data
document.addEventListener("DOMContentLoaded", async () => {
  try {
    // Fetch and cache the data once on page load
    const commentsData = await retrieveCommentsData();

    // Group all comments by their post IDs
    cachedPostGroups = groupByPostId(commentsData);
    console.log("Cached Post Groups:", cachedPostGroups); // For debugging

    // Get all post IDs
    const allPostIds = Object.keys(cachedPostGroups);
    const shownPosts = new Set();

    // Function to create post elements from post data
    function createPostElements(postIds) {
      const posts = postIds.map(postId => {
        const postGroup = cachedPostGroups[postId];
        const { post_author, post_title } = postGroup[0];

        const comments = postGroup.map(post => ({
          author: post.comment_author,
          text: post.comment_body_adjusted,
        }));

        return { post_author, postId, post_title, comments };
      });

      return posts;
    }

    // Function to display posts
    function displayPosts(postIds) {
      // Clear existing posts
      const mainFeed = document.getElementById("post-feed");
      mainFeed.innerHTML = '';

      // Create and append new posts
      const postsToShow = createPostElements(postIds);
      postsToShow.forEach(post => {
        createPost(
          post.post_author,
          post.postId,
          commentRegex(post.post_title),
          post.comments
        );
        shownPosts.add(post.postId);
      });
    }

    // Show first 5 posts
    // const initialPostIds = allPostIds.slice(0, Math.min(5, allPostIds.length))
    const initialPostIds = getRandomSample(allPostIds, Math.min(5, allPostIds.length));
    displayPosts(initialPostIds);

    // Add refresh button functionality
    const showMoreButton = document.getElementById("show-more-posts");
    showMoreButton.addEventListener("click", () => {
      // Get remaining post IDs that haven't been shown
      const remainingPostIds = allPostIds.filter(id => !shownPosts.has(id));

      // If fewer than 5 posts remain, reset the shownPosts set
      if (remainingPostIds.length < 5) {
        shownPosts.clear();
        remainingPostIds.push(...allPostIds);
      }

      // Get 5 random new posts
      const newRandomPostIds = getRandomSample(
        remainingPostIds,
        Math.min(5, remainingPostIds.length)
      );

      displayPosts(newRandomPostIds);
    });

  } catch (error) {
    console.error("Error during initialization:", error);
    cachedPostGroups = {};
  }
});

