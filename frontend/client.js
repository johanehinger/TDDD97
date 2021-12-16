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

function signUp() {
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
  userData = {
    email: document.getElementById("username-sign-up").value,
    password: password,
    firstname: document.getElementById("first-name").value,
    familyname: document.getElementById("last-name").value,
    gender: document.getElementById("gender-select").value,
    city: document.getElementById("city").value,
    country: document.getElementById("country").value,
  };
  console.log(userData);
  response = serverstub.signUp(userData);
  if (!response.success) {
    document.getElementById("sign-up-error").innerHTML = response.message;
    return false;
  }
  return response.success;
}
