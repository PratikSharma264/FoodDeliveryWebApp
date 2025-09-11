function showError(messageobj, condition) {
  console.log(messageobj);
  const key = Object.keys(messageobj);
  const cardContainer = document.getElementById("card-container");

  if (!cardContainer) {
    console.error("Card container not found in DOM.");
    return;
  }

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
  }, 3000);
}

document.addEventListener("DOMContentLoaded", function () {
  const errorScript = document.getElementById("form-errors");
  if (errorScript) {
    const errors = JSON.parse(errorScript.textContent);
    Object.keys(errors).forEach((field, index) => {
      errors[field].forEach((err, i) => {
        const errorObj = {};
        errorObj[field + "Error"] = err;
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

document.addEventListener("DOMContentLoaded", function () {
  const map = L.map("map").setView([27.7, 85.3], 12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
  }).addTo(map);

  let marker;

  const kathmanduValleyPolygon = L.polygon(
    [
      [27.7167, 85.204],
      [27.587, 85.2785],
      [27.609, 85.432],
      [27.8, 85.4785],
      [27.806, 85.27],
      [27.74, 85.2],
    ],
    {
      color: "#2196f3",
      fillColor: "#2196f3",
      fillOpacity: 0.2,
      interactive: false,
    }
  ).addTo(map);

  const kathmanduBounds = kathmanduValleyPolygon.getBounds();
  map.setMaxBounds(kathmanduBounds);
  map.fitBounds(kathmanduBounds);

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;

        if (kathmanduBounds.contains([lat, lng])) {
          map.setView([lat, lng], 13);
          marker = L.marker([lat, lng]).addTo(map);
          document.getElementById("lat").value = lat.toFixed(6);
          document.getElementById("lng").value = lng.toFixed(6);
        } else {
          console.log("User is outside Kathmandu Valley. Using default view.");
        }
      },
      () => {
        console.log("Geolocation failed. Using default Kathmandu view.");
      }
    );
  }

  map.on("click", function (e) {
    if (kathmanduValleyPolygon.getBounds().contains(e.latlng)) {
      const lat = e.latlng.lat.toFixed(6);
      const lng = e.latlng.lng.toFixed(6);

      if (marker) {
        marker.setLatLng(e.latlng);
      } else {
        marker = L.marker(e.latlng).addTo(map);
      }

      document.getElementById("lat").value = lat;
      document.getElementById("lng").value = lng;
    } else {
      alert("Please select a location inside Kathmandu Valley.");
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const roleButtons = document.querySelectorAll(".role-btn");
  const merchantForm = document.getElementById("merchantreg-main");
  const deliveryBoyForm = document.getElementById("deliveryboyreg-main");

  const urlParams = new URLSearchParams(window.location.search);
  const roleParam = urlParams.get("role");

  let merchantVisible = true;

  if (roleParam) {
    const role = roleParam.toLowerCase().trim();

    if (role.includes("merchant")) {
      merchantVisible = true;
    } else if (role.includes("delivery")) {
      merchantVisible = false;
    }
  }

  if (merchantVisible) {
    merchantForm.style.display = "block";
    deliveryBoyForm.style.display = "none";
    roleButtons[0].classList.add("role-active");
    roleButtons[1].classList.remove("role-active");
  } else {
    merchantForm.style.display = "none";
    deliveryBoyForm.style.display = "block";
    roleButtons[1].classList.add("role-active");
    roleButtons[0].classList.remove("role-active");
  }

  roleButtons.forEach((btn, index) => {
    btn.addEventListener("click", () => {
      roleButtons.forEach((b) => b.classList.remove("role-active"));
      btn.classList.add("role-active");

      let role;
      if (btn.textContent.trim().toLowerCase() === "merchant") {
        merchantForm.style.display = "block";
        deliveryBoyForm.style.display = "none";
        role = "merchant";
      } else {
        merchantForm.style.display = "none";
        deliveryBoyForm.style.display = "block";
        role = "deliveryman";
      }
      const newUrl = new URL(window.location);
      newUrl.searchParams.set("role", role);
      window.history.pushState({}, "", newUrl);
    });
  });

  const mform = document.getElementById("merchant-form");
  // if (mform.style.display === "none") return;
  let mregerrors = [];

  mform.addEventListener("submit", (e) => {
    mregerrors.length = 0;

    const restaurant_name = document
      .getElementById("restaurant-name")
      .value.trim();
    const owner_name = document.getElementById("owner-name").value.trim();
    const owner_contact = document.getElementById("owner_contact").value.trim();
    const email = document.getElementById("email").value.trim();
    const restaurant_address = document
      .getElementById("restaurant_address")
      .value.trim();
    const cuisine = document.getElementById("cuisine").value.trim();
    const description = document.getElementById("description").value.trim();
    const restaurant_type = document.getElementById("restype").value.trim();

    const latitude = document.getElementById("lat").value.trim();
    const longitude = document.getElementById("lng").value.trim();

    const emailregex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const bhaktapurBounds = {
      minLat: 27.64, // South
      maxLat: 27.75, // North
      minLng: 85.4, // West
      maxLng: 85.46, // East
    };

    if (!restaurant_name) {
      mregerrors.push({
        restaurant_nameError: "Restaurant name is required",
      });
    }
    if (!owner_name) {
      mregerrors.push({
        owner_nameError: "Owner name is required",
      });
    }

    if (!email) {
      mregerrors.push({ emailError: "Email is required" });
    } else if (!emailregex.test(email)) {
      mregerrors.push({ emailError: "Valid email is required" });
    }

    if (!owner_contact) {
      mregerrors.push({ phonenumberError: "Owner contact is required" });
    } else if (![8, 9, 10].includes(owner_contact.length)) {
      mregerrors.push({
        phonenumberError: "Valid contact number is required",
      });
    }

    if (!restaurant_address) {
      mregerrors.push({
        restaurant_addressError: "Resturant address is required",
      });
    }

    if (!description) {
      mregerrors.push({
        descriptionError: "Description is required",
      });
    }

    if (!restaurant_type) {
      mregerrors.push({
        restaurant_typeError: "Restaurant type is required",
      });
    }

    if (!latitude) {
      mregerrors.push({ latitudeError: "Latitude is required" });
    }
    if (!longitude) {
      mregerrors.push({ longitudeError: "Longitude is required" });
    }

    if (latitude && longitude) {
      const { minLat, maxLat, minLng, maxLng } = bhaktapurBounds;

      if (
        latitude < minLat ||
        latitude > maxLat ||
        longitude < minLng ||
        longitude > maxLng
      ) {
        mregerrors.push({
          locationError:
            "Latitude and Longitude must be inside Bhaktapur Valley",
        });
      }
    }
    if (mregerrors.length !== 0) {
      e.preventDefault();
      mregerrors.forEach((err, index) => {
        setTimeout(() => {
          showError(err, "error");
        }, index * 500);
      });
    }
  });

  const dform = document.getElementById("deliveryman-form");
  const dregerrors = [];

  dform.addEventListener("submit", (e) => {
    // if (dform.style.display === "none") return;
    dregerrors.length = 0;
    console.log("here");
    const formData = new FormData(dform);

    const first_name = (formData.get("Firstname") || "").trim();
    const last_name = (formData.get("Lastname") || "").trim();
    const address = (formData.get("Address") || "").trim();
    const dutytime = (formData.get("DutyTime") || "").trim();
    const pannumber = (formData.get("PanNumber") || "").trim();
    const vehiclenumber = (formData.get("VehicleNumber") || "").trim();
    const dob = (formData.get("DateofBirth") || "").trim();
    const vehicletype = (formData.get("Vehicle") || "").trim();
    const deliveryzone = (formData.get("Zone") || "").trim();
    const profileimage = formData.get("UserImage");
    const billbookimg = formData.get("BillBookScanCopy");

    if (!first_name)
      dregerrors.push({ firstNameError: "First name is required" });
    if (!last_name) dregerrors.push({ lastNameError: "Last name is required" });
    if (!address) dregerrors.push({ addressError: "Address is required" });
    if (!dutytime) dregerrors.push({ dutytimeError: "Duty time is required" });
    if (!deliveryzone)
      dregerrors.push({ deliveryzoneError: "Delivery zone is required" });
    if (!pannumber) {
      dregerrors.push({
        pannumberError: "Pan number is required",
      });
    }
    if (!dob) {
      dregerrors.push({
        dobError: "Date of Birth is required",
      });
    }
    if (!vehicletype) {
      dregerrors.push({
        vehicletypeError: "Vehicle type is required",
      });
    }
    if (!vehiclenumber) {
      dregerrors.push({
        vehiclenumberError: "Vehicle number is required",
      });
    }

    if (!profileimage || profileimage.size === 0 || !profileimage.name) {
      dregerrors.push({
        profileimageError: "Profile image is required",
      });
    } else if (profileimage.size > 2 * 1024 * 1024) {
      dregerrors.push({
        profileimageError: "Profile image must be less than 2MB",
      });
    }

    if (!billbookimg || billbookimg.size === 0 || !billbookimg.name) {
      dregerrors.push({
        billbookError: "Bill Book Scan Copy is required",
      });
    } else if (billbookimg.size > 2 * 1024 * 1024) {
      dregerrors.push({
        billbookError: "Bill Book Scan Copy must be less than 2MB",
      });
    }

    if (dregerrors.length > 0) {
      e.preventDefault();
      dregerrors.forEach((err, index) => {
        setTimeout(() => {
          showError(err, "error");
        }, index * 500);
      });
    }
  });
});
