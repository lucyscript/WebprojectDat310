
let uploadedImages = [];

function add_image_preview(upload) {
    // TODO: Save the images, as everytime a file is uploaded it deletes the previous upload from the form
    
    const images = upload.target.files;
    const upload_container = document.getElementById("image_preview_container");
    const upload_box = document.getElementById("image_preview");
    upload_box.style.display = "block";

    const image_upload = document.getElementById("image_upload");

    let loadedImages = 0;
    for (let i = 0; i < images.length; i++) {
        const image = images[i];
        const reader = new FileReader();

        reader.readAsDataURL(image);
        reader.onload = function (e) { // THIS IS asynchronous so it will not run in order 🤬🤬🤬
            const dataURL = e.target.result;
            const filename = image.name;
            const file = dataURLtoFile(dataURL, filename);
            uploadedImages.push(file);

            const container = document.createElement("div");
            container.classList.add("image_preview_image_container");
            
            const img = document.createElement("img");
            img.classList.add("image_preview_image");
            
            img.src = dataURL;

            const removeButton = document.createElement("button");
            removeButton.classList.add("remove");
            removeButton.setAttribute("type", "button");
            removeButton.setAttribute("aria-label", "Remove");
            removeButton.innerHTML = "<span aria-hidden='true'>&times;</span>";
            removeButton.addEventListener("click", function () { 
                remove_image_preview(this);
            });

            const arrowsDiv = document.createElement("div");
            arrowsDiv.classList.add("arrows");

            const leftArrow = document.createElement("button");
            leftArrow.classList.add("arrow");
            leftArrow.classList.add("left");
            leftArrow.setAttribute("type", "button");
            leftArrow.setAttribute("onclick", "arrowChange(this)");
            leftArrow.innerHTML = "<span>&#10094;</span>";

            const rightArrow = document.createElement("button");
            rightArrow.classList.add("arrow");
            rightArrow.classList.add("right");
            rightArrow.setAttribute("type", "button");
            rightArrow.setAttribute("onclick", "arrowChange(this)");
            rightArrow.innerHTML = "<span>&#10095;</span>";

            arrowsDiv.appendChild(leftArrow);
            arrowsDiv.appendChild(rightArrow);
            
            container.appendChild(img);
            container.appendChild(removeButton);
            container.appendChild(arrowsDiv);
            upload_container.appendChild(container);

            loadedImages++;
            if (loadedImages === images.length) {
            //    onload_complete();
                image_upload.value = "";
            }
        } // Reader end
    } // For end
} // Function end

description_box = document.getElementById("description_input");
description_error = document.getElementById("description_error");
description_box.addEventListener("input", function (event) {
    if (event.target.textContent.length > 500) {
        description_error.style.display = "block";
    }
    else {
        description_error.style.display = "none";
    }
});


function arrowChange(element) {
    var container = document.getElementById("image_preview_container");
    var container_list = Array.from(container.children)

    var image = element.parentNode.parentNode;
    var direction = element.classList.contains('left') ? -1 : 1;
    var index = container_list.indexOf(image);
    var newIndex = index + direction;
  
    if (newIndex >= 0 && newIndex <= container_list.length) {
        var nextImage = container_list[newIndex];
        if (direction === -1) {
            container.insertBefore(image, nextImage);
            image_file = uploadedImages.splice(index, 1)[0];
            uploadedImages.splice(newIndex, 0, image_file);

          } else if (newIndex != container_list.length) {
                container.insertBefore(nextImage, image);
                image_file = uploadedImages.splice(index, 1)[0];
                uploadedImages.splice(newIndex, 0, image_file);
      }
    }
  };

const form = document.getElementById("new_product_form");
form.addEventListener("submit", function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const textInputs = [];
    textInputs.push(document.getElementById("title_input"));
    textInputs.push(document.getElementById("price_input"));

    formData.append("description", document.getElementById("description_input").textContent);

    for (let i = 0; i < textInputs.length; i++) {
        const input = textInputs[i];
        formData.append(input.name, input.value);
    }
    for (let i = 0; i < uploadedImages.length; i++) {
        const image = uploadedImages[i];
        formData.append("imageValues[]", image);
    }

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/new_product");
    xhr.onload = function() {
        if (xhr.status === 200) {
            window.location.href = xhr.responseURL;
        }
    };
    xhr.send(formData);
    uploadedImages = [];
});


function remove_image_preview(button) {
    const image = button.parentNode.firstChild;
    const parent = image.parentNode.parentNode;
    const index = Array.prototype.indexOf.call(parent.childNodes, image.parentNode);
    parent.removeChild(image.parentNode);
    uploadedImages.splice(index-1, 1);
}

function dataURLtoFile(dataurl, filename) {
    const arr = dataurl.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, { type: mime });
}

const title_input = document.getElementById("title_input");
const price_input = document.getElementById("price_input");
const upload_button = document.getElementById("submit_button");

title_input.addEventListener("input", toggleSubmitButton);
price_input.addEventListener("input", toggleSubmitButton);

function toggleSubmitButton() {
    const isTitleEmpty = title_input.value.trim() === "";
    const isPriceEmpty = price_input.value.trim() === "";

    if (isTitleEmpty || isPriceEmpty) {
        upload_button.disabled = true;
        upload_button.classList.remove("enabled")
    }
    else {
        upload_button.disabled = false;
        upload_button.classList.add("enabled")
    }
  }
