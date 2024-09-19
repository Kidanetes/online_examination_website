const signUp = document.querySelector('.signup');
const formSection = document.querySelector('.form-section');

function handleSignupClick(event) {
  event.preventDefault(); // Prevents the form from submitting

  // Add signup mode class to form section
  formSection.classList.add('signup-mode');

  const form = document.querySelector('.form');

  // Clear the current form content
  while (form.firstChild) {
    form.removeChild(form.firstChild);
  }

  // Create new input fields for signup
  var placeholders = ['First name', 'Last name', 'Email', 'Password', 'Confirm Password'];
  placeholders.forEach(function(placeholder) {
    var input = document.createElement('input');
    input.classList.add('input');
    input.setAttribute('type', placeholder.toLowerCase().includes('password') ? 'password' : 'text');
    input.setAttribute('placeholder', placeholder);
    form.appendChild(input);
    form.appendChild(document.createElement('br'));
  });

  // Create a container div for buttons
  var buttonContainer = document.createElement('div');
  buttonContainer.classList.add('button-container');

  // Add a Submit button for signup
  var submitButton = document.createElement('input');
  submitButton.setAttribute('type', 'submit');
  submitButton.setAttribute('value', 'Submit');
  submitButton.classList.add('button', 'signup-submit');
  buttonContainer.appendChild(submitButton);

  // Add a Login button to return to the login page
  var loginButton = document.createElement('input');
  loginButton.setAttribute('type', 'button');
  loginButton.setAttribute('value', 'Back to Login');
  loginButton.classList.add('button', 'login-back');
  buttonContainer.appendChild(loginButton);

  // Append the button container to the form
  form.appendChild(buttonContainer);

  // Add event listener to Login button
  loginButton.addEventListener('click', handleLoginClick);
}

function handleLoginClick() {
  formSection.classList.remove('signup-mode');

  const form = document.querySelector('.form');

  // Clear form and revert to original login fields
  while (form.firstChild) {
    form.removeChild(form.firstChild);
  }

  // Recreate the original login form fields
  var emailInput = document.createElement('input');
  emailInput.classList.add('input');
  emailInput.setAttribute('type', 'text');
  emailInput.setAttribute('placeholder', 'Email');
  form.appendChild(emailInput);
  form.appendChild(document.createElement('br'));

  var passwordInput = document.createElement('input');
  passwordInput.classList.add('input');
  passwordInput.setAttribute('type', 'password');
  passwordInput.setAttribute('placeholder', 'Password');
  form.appendChild(passwordInput);
  form.appendChild(document.createElement('br'));

  // Recreate the "Forgot your password?" link
  var forgotPassword = document.createElement('p');
  var forgotLink = document.createElement('a');
  forgotLink.setAttribute('href', '#');
  forgotLink.textContent = 'Forgot your password?';
  forgotPassword.appendChild(forgotLink);
  form.appendChild(forgotPassword);

  // Recreate login and signup buttons
  var loginBtn = document.createElement('input');
  loginBtn.setAttribute('type', 'submit');
  loginBtn.setAttribute('value', 'Login');
  loginBtn.classList.add('button', 'login');
  form.appendChild(loginBtn);

  var signupBtn = document.createElement('input');
  signupBtn.setAttribute('type', 'submit');
  signupBtn.setAttribute('value', 'Signup');
  signupBtn.classList.add('button', 'signup');
  form.appendChild(signupBtn);

  // Reattach the event listener to the newly created signup button
  signupBtn.addEventListener('click', handleSignupClick);
}

// Attach the initial event listener to the signup button
signUp.addEventListener('click', handleSignupClick);
