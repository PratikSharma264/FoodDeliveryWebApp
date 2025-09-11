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


document.addEventListener("DOMContentLoaded", () => {
  const updateBtn = document.querySelector(".bioupdate-btn");
  const cancelBtn = document.getElementById("cancel-update");
  let updateBioErrors = [];
  let updateProfilePicErrors = [];

  const profileActual = document.getElementById("profileinfo-actual");
  const profileForm = document.getElementById("profileinfo-toupdate");

  
  updateBtn.addEventListener("click", async (e) => {
    profileActual.classList.add("profileinfo-hide");
    profileForm.classList.remove("profileinfo-hide");
    const delivermanid = updateBtn.getAttribute("id");
 
    // try{
    //   const response = await fetch(`http://127.0.0.1:8000/json/update-restaurant-bio/${delivermanid}/`);
    //   const data = await response.json();
    // document.getElementById("first-name").value = data.data.first_name || "";
    // document.getElementById("last-name").value = data.data.last_name || "";
    // document.getElementById("email").value = data.data.email || "";
    // document.getElementById("contact").value = data.data.contact || "";
    // document.getElementById("address").value = data.data.address || "";
    // document.getElementById("dob").value = data.data.dob || "";
    // document.getElementById("pannumber").value = data.data.pan_number|| "";
    // }catch(err){
    //   showError(err.message||"error while fetching deliveryman data from server","error");
    // }
  });

 
  cancelBtn.addEventListener("click", (e) => {
    e.preventDefault();
    document.getElementById("first-name").value = "";
    document.getElementById("last-name").value = "";
    document.getElementById("email").value = "";
    document.getElementById("contact").value = "";
    document.getElementById("address").value = "";
    document.getElementById("dob").value = "";
    document.getElementById("pannumber").value = "";
    profileForm.classList.add("profileinfo-hide");
    profileActual.classList.remove("profileinfo-hide");
  });


const profileFormElement = document.getElementById("profileinfo-form");

profileFormElement.addEventListener("submit",(e)=>{
    updateBioErrors.length = 0;
    const firstName = document.getElementById("first-name").value.trim();
    const lastName = document.getElementById("last-name").value.trim();
    const email = document.getElementById("email").value.trim();
    const contact = document.getElementById("contact").value;
    const address = document.getElementById("address").value.trim();
    const dob = document.getElementById("dob").value;
    const panNumber = document.getElementById("pannumber").value;

    const emailregex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if(!firstName){
      updateBioErrors.push({
        firstNameError : "First Name is required"
      })
    }

    if(!lastName){
      updateBioErrors.push({
        lastNameError : "Last Name is required"
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

    if(!dob){
      updateBioErrors.push({
        dobError : "Date of Birth is required"
      })
    }

    if(!panNumber){
      updateBioErrors.push({
        panNumberError : "Pan number is required"
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
