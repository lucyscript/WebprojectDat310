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
        $('#loading img').attr('src', 'https://gregoryuniversityuturu.edu.ng/portal/assets/scholars/images/ajax-loader.gif');
        $('#loading img').show();
        $.ajax({
            method: 'POST',
            url: '/login',
            data: {username: username, password: password},
            success: function(response) {
                if (response.success) {
                    window.location.href = '/';
                } else {
                    $('#invalid-form').text('Invalid login credentials');
                }
            },
            complete: function() {
                $('#loading img').hide();
                $('#loading img').attr('src', '');
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const root = document.documentElement;

    const savedColorScheme = localStorage.getItem("colorScheme");
    if (savedColorScheme === "dark") {
        root.classList.add("dark-theme");
    } else {
        root.classList.remove("dark-theme");
    }
});