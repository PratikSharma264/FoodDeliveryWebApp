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

function showError(messageobj, condition) {
  const key = Object.keys(messageobj);
  const cardContainer = document.getElementById("card-container");
  const cardDiv = document.createElement("div");
  const cardSubDiv = document.createElement("div");
  const i = document.createElement("i");

  if (condition === "error") {
    i.classList.add("fa-solid", "fa-triangle-exclamation");
  } else {
    i.classList.add("fa-solid", "fa-check");
  }

  cardDiv.appendChild(i);
  const textNode = document.createTextNode(messageobj[key]);
  cardSubDiv.appendChild(textNode);
  cardDiv.appendChild(cardSubDiv);
  cardDiv.classList.add("card");

  if (condition === "error") {
    cardDiv.classList.add("error");
  } else {
    cardDiv.classList.add("success");
  }

  cardContainer.prepend(cardDiv);

  setTimeout(() => {
    cardDiv.classList.add("fade-out");
    setTimeout(() => {
      cardContainer.removeChild(cardDiv);
    }, 500);
  }, 5000);
}