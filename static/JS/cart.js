$(document).ready(function() {
    $('.del').click(function() {
        let itemID = $(this).data('item-id');
        removeCartItem(itemID);
    });
});

function removeCartItem(itemID) {
    let totalPrice = document.getElementById('total_price');
    $.ajax({
        url: '/cart/' + itemID,
        method: 'DELETE',
        success: function(response) {
            $('#row-' + itemID).remove();
            totalPrice.textContent = response.total_price;
        }
    });
}