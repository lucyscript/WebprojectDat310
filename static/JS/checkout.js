function handleSubmit(event) {
    event.preventDefault();

    let button = document.getElementById('purchaseBtn');
    let successMsg = document.getElementById('successMsg');

    button.disabled = true;
    successMsg.style.display = '';

    setTimeout(function() {
      event.target.submit();
    }, 2000);
  }