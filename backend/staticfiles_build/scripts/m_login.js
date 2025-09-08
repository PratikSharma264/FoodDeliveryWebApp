
const loginerrors = [];
const form = document.getElementById("login-form");

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

document.addEventListener("DOMContentLoaded", function () {
  const errorScript = document.getElementById("form-errors");
  if (errorScript) {
    const errors = JSON.parse(errorScript.textContent);
    errors.error.forEach((err, i) => {
      setTimeout(() => {
        showError({ errmsg: err.message }, "error");
      }, i * 1000);
    });
  }

  const successScript = document.getElementById("login-success");
  if (successScript) {
    const successData = JSON.parse(successScript.textContent);
    showError({ success: successData.message }, "success");
    setTimeout(() => {
      window.location.href = "/";
    }, 3000);
  }
});

form.addEventListener("submit", function (e) {
  loginerrors.length = 0;

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  const emailregex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  if (!email) loginerrors.push({ emailError: "Email is required" });
  else if (!emailregex.test(email)) loginerrors.push({ emailError: "Valid email is required" });

  if (!password) loginerrors.push({ passwordError: "Password is required" });

  if (loginerrors.length !== 0) {
    e.preventDefault(); 
    loginerrors.forEach((err, index) => {
      setTimeout(() => showError(err, "error"), index * 500);
    });
  }
});
