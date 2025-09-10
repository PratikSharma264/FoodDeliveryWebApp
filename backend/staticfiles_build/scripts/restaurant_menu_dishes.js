const addItemBtn = document.querySelector("#currentmenu-header button");
const modal = document.getElementById("additem-modal");
const closeModalBtn = document.getElementById("close-modal");

addItemBtn.addEventListener("click", () => {
  document.getElementById("item-name").value = "";
  document.getElementById("price").value = "";
  document.getElementById("discount").value = "";
  document.getElementById("category").value = "";
  document.getElementById("availability").value = "";
  document.getElementById("description").value = "";
  document.getElementById("item-id").value = "";
  modal.classList.remove("hidden");
  document.body.style.overflow = "hidden";
});

closeModalBtn.addEventListener("click", () => {
  document.getElementById("item-name").value = "";
  document.getElementById("price").value = "";
  document.getElementById("discount").value = "";
  document.getElementById("category").value = "";
  document.getElementById("availability").value = "";
  document.getElementById("description").value = "";
  document.getElementById("item-id").value = "";
  modal.classList.add("hidden");
  document.body.style.overflow = "auto";
});

document.addEventListener("DOMContentLoaded", (e) => {
  const updateBtns = document.querySelectorAll(".update-currentitems");
  const itemForm = document.getElementById("item-form");

  updateBtns.forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      const foodId = parseInt(e.currentTarget.getAttribute("id"));
      console.log("FOODID:", foodId);
      const response = await fetch(
        `http://127.0.0.1:8000/menu-dishes/update/${foodId}`
      );
      const data = await response.json();

      document.getElementById("item-name").value = data.name;
      document.getElementById("price").value = data.price;
      document.getElementById("discount").value = data.discount;
      document.getElementById("category").value = data.veg_nonveg;
      document.getElementById("availability").value = data.availability_status;
      document.getElementById("description").value = data.description;
      document.getElementById("item-id").value = data.id;
      //   if (data.profile_picture) {
      //     const imageUrl = data.profile_picture;
      //     const fileName = imageUrl.split("/").pop();
      //     document.getElementById("image-preview").innerHTML = fileName;
      //   }
      document.getElementById("additem-modal").classList.remove("hidden");
      document.body.style.overflow = "hidden";
    });
  });
});

document.addEventListener("DOMContentLoaded", (e) => {
  const revalidatecontainer = document.getElementById("revalidate-delete");
  const deletebtns = document.querySelectorAll(".delete-currentitems");
  const nobtn = document.querySelector("#no-btn");

  const closerevalidatepopup = document.getElementById(
    "close-revalidate-popup"
  );

  closerevalidatepopup.addEventListener("click", () => {
    revalidatecontainer.classList.add("hidden");
    document.body.style.overflow = "hidden";
  });

  if (nobtn) {
    nobtn.addEventListener("click", (e) => {
      revalidatecontainer.classList.add("hidden");
      document.body.style.overflow = "auto";
    });
  }

  if (deletebtns) {
    deletebtns.forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const foodId = parseInt(e.currentTarget.getAttribute("id"));
        itemToDeleteId = foodId;
        const hiddenInput = document.getElementById("item-to-delete");
        hiddenInput.value = foodId;
        revalidatecontainer.classList.remove("hidden");
        document.body.style.overflow = "hidden";
      });
    });
  }
});

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

document.addEventListener("DOMContentLoaded", () => {
  const additemform = document.getElementById("item-form");
  let additemerrors = [];

  additemform.addEventListener("submit", (e) => {
    additemerrors.length = 0;

    const formData = new FormData(additemform);

    const itemName = (formData.get("name") || "").trim();
    const itemPrice = (formData.get("price") || "").trim();
    const itemDiscount = (formData.get("discount") || "").trim();
    const itemCategory = (formData.get("veg_nonveg") || "").trim();
    const itemAvailabilityStatus = (
      formData.get("availability_status") || ""
    ).trim();
    const itemPicture = formData.get("profile_picture");
    const itemDescription = (formData.get("description") || "").trim();

    if (!itemName) {
      additemerrors.push({ itemNameError: "Item Name is required" });
    }

    if (!itemPrice) {
      additemerrors.push({ itemPriceError: "Item Price is required" });
    }

    if (!itemDiscount) {
      additemerrors.push({ itemDiscountError: "Item Discount is required" });
    }

    if (!itemCategory) {
      additemerrors.push({ itemCategoryError: "Item Category is required" });
    }

    if (!itemAvailabilityStatus) {
      additemerrors.push({
        itemAvailabilityStatusError: "Item Availability is required",
      });
    }

    if (!itemDescription) {
      additemerrors.push({
        itemDescriptionError: "Item Description is required",
      });
    }

    if (!itemPicture || itemPicture.size === 0 || !itemPicture.name) {
      additemerrors.push({
        itemPictureError: "Item image is required",
      });
    } else if (itemPicture.size > 2 * 1024 * 1024) {
      additemerrors.push({
        itemPictureError: "Item image must be less than 2MB",
      });
    }

    if (additemerrors.length > 0) {
      e.preventDefault();
      additemerrors.forEach((err, index) => {
        setTimeout(() => {
          showError(err, "error");
        }, index * 500);
      });
    }
  });
});
