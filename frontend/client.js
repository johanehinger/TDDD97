displayview = function () {
  document.getElementById("view").innerHTML =
    document.getElementById("welcome-view").innerHTML;
};

window.onload = function () {
  displayview();
};

function loginValidation() {
  password = document.getElementById("password").value;
  if (password.length < 5) {
    document.getElementById("login-error").innerHTML =
      "Password must be longer than 5 characters!";
    return false;
  }
  return true;
}

function signUpValidation() {
  password = document.getElementById("password-sign-up").value;
  repeat_password = document.getElementById("repeat-password-sign-up").value;
  if (password.length < 5 || repeat_password.length < 5) {
    document.getElementById("sign-up-error").innerHTML =
      "Password must be longer than 5 characters!";
    return false;
  }
  if (password != repeat_password) {
    document.getElementById("sign-up-error").innerHTML =
      "Passwords must match!";
    return false;
  }
  return true;
}
