function sortItems(sortBy) {
    $('#product-grid').empty();

    $.ajax({
        url: `/sort/${sortBy}`,
        type: 'GET',
        success: function(response) {
            let items = response.items;

            for (let i = 0; i < items.length; i++) {
                let item = items[i];
                let productBox = createProductBox(item);
                $('#product-grid').append(productBox);
            }
        },
        error: function() {
            console.log('Error occurred while sorting items.');
        }
    });
}

function createProductBox(item) {
    let productBox = document.createElement('div');
    productBox.className = 'product-box';
    productBox.onclick = function() {
        location.href = '/product/' + item[0];
    };

    let image = document.createElement('img');
    image.src = item[2];
    image.alt = item[1];
    productBox.appendChild(image);

    let title = document.createElement('h3');
    title.textContent = item[1];
    productBox.appendChild(title);

    return productBox;
}
