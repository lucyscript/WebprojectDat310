function confirmDelete(user_id) {
    let popup = document.createElement('div');
    popup.className = 'popup';

    let popupContent = document.createElement('div');
    popupContent.className = 'popup-content';

    let message = document.createElement('p');
    message.textContent = 'Are you sure you want to delete your account?';

    let confirmButton = document.createElement('button');
    confirmButton.textContent = 'Yes';
    confirmButton.addEventListener('click', function() {
        document.body.removeChild(popup);
        deleteUser(user_id);   
    });

    let cancelButton = document.createElement('button');
    cancelButton.textContent = 'No';
    cancelButton.addEventListener('click', function() {
        document.body.removeChild(popup);
    });

    popupContent.appendChild(message);
    popupContent.appendChild(confirmButton);
    popupContent.appendChild(cancelButton);
    popup.appendChild(popupContent);
    document.body.appendChild(popup);

    return false;
}
  
function deleteUser() {
    fetch('/profile', {
        method: 'DELETE'
    })
    .then(function(response) {
        if (response.ok) {
            window.location.href = '/logout';
        } else {
            throw new Error('Failed to delete user.');
        }
    });
}