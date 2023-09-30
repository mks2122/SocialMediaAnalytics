// Add validation to the login form
const loginForm = document.querySelector('#login-signup form');
loginForm.addEventListener('submit', function(event) {
  event.preventDefault();

  // Validate the email and password fields
  const emailField = document.querySelector('#login-signup form input[name="email"]');
  const passwordField = document.querySelector('#login-signup form input[name="password"]');

  if (!emailField.value) {
    alert('Please enter your email address.');
    return;
  }

  if (!passwordField.value) {
    alert('Please enter your password.');
    return;
  }

  // Submit the form if validation is successful
  this.submit();
});
