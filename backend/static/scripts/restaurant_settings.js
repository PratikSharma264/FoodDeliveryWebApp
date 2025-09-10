document.addEventListener("DOMContentLoaded",(e)=>{
const djangoMessages = document.getElementById("django-messages");
if (djangoMessages) {
  try {
    const parsedMessages = JSON.parse(djangoMessages.textContent);

    if (parsedMessages.errors && parsedMessages.errors.length > 0) {
      parsedMessages.errors.forEach((error, index) => {
        setTimeout(() => {
          showError({ error: error }, "error");
        }, index * 500);
      });
    }

    if (parsedMessages.success && parsedMessages.success.length > 0) {
      parsedMessages.success.forEach((msg, index) => {
        setTimeout(() => {
          showError({ success: msg }, "success");
        }, index * 500);
      });
    }
  } catch (err) {
    console.error("Error parsing Django messages JSON:", err);
  }
}

})


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

    const lat = parseFloat(document.getElementById("lat").value);
    const lng = parseFloat(document.getElementById("lng").value) ;

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
  let updateProfilePicErrors = [];
  let latlngError = [];

  const profileActual = document.getElementById("profileinfo-actual");
  const profileForm = document.getElementById("profileinfo-toupdate");

  
  updateBtn.addEventListener("click", async (e) => {
    profileActual.classList.add("profileinfo-hide");
    profileForm.classList.remove("profileinfo-hide");
    const resid = updateBtn.getAttribute("id");
 
    try{
      const response = await fetch(`http://127.0.0.1:8000/json/update-restaurant-bio/${resid}/`);
      const data = await response.json();
    document.getElementById("restaurant-name").value = data.data.restaurant_name || "";
    document.getElementById("owner-name").value = data.data.owner_name || "";
    document.getElementById("email").value = data.data.owner_email || "";
    document.getElementById("contact").value = data.data.owner_contact || "";
    document.getElementById("address").value = data.data.restaurant_address || "";
    document.getElementById("restype").value = data.data.restaurant_type || "";
    document.getElementById("description").value = data.data.description || "";
    }catch(err){
      showError(err.message||"error while fetching resturant data from server","error");
    }
  });

 
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


const profileFormElement = document.getElementById("profileinfo-form");

profileFormElement.addEventListener("submit",(e)=>{
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
   document.getElementById("updated-lat").value = document.getElementById("lat").value;
   document.getElementById("updated-lng").value = document.getElementById("lng").value;
  document.getElementById("revalidate-locationupdate").classList.remove("hidden");
  document.body.style.overflow = "hidden";
});

document.getElementById("no-locupdatebtn").addEventListener("click",(e)=>{
  document.getElementById("revalidate-locationupdate").classList.add("hidden");
  document.body.style.overflow = "auto";
})

document.querySelector(".latlngupdate-form").addEventListener("submit", (e) => {
  latlngError.length = 0;
  const latitude = document.getElementById("updated-lat").value;
  const longitude = document.getElementById("updated-lng").value;

   const bhaktapurBounds = {
      minLat: 27.64, // South
      maxLat: 27.75, // North
      minLng: 85.4, // West
      maxLng: 85.46, // East
    };

   if (!latitude) {
      latlngError.push({ latitudeError: "Latitude is required" });
    }
    if (!longitude) {
      latlngError.push({ longitudeError: "Longitude is required" });
    }

    if (latitude && longitude) {
      const { minLat, maxLat, minLng, maxLng } = bhaktapurBounds;

      if (
        latitude < minLat ||
        latitude > maxLat ||
        longitude < minLng ||
        longitude > maxLng
      ) {
        latlngError.push({
          locationError:
            "Latitude and Longitude must be inside Bhaktapur Valley",
        });
      }
    }
     if (latlngError.length > 0) {
      e.preventDefault();
      latlngError.forEach((err, index) => {
        setTimeout(() => {
          showError(err, "error");
        }, index * 500);
      });
    }
});

const profilePicForm = document.getElementById("profilepic-form")
profilePicForm.addEventListener("submit",(e)=>{
  updateProfilePicErrors.length = 0;
  const forminstance = new FormData(profilePicForm);

  const pp =  forminstance.get("profile_picture");

  if (!pp || pp.size === 0 || !pp.name) {
      updateProfilePicErrors.push({
        ppError: "Profile image is required",
      });
    } else if (pp.size > 2 * 1024 * 1024) {
      updateProfilePicErrors.push({
        ppError: "Profile image must be less than 2MB",
      });
    }
    
    if (updateProfilePicErrors.length > 0) {
      e.preventDefault();
      updateProfilePicErrors.forEach((err, index) => {
        setTimeout(() => {
          showError(err, "error");
        }, index * 500);
      });
    }
})


});
