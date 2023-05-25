document.addEventListener("DOMContentLoaded", function() {
    const toggle = document.getElementById("toggle");
    const root = document.documentElement;

    function applyColorScheme() {
        const isDarkMode = toggle.checked;

        if (isDarkMode) {
            root.classList.add("dark-theme");
        } else {
            root.classList.remove("dark-theme");
        }

        localStorage.setItem("colorScheme", isDarkMode ? "dark" : "light");
    }

    toggle.addEventListener("change", applyColorScheme);
    

    const savedColorScheme = localStorage.getItem("colorScheme");
    if (savedColorScheme === "dark") {
        toggle.checked = true;
    }

    applyColorScheme();
});