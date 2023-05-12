
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

function add_image_preview(upload) {
    // TODO: Save the images, as everytime a file is uploaded it deletes the previous upload from the form

    const images = upload.target.files;
    const upload_box = document.getElementById("image_preview");
    const upload_container = document.getElementById("image_preview_container");
    upload_box.style.display = "block";

    console.log(images)

    for (let i = 0; i < images.length; i++) {
        const image = images[i];
        const reader = new FileReader();

        reader.readAsDataURL(image);
        reader.onload = function (e) {
            const container = document.createElement("div");
            container.classList.add("image_preview_image_container");

            const img = document.createElement("img");
            img.classList.add("image_preview_image");

            img.src = e.target.result;

            const removeButton = document.createElement("button");
            removeButton.classList.add("remove");
            removeButton.setAttribute("type", "button");
            removeButton.setAttribute("aria-label", "Remove");
            removeButton.innerHTML = "<span aria-hidden='true'>&times;</span>";
            removeButton.addEventListener("click", function () { 
                remove_image_preview(this);
            });
            
            container.appendChild(img);
            container.appendChild(removeButton);
            upload_container.appendChild(container);
        }
    }
}

function remove_image_preview(image) {
    image.parentNode.remove();
}