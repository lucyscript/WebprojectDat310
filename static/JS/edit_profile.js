document.addEventListener('DOMContentLoaded', function() {
    const editButton = document.getElementById('edit-button');
    const bioElement = document.getElementById('bio');
    const addressElement = document.getElementById('address');
    const phoneElement = document.getElementById('phone');

    editButton.addEventListener('click', function() {
        bioElement.querySelector('p').hidden = true;
        bioElement.querySelector('input').hidden = false;
        addressElement.querySelector('p').hidden = true;
        addressElement.querySelector('input').hidden = false;
        phoneElement.querySelector('p').hidden = true;
        phoneElement.querySelector('input').hidden = false;

        editButton.innerHTML = 'Submit';
        editButton.classList.add('submit-button');
        editButton.removeEventListener('click', editButtonClickHandler);
        editButton.addEventListener('click', submitButtonClickHandler);
    });

    function submitButtonClickHandler() {
        const path = window.location.pathname;

        const bioValue = bioElement.querySelector('input').value;
        const addressValue = addressElement.querySelector('input').value;
        const phoneValue = phoneElement.querySelector('input').value;

        fetch(`${path}`, {
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
            if (!response.ok) {
                throw new Error('Failed to update profile content.');
            }
        })
        .catch(error => {
            console.error(error);
        });

        bioElement.querySelector('p').textContent = bioValue;
        bioElement.querySelector('p').hidden = false;
        bioElement.querySelector('input').hidden = true;
        addressElement.querySelector('p').textContent = addressValue;
        addressElement.querySelector('p').hidden = false;
        addressElement.querySelector('input').hidden = true;
        phoneElement.querySelector('p').textContent = phoneValue;
        phoneElement.querySelector('p').hidden = false;
        phoneElement.querySelector('input').hidden = true;

        editButton.innerHTML = 'Edit profile';
        editButton.classList.remove('submit-button');
        editButton.removeEventListener('click', submitButtonClickHandler);
        editButton.addEventListener('click', editButtonClickHandler);
    }

    function editButtonClickHandler() {
        bioElement.querySelector('p').hidden = true;
        bioElement.querySelector('input').hidden = false;
        addressElement.querySelector('p').hidden = true;
        addressElement.querySelector('input').hidden = false;
        phoneElement.querySelector('p').hidden = true;
        phoneElement.querySelector('input').hidden = false;

        editButton.innerHTML = 'Submit';
        editButton.classList.add('submit-button');
        editButton.removeEventListener('click', editButtonClickHandler);
        editButton.addEventListener('click', submitButtonClickHandler);
    }
});
