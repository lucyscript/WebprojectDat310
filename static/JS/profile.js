document.addEventListener('DOMContentLoaded', function() {
    const editButton = document.getElementById('edit-button');
    const bioElement = document.getElementById('bio');
    const addressElement = document.getElementById('address');
    const phoneElement = document.getElementById('phone');

    editButton.addEventListener('click', function() {
        bioElement.querySelector('p').hidden = true;
        bioElement.querySelector('span').hidden = false;
        addressElement.querySelector('p').hidden = true;
        addressElement.querySelector('span').hidden = false;
        phoneElement.querySelector('p').hidden = true;
        phoneElement.querySelector('span').hidden = false;

        editButton.innerHTML = 'Submit';
        editButton.classList.add('submit-button');
        editButton.removeEventListener('click', editButtonClickHandler);
        editButton.addEventListener('click', submitButtonClickHandler);
    });

    function submitButtonClickHandler() {
        const bioValue = bioElement.querySelector('span').textContent;
        const addressValue = addressElement.querySelector('span').textContent;
        const phoneValue = phoneElement.querySelector('span').textContent;
        const responseDiv = document.getElementById('edit-response');

        fetch(window.location.pathname, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                bio: bioValue,
                address: addressValue,
                phone: phoneValue
            })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to update profile content.');
            }
        })
        .then(data => {
            responseDiv.hidden = false;
            responseDiv.textContent = data.message;
        })
        .finally(() => {
            setTimeout(() => {
                responseDiv.hidden = true;
                responseDiv.textContent = '';
            }, 3000);
        });

        bioElement.querySelector('p').textContent = bioValue;
        bioElement.querySelector('p').hidden = false;
        bioElement.querySelector('span').hidden = true;
        addressElement.querySelector('p').textContent = addressValue;
        addressElement.querySelector('p').hidden = false;
        addressElement.querySelector('span').hidden = true;
        phoneElement.querySelector('p').textContent = phoneValue;
        phoneElement.querySelector('p').hidden = false;
        phoneElement.querySelector('span').hidden = true;

        editButton.innerHTML = 'Edit profile';
        editButton.classList.remove('submit-button');
        editButton.removeEventListener('click', submitButtonClickHandler);
        editButton.addEventListener('click', editButtonClickHandler);
    }

    function editButtonClickHandler() {
        bioElement.querySelector('p').hidden = true;
        bioElement.querySelector('span').hidden = false;
        addressElement.querySelector('p').hidden = true;
        addressElement.querySelector('span').hidden = false;
        phoneElement.querySelector('p').hidden = true;
        phoneElement.querySelector('span').hidden = false;

        editButton.innerHTML = 'Submit';
        editButton.classList.add('submit-button');
        editButton.removeEventListener('click', editButtonClickHandler);
        editButton.addEventListener('click', submitButtonClickHandler);
    }
});

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
    fetch(window.location.pathname, {
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


// SPAN was stupid and copied its own element ??? Easy fiks
document.addEventListener('DOMContentLoaded', function() {
    const bioInput = document.getElementById("bio-input");
    bioInput.addEventListener("copy", function(event) {
      const copiedText = bioInput.textContent;
      event.clipboardData.setData("text/plain", copiedText);
      event.preventDefault();
    });
    const addressInput = document.getElementById("address-input");
    addressInput.addEventListener("copy", function(event) {
        const copiedText = addressInput.textContent;
        event.clipboardData.setData("text/plain", copiedText);
        event.preventDefault();
        }
    );
    const phoneInput = document.getElementById("phone-input");
    phoneInput.addEventListener("copy", function(event) {
        const copiedText = phoneInput.textContent;
        event.clipboardData.setData("text/plain", copiedText);
        event.preventDefault();
        }
    );
});