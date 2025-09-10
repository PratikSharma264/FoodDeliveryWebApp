// const foods = [
//   {
//     id: 1,
//     name: "Margherita Pizza",
//     price: 9.99,
//     discount: 0,
//     description: "Classic pizza with tomatoes, mozzarella, and basil",
//     category: "veg",
//     image:
//       "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?q=80&w=869&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//     availability: "available",
//   },
//   {
//     id: 2,
//     name: "Pepperoni Pizza",
//     price: 11.99,
//     discount: 0,
//     description: "Pepperoni, cheese, and tomato sauce",
//     category: "non-veg",
//     image:
//       "https://plus.unsplash.com/premium_photo-1733259709671-9dbf22bf02cc?q=80&w=580&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//     availability: "available",
//   },
//   {
//     id: 3,
//     name: "California Roll",
//     price: 7.49,
//     discount: 10,
//     description: "Crab, avocado, and cucumber",
//     category: "non-veg",
//     image:
//       "https://images.unsplash.com/photo-1559410545-0bdcd187e0a6?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//     availability: "available",
//   },
//   {
//     id: 4,
//     name: "Spicy Tuna Roll",
//     price: 8.99,
//     discount: 0,
//     description: "Tuna with spicy mayo",
//     category: "non-veg",
//     image:
//       "https://plus.unsplash.com/premium_photo-1712949141720-6ddee2bde0bf?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//     availability: "outofstock",
//   },
//   {
//     id: 5,
//     name: "Beef Taco",
//     price: 3.99,
//     discount: 5,
//     description: "Ground beef, lettuce, cheese, and salsa",
//     category: "non-veg",
//     image:
//       "https://plus.unsplash.com/premium_photo-1664391890333-b6708e34b021?q=80&w=729&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//     availability: "available",
//   },
//   {
//     id: 6,
//     name: "Chicken Quesadilla",
//     price: 6.49,
//     discount: 0,
//     description: "Grilled chicken with cheese in a tortilla",
//     category: "non-veg",
//     image:
//       "https://images.unsplash.com/photo-1628430044262-fb84cffbb744?q=80&w=871&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//     availability: "available",
//   },
//   {
//     id: 7,
//     name: "BBQ Chicken Pizza",
//     price: 12.49,
//     discount: 0,
//     description: "Grilled chicken, BBQ sauce, onions, and mozzarella",
//     category: "non-veg",
//     image:
//       "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=481&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//     availability: "lowstock",
//   },
//   {
//     id: 8,
//     name: "Shrimp Tempura Roll",
//     price: 9.25,
//     discount: 0,
//     description: "Shrimp tempura, avocado, and eel sauce",
//     category: "non-veg",
//     image:
//       "https://images.unsplash.com/photo-1570078362689-c57c33cca104?q=80&w=436&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//     availability: "available",
//   },
//   {
//     id: 9,
//     name: "Carnitas Taco",
//     price: 4.49,
//     discount: 0,
//     description: "Slow-cooked pork with onion and cilantro",
//     category: "non-veg",
//     image:
//       "https://plus.unsplash.com/premium_photo-1678051386853-5623e723745a?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//     availability: "outofstock",
//   },
//   {
//     id: 10,
//     name: "Veggie Quesadilla",
//     price: 5.99,
//     discount: 0,
//     description: "Grilled vegetables and cheese in a tortilla",
//     category: "veg",
//     image:
//       "https://images.unsplash.com/photo-1708388064941-de7a9f879bf9?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//     availability: "available",
//   },
//   {
//     id: 11,
//     name: "Four Cheese Pizza",
//     price: 10.99,
//     discount: 0,
//     description: "Mozzarella, cheddar, parmesan, and gorgonzola",
//     category: "veg",
//     image:
//       "https://plus.unsplash.com/premium_photo-1691911162192-f4a5cd1b7403?q=80&w=387&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//     availability: "available",
//   },
//   {
//     id: 12,
//     name: "Dragon Roll",
//     price: 10.49,
//     discount: 0,
//     description: "Eel, cucumber, avocado, and tobiko",
//     category: "non-veg",
//     image:
//       "https://images.unsplash.com/photo-1712192674556-4a89f20240c1?q=80&w=774&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//     availability: "outofstock",
//   },
// ];

let itemToDeleteId = null;
let foodss = null;

const addItemBtn = document.querySelector("#currentmenu-header button");
const modal = document.getElementById("additem-modal");
const closeModalBtn = document.getElementById("close-modal");

addItemBtn.addEventListener("click", () => {
  modal.classList.remove("hidden");
  document.body.style.overflow = "hidden";
});

closeModalBtn.addEventListener("click", () => {
  modal.classList.add("hidden");
  document.body.style.overflow = "auto";
});

// document.getElementById("item-form").addEventListener("submit", async (e) => {
//   e.preventDefault();
//     const name = document.getElementById("item-name").value;
//     const price = document.getElementById("price").value;
//     const discount = parseInt(document.getElementById("discount").value);
//     const category = document.getElementById("category").value;
//     const availability = document.getElementById("availability").value;
//     const image = document.getElementById("item-image").value;
//     const description = document.getElementById("description").value;

//     const foodItem = {
//       name,
//       price,
//       discount,
//       description,
//       category,
//       image,
//       availability,
//     };
//   });

// const updatebtns = document.querySelectorAll(".update-currentitems");

// updatebtns.forEach((btn) => {
//   btn.addEventListener("click", (e) => {
//     const foodId = parseInt(e.currentTarget.dataset.id); // instead of getAttribute("id")
//     console.log("Edit:", foodId);
//     // TODO: fetch the food data via Ajax or populate modal with Django form
//   });
// });

// deletebtns.forEach((btn) => {
//   btn.addEventListener("click", (e) => {
//     const foodId = parseInt(e.currentTarget.dataset.id); // fix here too
//     console.log("Delete:", foodId);
//     itemToDeleteId = foodId;
//     revalidatecontainer.classList.remove("hidden");
//     document.body.style.overflow = "hidden";
//   });
// });
// Use event delegation on container
container.addEventListener("click", (e) => {
  // Edit button
  if (e.target.closest(".update-currentitems")) {
    const foodId = parseInt(
      e.target.closest(".update-currentitems").dataset.id
    );
    console.log("Edit:", foodId);
    // TODO: populate form with foodId’s data and open modal
  }

  // Delete button
  if (e.target.closest(".delete-currentitems")) {
    const foodId = parseInt(
      e.target.closest(".delete-currentitems").dataset.id
    );
    console.log("Delete:", foodId);
    itemToDeleteId = foodId;
    revalidatecontainer.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  }
});

document.getElementById("item-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const id = parseInt(document.getElementById("item-id").value);
  const name = document.getElementById("item-name").value;
  const price = parseFloat(document.getElementById("price").value);
  const discount = parseInt(document.getElementById("discount").value);
  const description = document.getElementById("description").value;
  const category = document.getElementById("category").value;
  const image = document.getElementById("item-image").value;
  const availability = document.getElementById("availability").value;

  const foodItem = {
    id,
    name,
    price,
    discount,
    description,
    category,
    image,
    availability,
  };

  const existingIndex = foods.findIndex((f) => f.id === id);

  if (existingIndex !== -1) {
    (url = ""), (method = "PUT");
  } else {
    (url = ""), (method = "POST");
  }

  try {
    const response = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(foodItem),
    });
    if (!response.ok || response.status !== 200) {
      throw new Error("Failed to save data.");
    }
    const updatedData = response.json();

    if (method === "PUT") {
      foods[existingIndex] = updatedData;
    } else {
      foods.push(updatedData);
    }

    renderFood();
    modal.classList.add("hidden");
    document.body.style.overflow = "auto";
  } catch (err) {
    console.error("error:", err);
    alert("there was error saving the item.");
  }
});

const revalidatecontainer = document.getElementById("revalidate-delete");
const deletebtns = document.querySelectorAll(".delete-currentitems");
const yesbtn = document.querySelector("#yes-btn");
const nobtn = document.querySelector("#no-btn");

const closerevalidatepopup = document.getElementById("close-revalidate-popup");

closerevalidatepopup.addEventListener("click", () => {
  revalidatecontainer.classList.add("hidden");
  document.body.style.overflow = "hidden";
});

yesbtn.addEventListener("click", async () => {
  if (itemToDeleteId === null) return;
  const url = `http://127.0.0.1:8000/delete-item/${itemToDeleteId}/`;
  try {
    const response = await fetch(url, {
      method: "DELETE",
    });
    if (!response.ok) {
      throw new Error("failed to delete item");
    }
    const index = foods.findIndex((food) => food.id === itemToDeleteId);
    if (index !== -1) {
      foods.splice(index, 1);
    }
    container.innerHTML = "";
    renderFood();
    itemToDeleteId = null;
    revalidatecontainer.classList.add("hidden");
    document.body.style.overflow = "auto";
  } catch (err) {
    console.error("error:", err);
  }
});

nobtn.addEventListener("click", () => {
  revalidatecontainer.classList.add("hidden");
  itemToDeleteId = null;
  document.body.style.overflow = "auto";
});
