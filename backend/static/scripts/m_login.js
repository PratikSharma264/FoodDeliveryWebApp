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

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const forminstance = new FormData(form);
  const email = forminstance.get("email").trim();
  const password = forminstance.get("password").trim();

  loginerrors.length = 0;

  if (!email) {
    loginerrors.push({
      emailError: "Email is required",
    });
  }

  if (!password) {
    loginerrors.push({
      passwordError: "Password is required",
    });
  }

  if (loginerrors.length !== 0) {
    loginerrors.forEach((err, index) => {
      setTimeout(() => {
        showError(err, "error");
      }, index * 2000);
    });
    return;
  }
  const dataToSend = {
    email,
    password,
  };

  try {
    const response = await fetch(
      "https://8d058f57-310c-49fa-9b40-ca0a70eb56aa.mock.pstmn.io/login",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dataToSend),
      }
    );
    if (!response.ok) {
      const errorResponse = await response.json();
      throw new Error(errorResponse || "signup failed");
    }
    const result = response.json();
    console.log("result", result);
    const successobj = {
      message: "Log in successfully",
    };
    document.getElementById("email").value = "";
    document.getElementById("password").value = "";
    setTimeout(() => {
      showError(successobj, "success");
    }, 500);
  } catch (err) {
    console.log("error:", err);
    const errorobj = {
      errmsg: err?.message,
    };
    setTimeout(() => {
      showError(errorobj, "error");
    }, 500);
  }
});
