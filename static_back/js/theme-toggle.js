// Theme Toggle Functionality
function toggleTheme() {
    // Toggle theme based on the current theme
    if (document.body.getAttribute("data-theme") === "dark") {
        // Switch to light mode
        document.body.setAttribute("data-theme", "light");
        localStorage.setItem("theme", "light");
    } else {
        // Switch to dark mode
        document.body.setAttribute("data-theme", "dark");
        localStorage.setItem("theme", "dark");
    }
}

// Set theme on load based on user preference
document.addEventListener("DOMContentLoaded", function () {
    // Retrieve the user's theme preference from localStorage
    const savedTheme = localStorage.getItem("theme");

    // Apply the user's saved theme preference once on page load
    if (savedTheme) {
        document.body.setAttribute("data-theme", savedTheme);
    } else {
        // Default to light theme if no preference saved
        document.body.setAttribute("data-theme", "light");
    }
});

// Ensure the theme does not unintentionally toggle when clicking other elements
document.querySelectorAll('button.toggle-theme').forEach(button => {
    button.addEventListener("click", toggleTheme);
});
