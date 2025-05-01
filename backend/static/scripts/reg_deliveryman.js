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
