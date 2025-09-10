document.addEventListener("DOMContentLoaded", (e) => {
  const summaryCard = document.getElementById("summary2-div");

  summaryCard.addEventListener("mousemove", function (e) {
    const rect = summaryCard.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = ((centerY - y) / centerY) * 20;
    const rotateY = ((x - centerX) / centerX) * 20;
    summaryCard.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
  });
  summaryCard.addEventListener("mouseleave", function () {
    summaryCard.style.transform = "rotateX(0deg) rotateY(0deg)";
  });
});

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
