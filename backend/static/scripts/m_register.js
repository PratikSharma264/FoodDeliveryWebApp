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

      if (btn.textContent.trim().toLowerCase() === "merchant") {
        merchantForm.style.display = "block";
        deliveryBoyForm.style.display = "none";
      } else {
        merchantForm.style.display = "none";
        deliveryBoyForm.style.display = "block";
      }
    });
  });
});
