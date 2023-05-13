const loginForm = document.getElementById('login-form');
const loginButton = document.getElementById('login-button');
const loginError = document.getElementById('login-error');

loginForm.addEventListener('submit', function(event) {
    if (!loginButton.disabled) {
        loginButton.disabled = true;
        loginError.style.display = 'none';
    } else {
        event.preventDefault();
    }
});

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