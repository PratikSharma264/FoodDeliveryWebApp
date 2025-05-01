// header

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

// progress bar

const steps = document.querySelectorAll(".step");
const lines = document.querySelectorAll(".line");
const formSteps = document.querySelectorAll(".form-step");
let currentStep = 0;

document.getElementById("nextbtn").addEventListener("click", (e) => {
  e.preventDefault();

  const currentForm = formSteps[currentStep];
  const inputs = currentForm.querySelectorAll(
    "input[required], textarea[required]"
  );
  let allFilled = true;

  inputs.forEach((input) => {
    if (!input.value.trim()) allFilled = false;
  });

  const errorDivId = "form-error";
  let errorDiv = document.getElementById(errorDivId);

  if (!errorDiv) {
    errorDiv = document.createElement("div");
    errorDiv.id = errorDivId;
    errorDiv.style.color = "red";
    errorDiv.style.textAlign = "center";
    errorDiv.style.marginTop = "10px";
    document.querySelector(".btn").before(errorDiv);
  }

  if (!allFilled) {
    errorDiv.textContent =
      "Please fill in all required fields before proceeding.";
    return;
  } else {
    errorDiv.textContent = "";
  }

  // Move to next step
  formSteps[currentStep].classList.remove("active");
  steps[currentStep].classList.remove("current");
  steps[currentStep].classList.add("completed");

  currentStep++;

  if (currentStep < formSteps.length) {
    formSteps[currentStep].classList.add("active");
    steps[currentStep].classList.add("current");
    if (lines[currentStep - 1]) {
      lines[currentStep - 1].style.backgroundColor = "#2196f3";
    }
  } else {
    // Maybe submit the form here or show final message
    document.getElementById("main-form").submit();
  }
});

document.addEventListener("DOMContentLoaded", () => {
  formSteps[0].classList.add("active");
});

// map interaction

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

  // kathmanduValleyPolygon.bindPopup("Allowed region: Kathmandu Valley");

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

// image upload handle

document.getElementById("profile-pic").addEventListener("change", function (e) {
  const file = e.target.files[0];
  const preview = document.getElementById("profile-preview");
  if (file) {
    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";
  }
});

document.getElementById("cover-photo").addEventListener("change", function (e) {
  const file = e.target.files[0];
  const preview = document.getElementById("cover-preview");
  if (file) {
    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";
  }
});
