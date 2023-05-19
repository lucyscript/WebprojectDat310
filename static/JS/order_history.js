$(document).ready(function() {
  $('#search-input').on('keydown', function(event) {
    if (event.keyCode === 13) {
      event.preventDefault(); 
    }
  });

  $('#search-input').on('keyup', function() {
    let user_id = getUserId();
    let query = $(this).val();
    searchOrders(user_id, query);
  });

  function getUserId() {
    let url = window.location.href;
    let user_id = url.substring(url.lastIndexOf('/') + 1);
    return user_id;
  }

  function searchOrders(user_id, query) {
    $('.order-search input[type="text"]').css('background-image', 'url("https://sales.ufaber.com/public/static/img/loader-orange.gif")');
    $.ajax({
      url: `/search_orders/${user_id}`,
      method: 'GET',
      data: { query: query },
      success: function(response) {
        let orders = response; 
        let tableBody = '';

        orders.forEach(function(order) {
          tableBody += '<tr>';
          tableBody += '<td>' + order['order_id'] + '</td>';
          tableBody += '<td>' + order['order_date'] + '</td>';
          tableBody += '<td>' + order['product_id'] + '</td>';
          tableBody += '<td>' + order['quantity'] + '</td>';
          tableBody += '<td>$' + order['total_amount'] + '</td>';
          tableBody += '<td>' + order['title'] + '</td>';
          tableBody += '<td><img src="' + order['path'] + '" alt="Product Image" width="100"></td>';
          tableBody += '</tr>';
        });

        $('tbody').html(tableBody);
      },
      error: function(error) {
        console.log('Error:', error);
      },
      complete: function() {
        $('.order-search input[type="text"]').css('background-image', 'none');
      }
    });
  }
});
