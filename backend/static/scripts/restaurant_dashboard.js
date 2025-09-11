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

