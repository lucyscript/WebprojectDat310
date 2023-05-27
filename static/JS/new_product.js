
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
            leftArrow.setAttribute("aria-label", "Move left");
            leftArrow.innerHTML = "<span aria-hidden='true'>&#10094;</span>";

            const rightArrow = document.createElement("button");
            rightArrow.classList.add("arrow");
            rightArrow.classList.add("right");
            rightArrow.setAttribute("type", "button");
            rightArrow.setAttribute("aria-label", "Move right");
            rightArrow.innerHTML = "<span aria-hidden='true'>&#10095;</span>";

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

$('.arrow').on('click', function() {
    var container = document.getElementById("image_preview_container");
    var direction = $(this).hasClass('right') ? -1 : 1;
    var siblings = container.siblings('.image_preview_image_container');
    var index = container.index();
    var newIndex = index + direction;
  
    if (newIndex >= 0 && newIndex < siblings.length + 1) {
      if (direction === -1) {
        container.insertBefore(siblings.eq(newIndex));
      } else {
        container.insertAfter(siblings.eq(newIndex - 1));
      }
    }
  });

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

