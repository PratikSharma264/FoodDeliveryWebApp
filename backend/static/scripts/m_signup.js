
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


document.addEventListener("DOMContentLoaded", function () {
  const errorScript = document.getElementById("form-errors");
  if (errorScript) {
    const errors = JSON.parse(errorScript.textContent);
    Object.keys(errors).forEach((field, index) => {
      errors[field].forEach((err, i) => {
        const errorObj = {};
        errorObj[field + "Error"] = err.message;
        setTimeout(() => {
          showError(errorObj, "error");
        }, (index + i) * 1000);
      });
    });
  }

  const successScript = document.getElementById("signup-success");
  if (successScript) {
    const successData = JSON.parse(successScript.textContent);
    showError({ success: successData.message }, "success");

    setTimeout(() => {
      window.location.href = "/"; 
    }, 3000);
  }
});


form.addEventListener("submit", function (e) {
  signuperrors.length = 0;

  const fullname = document.getElementById("fullname").value.trim();
  const email = document.getElementById("email").value.trim();
  const phonenumber = document.getElementById("phonenumber").value.trim();
  const password = document.getElementById("password").value.trim();
  const confirmpassword = document.getElementById("confirmpassword").value.trim();

  const emailregex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  if (!fullname) {
    signuperrors.push({ fullnameError: "Full name is required" });
  }

  if (!email) {
    signuperrors.push({ emailError: "Email is required" });
  } else if (!emailregex.test(email)) {
    signuperrors.push({ emailError: "Valid email is required" });
  }

  if (!phonenumber) {
    signuperrors.push({ phonenumberError: "Phonenumber is required" });
  } else if (phonenumber.length !== 10) {
    signuperrors.push({ phonenumberError: "Valid phonenumber is required" });
  }

  if (!password) {
    signuperrors.push({ passwordError: "Password is required" });
  }

  if (!confirmpassword) {
    signuperrors.push({ confirmpasswordError: "Confirm Password is required" });
  } else if (confirmpassword !== password) {
    signuperrors.push({ confirmpasswordError: "Confirm Password must match the password" });
  }

  if (signuperrors.length !== 0) {
    e.preventDefault(); 
    signuperrors.forEach((err, index) => {
      setTimeout(() => {
        showError(err, "error");
      }, index * 500);
    });
  }
});
