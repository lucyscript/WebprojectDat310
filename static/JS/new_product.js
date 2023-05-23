
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
            
            container.appendChild(img);
            container.appendChild(removeButton);
            upload_container.appendChild(container);

            console.log("Uploaded image:", image);
            console.log("All uploaded images:", uploadedImages);
            console.log("input form values:", image_upload.value);
            loadedImages++;
            if (loadedImages === images.length) {
            //    onload_complete();
                image_upload.value = "";
            }
        } // Reader end
    } // For end
} // Function end


const form = document.getElementById("new_product_form");
form.addEventListener("submit", function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const textInputs = form.querySelectorAll("input[type=text]");

    for (let i = 0; i < textInputs.length; i++) {
        const input = textInputs[i];
        formData.append(input.name, input.value);
    }
    for (let i = 0; i < uploadedImages.length; i++) {
        const image = uploadedImages[i];
        formData.append("imageValues[]", image);
    }

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/handle_upload");
    xhr.onload = function() {
        if (xhr.status === 200) {
            window.location.href = xhr.responseURL;
        }
    };
    xhr.send(formData);
    uploadedImages = [];
});


function remove_image_preview(image) {
    image.parentNode.remove();
    const index = uploadedImages.indexOf(image.src);
    uploadedImages.splice(index, 1);
}
function log() {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/test");
    xhr.send();
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

