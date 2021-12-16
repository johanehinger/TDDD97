displayview = function () {
  document.getElementById("view").innerHTML =
    document.getElementById("welcome-view").innerHTML;
};

window.onload = function () {
  displayview();
};
