let username = document.getElementById('username');
let password = document.getElementById('pw');
let confirm_password = document.getElementById('confirm_pw');

let username_error = document.getElementById('username-error');
let password_error = document.getElementById('password-error');
let confirm_password_error = document.getElementById('confirm-password-error');

username.addEventListener('input', function() {
    if (username.value.length < 4) {
        username_error.innerHTML = "Username must be at least 4 characters long";
    } else {
        username_error.innerHTML = "";
    }
});

password.addEventListener('input', function() {
    if (password.value.length < 5) {
        password_error.innerHTML = "Password must be at least 5 characters long";
    } else {
        password_error.innerHTML = "";
    }
});

confirm_password.addEventListener('input', function() {
    if (confirm_password.value !== password.value) {
        confirm_password_error.innerHTML = "Passwords do not match";
    } else {
        confirm_password_error.innerHTML = "";
    }
});

username.addEventListener('input', updateLoginButton);
password.addEventListener('input', updateLoginButton);
confirm_password.addEventListener('input', updateLoginButton);

function updateLoginButton() {
    const login_button = document.getElementById('btn');
    if (username.value.length < 4 || password.value.length < 5 || password.value !== confirm_password.value) {
        login_button.disabled = true;
    } else {
        login_button.disabled = false;
    }
}