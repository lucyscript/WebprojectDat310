document.addEventListener("DOMContentLoaded", function() {
    const toggle = document.getElementById("toggle");
    const root = document.documentElement;

    function applyColorScheme() {
        const isDarkMode = toggle.checked;

        if (isDarkMode) {
            root.style.setProperty("--background-color", "var(--background-color-dark)");
            root.style.setProperty("--text-color", "var(--text-color-dark)");
        } else {
            root.style.setProperty("--background-color", "var(--background-color-light)");
            root.style.setProperty("--text-color", "var(--text-color-light)");
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
