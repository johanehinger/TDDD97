displayview = function () {
  token = sessionStorage.getItem("token");

  if (token) {
    document.getElementById("view").innerHTML =
      document.getElementById("profile-view").innerHTML;
    getUserInfo();
    getPosts();
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

function changePassword() {
  old_password = document.getElementById("old-password").value;
  new_password = document.getElementById("new-password").value;
  repeat_new_password = document.getElementById("repeat-new-password").value;

  if (new_password != repeat_new_password) {
    document.getElementById("change-password-error").innerHTML =
      "Passwords must match!";
    return false;
  }
  if (new_password.length < 5 || repeat_new_password.length < 5) {
    document.getElementById("change-password-error").innerHTML =
      "Password must be longer than 5 characters!";
    return false;
  }
  token = sessionStorage.getItem("token");

  response = serverstub.changePassword(token, old_password, new_password);

  document.getElementById("change-password-error").innerHTML = response.message;
  return false;
}

function signOut() {
  token = sessionStorage.getItem("token");
  response = serverstub.signOut(token);
  if (response.success) {
    sessionStorage.clear();
    displayview();
  }
}

function getUserInfo() {
  token = sessionStorage.getItem("token");

  response = serverstub.getUserDataByToken(token);
  document.getElementById("user-email").innerHTML =
    "Email: " + response.data.email;
  document.getElementById("first-name").innerHTML =
    "First name: " + response.data.firstname;
  document.getElementById("last-name").innerHTML =
    "Last name: " + response.data.familyname;
  document.getElementById("gender").innerHTML =
    "Gender: " + response.data.gender;
  document.getElementById("user-city").innerHTML =
    "City: " + response.data.city;
  document.getElementById("user-country").innerHTML =
    "Country: " + response.data.country;
}

function post() {
  token = sessionStorage.getItem("token");
  response = serverstub.getUserDataByToken(token);
  content = document.getElementById("new-post-text").value;
  to_email = response.data.email;
  response = serverstub.postMessage(token, content, to_email);
  getPosts();
  document.getElementById("new-post-text").value = "";
}

function getPosts() {
  document.getElementById("post-list").innerHTML = "";
  token = sessionStorage.getItem("token");

  response = serverstub.getUserMessagesByToken(token);
  posts = response.data;
  list_container = document.createElement("div");
  list_element = document.createElement("ul");
  document.getElementsByClassName("post-list")[0].appendChild(list_container);
  list_container.appendChild(list_element);

  for (i = 0; i < posts.length; ++i) {
    list_item = document.createElement("li");
    list_item.innerHTML = posts[i].content + " - " + posts[i].writer;

    list_element.appendChild(list_item);
  }
}

function getOtherUserPosts() {
  document.getElementById("search-post-list").innerHTML = "";

  token = sessionStorage.getItem("token");
  email = document.getElementById("search-username").value;
  response = serverstub.getUserMessagesByEmail(token, email);
  console.log(response);
  posts = response.data;

  list_container = document.createElement("div");
  list_element = document.createElement("ul");
  document
    .getElementsByClassName("search-post-list")[0]
    .appendChild(list_container);
  list_container.appendChild(list_element);

  for (i = 0; i < posts.length; ++i) {
    list_item = document.createElement("li");
    list_item.innerHTML = posts[i].content + " - " + posts[i].writer;

    list_element.appendChild(list_item);
  }
}

function postOnOtherUser() {
  token = sessionStorage.getItem("token");
  content = document.getElementById("search-new-post-text").value;
  to_email = document.getElementById("search-username").value;
  if (!to_email || !content) {
    return;
  }
  response = serverstub.postMessage(token, content, to_email);
  console.log(response);
  getOtherUserPosts();
  document.getElementById("search-new-post-text").value = "";
}

function getOtherUserInfo() {
  email = document.getElementById("search-username").value;
  token = sessionStorage.getItem("token");

  if (!email) {
    return;
  }
  response = serverstub.getUserDataByEmail(token, email);
  console.log(response);
  if (!response.success) {
    document.getElementById("search-error").innerHTML = response.message;
    return;
  }
  document.getElementById("search-error").innerHTML = "";
  document.getElementById("search-user-email").innerHTML =
    "Email: " + response.data.email;
  document.getElementById("search-first-name").innerHTML =
    "First name: " + response.data.firstname;
  document.getElementById("search-last-name").innerHTML =
    "Last name: " + response.data.familyname;
  document.getElementById("search-gender").innerHTML =
    "Gender: " + response.data.gender;
  document.getElementById("search-user-city").innerHTML =
    "City: " + response.data.city;
  document.getElementById("search-user-country").innerHTML =
    "Country: " + response.data.country;
  getOtherUserPosts();
  console.log(email);
}
