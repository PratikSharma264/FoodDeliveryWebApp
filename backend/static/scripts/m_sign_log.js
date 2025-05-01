const signUpButton = document.getElementById("signUp");
const logInButton = document.getElementById("logIn");
const container = document.getElementById("container");

signUpButton.addEventListener("click", () => {
  container.classList.add("right-panel-active");
  document.body.classList.add("bg-shift-right");
});

logInButton.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
  document.body.classList.remove("bg-shift-right");
});

// header

const dropBtn = document.getElementById("drop-btn");
const menu = document.querySelector(".header-link");
const bar = document.querySelector("#bar");
const xmark = document.querySelector("#xmark");
const div = 0;

dropBtn.addEventListener("click", () => {
  menu.classList.toggle("active");
  const isMenuOpen = menu.classList.contains("active");

  if (isMenuOpen) {
    bar.style.display = "none";
    xmark.style.display = "block";
  } else {
    bar.style.display = "block";
    xmark.style.display = "none";
  }
});
