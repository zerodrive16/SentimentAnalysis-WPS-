document.getElementById("theme-toggle").addEventListener("click", function () {
    const body = document.body;
    const isDarkMode = body.classList.toggle("dark-mode");

    // Update button text
    this.textContent = isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode";
});
