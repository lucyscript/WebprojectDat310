const loginForm = document.getElementById('login-form');
const loginButton = document.getElementById('login-button');
const loginError = document.getElementById('login-error');

loginForm.addEventListener('input', function(event) {
    const username = loginForm.elements.username.value;
    const password = loginForm.elements.password.value;
    if (username.trim() === '' || password.trim() === '') {
        loginButton.disabled = true;
        loginError.innerHTML = 'Please fill in all fields';
        loginError.style.display = 'block';
    } else {
        loginButton.disabled = false;
        loginError.style.display = 'none';
    }
});

$(document).ready(function() {
    $('#login-form').submit(function(event) {
        event.preventDefault();
        let username = $('#username').val();
        let password = $('#password').val();
        $.ajax({
            type: 'POST',
            url: '/login',
            data: {username: username, password: password},
            success: function(response) {
                if (response.success) {
                    window.location.href = '/';
                } else {
                    $('#invalid-form').text('Invalid login credentials');
                }
            }
        });
    });
});