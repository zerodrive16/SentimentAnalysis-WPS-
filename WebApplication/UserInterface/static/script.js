function toggleDarkmode() {
    const body = document.body;
    const isDarkMode = body.classList.toggle("dark-mode");

    // Update button text
    this.textContent = isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode";
    console.log("Toggle Dark Mode");
}
document.getElementById("theme-toggle").addEventListener("click", toggleDarkmode);


function createNewComment(){
    const name = document.getElementById("createCommentName").value;
    const commentId = document.getElementById("checkCommentId").value;
    const content = document.getElementById("createCommentContent").value;

    console.log("All data", {name, commentId, content});

    // Clear everything
    document.getElementById("createCommentName").value = "";
    document.getElementById("checkPostId").value = "";
    document.getElementById("createCommentContent").value = "";
}
document.getElementById("createComment").addEventListener("click", function() {
    createNewComment();
});






