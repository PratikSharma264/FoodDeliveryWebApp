const successCard = document.getElementById("success-card");
if (successCard) {
  setTimeout(() => {
    successCard.style.opacity = "0";
    successCard.style.transform = "translateY(-20px)";
    setTimeout(() => {
      successCard.remove();
    }, 500);
  }, 3000);
}

document.addEventListener("DOMContentLoaded", (e) => {
  const logoutbtn = document.getElementById("logout");
  const nobtn = document.getElementById("no-btn");
  const revalidatecontainer = document.getElementById("revalidate-logout");

  if (logoutbtn && revalidatecontainer && nobtn) {
    logoutbtn.addEventListener("click", (e) => {
      revalidatecontainer.classList.remove("hidden");
      document.body.style.overflow = "hidden";
    });

    nobtn.addEventListener("click", (e) => {
      revalidatecontainer.classList.add("hidden");
      document.body.style.overflow = "auto";
    });
  }
});
