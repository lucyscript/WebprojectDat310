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

$(document).ready(function() {
    $('#cart-form').submit(function(event) {
        event.preventDefault();

        let formdata = $(this).serialize();
        $('#loading img').attr('src', 'https://sales.ufaber.com/public/static/img/loader-orange.gif');
        $('#loading img').show();

        $.ajax({
            url: '/cart',
            method: 'POST',
            data: formdata,
            success: function(response) {
                $('#response-message').text(response.message);
                setTimeout(function() {
                    $('#response-message').text('');
                }, 3000);
            },
            complete: function() {
                $('#loading img').hide();
                $('#loading img').attr('src', '');
            }
        });
    });
});

function delete_product() {
    const confirmed = confirm('Are you sure you want to delete this product? This action cannot be undone.');
    if (confirmed) {
        $.ajax({
            url: window.location.href,
            method: 'DELETE',
            success: function() {
                const container = document.getElementById('product_page');
                container.innerHTML = "";
                container.style.textAlign = "center";
                container.style.paddingTop = "50px";

                const messageElement = document.createElement('div');
                messageElement.style.color = "green";
                messageElement.style.fontSize = "20px";
                messageElement.textContent = "Product deleted successfully!";
                
                container.appendChild(messageElement);
                
                setTimeout(() => {
                    container.removeChild(messageElement);
                    window.location.href = '/';
                }, 3800);
            }
        });
    }
    else {
        return;
    }
}