 $(document).ready(function () {

  // Activate MaterializeCSS sidenav
  $('.sidenav').sidenav();

  // MaterializeCSS Character counter
  $('input#input_text, textarea#textarea1').characterCounter();

});

// Visibility button - https://www.youtube.com/watch?v=INhtMA54iMM
const visibilityBtn = document.getElementById("visibilityBtn");
visibilityBtn.addEventListener("click", toggleVisibility)

function toggleVisibility() {
  const passwordInput = document.getElementById("password")
  if (passwordInput.type === "password") {
    passwordInput.type = "text"
    visibilityBtn.classList.remove("fa-lock")
    visibilityBtn.classList.add("fa-lock-open")
  } else {
    passwordInput.type = "password"
    visibilityBtn.classList.remove("fa-lock-open")
    visibilityBtn.classList.add("fa-lock")
  }
}