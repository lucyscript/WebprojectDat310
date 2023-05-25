
function side_menu_open() {
    document.getElementById("side_menu").style.display = "block";
    document.getElementById("side_menu").style.width = "45%";
}

function side_menu_close() {
    document.getElementById("side_menu").style.display = "none";
    document.getElementById("side_menu").style.width = "0";
}


function image_slide_change(n, image_index) {
    var i;
    var images = document.getElementsByClassName("image-slide");
    var shown_number = document.getElementById("image-number");
    image_index += n;

    if (image_index > images.length) { image_index = 1 }
    if (image_index < 1) { image_index = images.length }

    for (i = 0; i < images.length; i++) {
        images[i].style.display = "none";
    }

    images[image_index - 1].style.display = "block";
    shown_number.innerHTML = image_index + "/" + images.length;
    document.getElementById("back-button").onclick = function () { image_slide_change(-1, image_index) };
    document.getElementById("forward-button").onclick = function () { image_slide_change(1, image_index) };
}



// SEARCH RECOMEND
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
            td2.innerHTML = `$${item.price}`;
            
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