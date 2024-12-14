function toggleDarkmode() {
    const body = document.body;
    const isDarkMode = body.classList.toggle("dark-mode");

    // Update button text
    this.textContent = isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode";
    console.log("Toggle Dark Mode");
}
document.getElementById("theme-toggle").addEventListener("click", toggleDarkmode);









