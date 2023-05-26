// SEARCH RECOMEND
$('#search').on('keydown', function(event) {
    if (event.keyCode === 13) {
    event.preventDefault(); 
    }
});
const search = document.getElementById("searchbar-form");
search.addEventListener("input", function(event){
    const xhttp = new XMLHttpRequest();
    xhttp.responseType = "json";
    xhttp.onload = function() {
        const items = this.response;
        container = document.getElementById("drop-down-suggestion")
        container.innerHTML = "";

        const table = document.createElement("table");

        for (let i = 0; i < items.length; i++) {
            const tr = document.createElement("tr");
            const td1 = document.createElement("td");
            const td2 = document.createElement("td");
            const th = document.createElement("th");
            const img = document.createElement("img");
            
            const item = items[i];
            tr.innerHTML = "";
            tr.onclick = function() {
                window.location.href = "/product/" + item.item_id;
            }
            img.src = item.path;
            td1.appendChild(img);
            th.innerHTML = item.title;
            td2.innerHTML = item.price;
            
            tr.appendChild(td1);
            tr.appendChild(th);
            tr.appendChild(td2);
            
            table.appendChild(tr);
        }
        container.appendChild(table);
      }
    xhttp.open("GET", "/search/" + event.target.value, true);
    xhttp.send();
});

document.addEventListener("DOMContentLoaded", function() {
    const toggle = document.getElementById("toggle");
    const root = document.documentElement;
    
    
    function applyColorScheme() {
        const isDarkMode = toggle.checked;
        const header_icons = document.getElementsByClassName("header_icon");

        if (isDarkMode) {
            root.classList.add("dark-theme");
            for (let i = 0; i < header_icons.length; i++) {
                header_icons[i].style.filter = "invert(1)";
              }

        } else {
            root.classList.remove("dark-theme");
            for (let i = 0; i < header_icons.length; i++) {
                header_icons[i].style.filter = "invert(0)";
              }
        }

        localStorage.setItem("colorScheme", isDarkMode ? "dark" : "light");
    }

    toggle.addEventListener("change", applyColorScheme);

    applyColorScheme();
});