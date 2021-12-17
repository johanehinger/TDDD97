displayview = function () {
  token = sessionStorage.getItem("token");
  console.log(token);

  if (token) {
    document.getElementById("view").innerHTML =
      document.getElementById("profile-view").innerHTML;
    return;
  }
  document.getElementById("view").innerHTML =
    document.getElementById("welcome-view").innerHTML;
};

window.onload = function () {
  displayview();
};

function signIn() {
  password = document.getElementById("password").value;
  email = document.getElementById("username").value;
  if (password.length < 5) {
    document.getElementById("login-error").innerHTML =
      "Password must be longer than 5 characters!";
    return false;
  }
  response = serverstub.signIn(email, password);
  if (!response.success) {
    document.getElementById("login-error").innerHTML = response.message;
    return false;
  }
  sessionStorage.setItem("token", response.data);
  displayview();
  return response.success;
}

function signUp() {
  password = document.getElementById("password-sign-up").value;
  email = document.getElementById("username-sign-up").value;
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
    email: email,
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
  response = serverstub.signIn(email, password);
  if (!response.success) {
    document.getElementById("login-error").innerHTML = response.message;
    return false;
  }
  sessionStorage.setItem("token", response.data);
  displayview();
  return response.success;
}

function navigate(evt, tab) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tab).style.display = "block";
  evt.currentTarget.className += " active";
}
