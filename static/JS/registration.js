let username = document.getElementById('username');
let password = document.getElementById('pw');
let confirm_password = document.getElementById('confirm_pw');

let username_error = document.getElementById('username-error');
let password_error = document.getElementById('password-error');
let confirm_password_error = document.getElementById('confirm-password-error');

let usernameTaken = false;

username.addEventListener('input', function() {
    if (username.value.length < 4) {
        username_error.innerHTML = "Username must be at least 4 characters long";
    } else {
        username_error.innerHTML = "";
    }
    updateRegisterBtn();
});

password.addEventListener('input', function() {
    if (password.value.length < 5) {
        password_error.innerHTML = "Password must be at least 5 characters long";
    } else {
        password_error.innerHTML = "";
    }
    updateRegisterBtn();
});

confirm_password.addEventListener('input', function() {
    if (confirm_password.value !== password.value) {
        confirm_password_error.innerHTML = "Passwords do not match";
    } else {
        confirm_password_error.innerHTML = "";
    }
    updateRegisterBtn();
});

$(document).ready(function() {
    $('#username').on('keyup', function() {
        let new_username = $(this).val();
        if (new_username.length > 3) {
            $('#username').css('background-image', 'url("https://sales.ufaber.com/public/static/img/loader-orange.gif")');
        }
        $.ajax({
            url: '/check_username',
            method: 'GET',
            data: {username: new_username},
            success: function(response) {
                if (response.success) {
                    usernameTaken = false;
                    if (new_username.length > 3) {
                        $('#username-taken').text('');
                        $('#username-available').text('Username is available');
                    } else {
                        $('#username-taken').text('');
                        $('#username-available').text('');
                    }
                } else {
                    usernameTaken = true;
                    if (new_username.length > 3) {
                        $('#username-available').text('');
                        $('#username-taken').text('Username is already taken.');
                    } else {
                        $('#username-taken').text('');
                        $('#username-available').text('');
                    }
                }
                updateRegisterBtn(); 
            },
            complete: function() {
                $('#username').css('background-image', 'url("")');
            }
        });
    });
});


function updateRegisterBtn() {
    const register_btn = document.getElementById('btn');
    if (username.value.length < 4 || password.value.length < 5 || password.value !== confirm_password.value || usernameTaken) {
        register_btn.disabled = true;
    } else {
        register_btn.disabled = false;
    }
}