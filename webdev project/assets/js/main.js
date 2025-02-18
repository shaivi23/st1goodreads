// main.js

// Show hidden password functionality
const showHiddenPassword = (inputPassword, inputIcon) => {
  const input = document.getElementById(inputPassword),
        iconEye = document.getElementById(inputIcon)

  iconEye.addEventListener('click', () => {
    // Change password to text
    if (input.type === 'password') {
      input.type = 'text';
      iconEye.classList.add('ri-eye-line');
      iconEye.classList.remove('ri-eye-off-line');
    } else {
      input.type = 'password';
      iconEye.classList.remove('ri-eye-line');
      iconEye.classList.add('ri-eye-off-line');
    }
  })
}

showHiddenPassword('password', 'input-icon')

// Redirect to app.html when login button is clicked
document.getElementById('loginForm').addEventListener('submit', function (e) {
  e.preventDefault(); // Prevent form submission
  window.location.href = 'app.html'; // Redirect to app.html
});
