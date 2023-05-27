$(document).ready(function() {
    $('.del').click(function() {
        let itemID = $(this).data('item-id');
        removeCartItem(itemID);
    });
});

function removeCartItem(itemID) {
    $.ajax({
        url: '/cart/' + itemID,
        type: 'DELETE',
        success: function(response) {
            console.log(response.message);
            $('#row-' + itemID).remove();
        }
    });
}
