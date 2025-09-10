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

function previewImage(event) {
    const reader = new FileReader();
    const imagePreview = document.getElementById("image-preview-img");
    
    reader.onload = function () {
        imagePreview.style.display = "block"; 
        imagePreview.src = reader.result; 
    };
    
    reader.readAsDataURL(event.target.files[0]); 
}


document.addEventListener("DOMContentLoaded", function () {
  const map = L.map("map").setView([27.7, 85.3], 12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
  }).addTo(map);

  let marker;

  const bhaktapurPolygon = L.polygon([
  [27.636, 85.406],
  [27.636, 85.454],
  [27.708, 85.454],
  [27.708, 85.406]
], {
  color: "#e91e63",
  fillColor: "#e91e63",
  fillOpacity: 0.2,
  interactive: false,
}).addTo(map);



  const bhaktapurBounds = bhaktapurPolygon.getBounds();
  map.setMaxBounds(bhaktapurBounds);
  map.fitBounds(bhaktapurBounds);

    // const lat = parseFloat(document.getElementById("lat").value || 0).toFixed(6);
    // const lng = parseFloat(document.getElementById("lng").value || 0).toFixed(6);
    const lat = 27.636;
    const lng = 85.406;


   if (bhaktapurBounds.contains([lat, lng])) {
          map.setView([lat, lng], 13);
          marker = L.marker([lat, lng]).addTo(map);
        } else {
          showError({
            mapError: "User is outside Bhaktapur Valley. Using default view."
          },"error");
        }


  map.on("click", function (e) {
    if (bhaktapurPolygon.getBounds().contains(e.latlng)) {
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
      showError({
            mapError: "Please select a location inside Bhaktapur Valley."
          },"error");
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const updateBtn = document.querySelector(".bioupdate-btn");
  const cancelBtn = document.getElementById("cancel-update");
  const submitBtn = document.getElementById("merchant-submit-btn");
  let updateBioErrors = [];

  const profileActual = document.getElementById("profileinfo-actual");
  const profileForm = document.getElementById("profileinfo-toupdate");

  // update btn click for bio update
  updateBtn.addEventListener("click", () => {
    profileActual.classList.add("profileinfo-hide");
    profileForm.classList.remove("profileinfo-hide");

    document.getElementById("restaurant-name").value = "";
    document.getElementById("owner-name").value = "";
    document.getElementById("email").value = "";
    document.getElementById("contact").value = "";
    document.getElementById("address").value = "";
    document.getElementById("restype").value = "";
    document.getElementById("description").value = "";
  });

  // cancel update of bio info
  cancelBtn.addEventListener("click", (e) => {
    e.preventDefault();
    document.getElementById("restaurant-name").value = "";
    document.getElementById("owner-name").value = "";
    document.getElementById("email").value = "";
    document.getElementById("contact").value = "";
    document.getElementById("address").value = "";
    document.getElementById("restype").value = "";
    document.getElementById("description").value = "";
    profileForm.classList.add("profileinfo-hide");
    profileActual.classList.remove("profileinfo-hide");
  });

  // after submit of bio info handle
  submitBtn.addEventListener("submit",(e)=>{
    updateBioErrors.length = 0;
    const restaurantName = document.getElementById("restaurant-name").value.trim();
    const ownerName = document.getElementById("owner-name").value.trim();
    const email = document.getElementById("email").value.trim();
    const contact = document.getElementById("contact").value.trim();
    const address = document.getElementById("address").value.trim();
    const restaurantType = document.getElementById("restype").value;
    const description = document.getElementById("description").value.trim();

    const emailregex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if(!restaurantName){
      updateBioErrors.push({
        restaurantNameError : "Restaurant Name is required"
      })
    }

    if(!ownerName){
      updateBioErrors.push({
        ownerNameError : "Owner Name is required"
      })
    }

    if(!email){
      updateBioErrors.push({
        emailError : "Email is required"
      })
    } else if(!emailregex.test(email)) {
      updateBioErrors.push({
        emailError : "Enter the valid email"
      })
    }

    if(!address){
      updateBioErrors.push({
        addressError : "Address is required"
      })
    }

    if(!contact){
      updateBioErrors.push({
        contactError : "Contact is required"
      }) 
    } else if (![8, 9, 10].includes(contact.length)) {
      updateBioErrors.push({
        contactError: "Valid contact number is required",
      });
    }

    if(!restaurantType){
      updateBioErrors.push({
        restaurantTypeError : "Restaurant Type is required"
      })
    }

    if(!description){
      updateBioErrors.push({
        descriptionError : "Description is required"
      })
    }

    if (updateBioErrors.length !== 0) {
      e.preventDefault();
      updateBioErrors.forEach((err, index) => {
        setTimeout(() => {
          showError(err, "error");
        }, index * 500);
      });
    }

  })


  // profile change btn handle
  const profilePicChangeBtn = document.getElementById("profilepicchangebtn");
  profilePicChangeBtn.addEventListener("click",(e)=>{
    document.getElementById("profilepicform-container").classList.remove("hidden");
    document.body.style.overflow = "hidden";
  })

  const profilePicInput = document.getElementById("profile_picture");
  profilePicInput.addEventListener("change", function(event) {
  const previewinfo = document.getElementById("previewinfo");
  previewinfo.style.display = "none";
  previewImage(event); 
});

const profilePicCancelBtn = document.getElementById("close-ppmodal");
profilePicCancelBtn.addEventListener("click",(e)=>{
  document.getElementById("profilepicform-container").classList.add("hidden");
  document.body.style.overflow = "auto";
})

const updateLoctionBtn = document.getElementById("map-update-btn");
updateLoctionBtn.addEventListener("click",(e)=>{
  document.getElementById("revalidate-locationupdate").classList.remove("hidden");
  document.body.style.overflow = "hidden";
});

document.getElementById("no-btn").addEventListener("click",(e)=>{
  document.getElementById("revalidate-locationupdate").classList.add("hidden");
  document.body.style.overflow = "auto";
})

document.getElementById("yes-btn").addEventListener("click", (e) => {
  const lat = document.getElementById("updated-lat").value;
  const lng = document.getElementById("updated-lng").value;

  if (!lat || !lng) {
    e.preventDefault();
    showError({ locationError: "Please select a valid location before submitting." }, "error");
  }
});


});
