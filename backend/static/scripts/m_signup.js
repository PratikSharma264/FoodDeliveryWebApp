const signuperrors = [];
const form = document.getElementById("signup-form");

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
  const fullname = forminstance.get("fullname").trim();
  const email = forminstance.get("email").trim();
  const phonenumber = forminstance.get("phonenumber").trim();
  const password = forminstance.get("password").trim();
  const confirmpassword = forminstance.get("confirmpassword").trim();

  const emailregex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  signuperrors.length = 0;
  if (!fullname) {
    signuperrors.push({
      fullnameError: "Full name is required",
    });
  }

  if (!email) {
    signuperrors.push({
      emailError: "Email is required",
    });
  } else if (!emailregex.test(email)) {
    signuperrors.push({
      emailError: "Valid email is required",
    });
  }

  if (!phonenumber) {
    signuperrors.push({
      phonenumberError: "Phonenumber is required",
    });
  } else if (phonenumber.length !== 10) {
    signuperrors.push({
      phonenumberError: "Valid phonenumber is required",
    });
  }

  if (!password) {
    signuperrors.push({
      passwordError: "Password is required",
    });
  }

  if (!confirmpassword) {
    signuperrors.push({
      confirmpasswordError: "Confirm Password is required",
    });
  } else if (confirmpassword !== password) {
    signuperrors.push({
      confirmpasswordError: "Confirm Password must match the password",
    });
  }
  if (signuperrors.length !== 0) {
    signuperrors.forEach((err, index) => {
      setTimeout(() => {
        showError(err, "error");
      }, index * 2000);
    });
    return;
  }
  const dataToSend = {
    fullname,
    email,
    phonenumber,
    password,
  };
  try {
    const response = await fetch(
      "https://8d058f57-310c-49fa-9b40-ca0a70eb56aa.mock.pstmn.io/signup",
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
      message: "Successfully registered",
    };
    document.getElementById("fullname").value = "";
    document.getElementById("email").value = "";
    document.getElementById("phonenumber").value = "";
    document.getElementById("password").value = "";
    document.getElementById("confirmpassword").value = "";
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
