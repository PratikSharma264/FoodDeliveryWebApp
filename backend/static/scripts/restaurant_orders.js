// document.addEventListener("DOMContentLoaded", () => {
//   const orders = [
//     {
//       orderId: "ORD-1001",
//       orderDate: "2025-08-08T14:30:00Z",
//       customer: {
//         customerId: "CUST-001",
//         name: "Alice Johnson",
//         email: "alice.johnson@example.com",
//         phone: "9876543211",
//       },
//       items: [
//         {
//           id: 1,
//           name: "Margherita Pizza",
//           price: 1000,
//           discount: 0,
//           quantity: 1,
//           description: "Classic pizza with tomatoes, mozzarella, and basil",
//           category: "veg",
//           image:
//             "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?q=80&w=869&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//           availability: "available",
//         },
//         {
//           id: 3,
//           name: "California Roll",
//           price: 800,
//           discount: 10,
//           quantity: 2,
//           description: "Crab, avocado, and cucumber",
//           category: "non-veg",
//           image:
//             "https://images.unsplash.com/photo-1559410545-0bdcd187e0a6?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//           availability: "available",
//         },
//       ],
//       totalAmount: 2440,
//       status: "Processing",
//       deliveryman: null,
//       deliveryRequestTime: null,
//       estimatedDeliveryTime: null,
//     },
//     {
//       orderId: "ORD-1002",
//       orderDate: "2025-08-08T15:10:00Z",
//       customer: {
//         customerId: "CUST-002",
//         name: "Bob Smith",
//         email: "bob.smith@example.com",
//         phone: "9808766542",
//       },
//       items: [
//         {
//           id: 2,
//           name: "Pepperoni Pizza",
//           price: 1200,
//           discount: 0,
//           quantity: 1,
//           description: "Pepperoni, cheese, and tomato sauce",
//           category: "non-veg",
//           image:
//             "https://plus.unsplash.com/premium_photo-1733259709671-9dbf22bf02cc?q=80&w=580&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//           availability: "available",
//         },
//         {
//           id: 5,
//           name: "Beef Taco",
//           price: 100,
//           discount: 5,
//           quantity: 10,
//           description: "Ground beef, lettuce, cheese, and salsa",
//           category: "non-veg",
//           image:
//             "https://plus.unsplash.com/premium_photo-1664391890333-b6708e34b021?q=80&w=729&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//           availability: "available",
//         },
//       ],
//       totalAmount: 2150,
//       status: "Waiting for Delivery",
//       deliveryman: {
//         deliverymanId: "DEL-1001",
//         name: "Ravi Kumar",
//         phone: "+1122334455",
//         vehicleType: "Bike",
//       },
//       deliveryRequestTime: "2025-08-08T15:15:00Z",
//       estimatedDeliveryTime: "2025-08-08T15:50:00Z",
//     },
//     {
//       orderId: "ORD-1003",
//       orderDate: "2025-08-08T16:00:00Z",
//       customer: {
//         customerId: "CUST-003",
//         name: "Catherine Lee",
//         email: "catherine.lee@example.com",
//         phone: "+1478523690",
//       },
//       items: [
//         {
//           id: 1,
//           name: "Margherita Pizza",
//           price: 1000,
//           discount: 0,
//           quantity: 1,
//           description: "Classic pizza with tomatoes, mozzarella, and basil",
//           category: "veg",
//           image:
//             "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?q=80&w=869&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
//           availability: "available",
//         },
//       ],
//       totalAmount: 1000,
//       status: "Delivered",
//       deliveryman: {
//         deliverymanId: "DEL-1001",
//         name: "Rajesh Hamal",
//         phone: "+1122334455",
//         vehicleType: "Bike",
//       },
//       deliveryRequestTime: "2025-08-08T15:15:00Z",
//       estimatedDeliveryTime: "2025-08-08T15:50:00Z",
//     },
//   ];

//   const orderWrapper = document.querySelector("#current-order-wrapper");
//   const emptyOrder = document.querySelector("#emptyorder");

//   function renderOrders() {
//     if (!orders.length) {
//       emptyOrder.style.display = "flex";
//       return;
//     } else {
//       emptyOrder.style.display = "none";
//     }

//     orders.forEach((order, index) => {
//       const orderCard = document.createElement("div");
//       orderCard.classList.add("order-card");
//       orderCard.innerHTML = `
//           <div class="order-summary">
//             <div>
//               <h4>Order ID: ${order.orderId}</h4>
//               <p>Customer: ${order.customer.name}</p>
//               <p>Total: NPR ${order.totalAmount}</p>
//               <p>Status: <strong>${order.status}</strong></p>
//             </div>
//             <div>
//               <button class="toggle-details">Details</button>
//               <button class="next-status">Next Status</button>
//               ${
//                 order.status === "Processing" && !order.deliveryman
//                   ? '<button class="request-delivery">Request Delivery</button>'
//                   : ""
//               }
//               ${
//                 order.deliveryman
//                   ? '<button class="track-delivery">Track</button>'
//                   : ""
//               }
//             </div>
//           </div>
//           <div class="order-details" style="display:none">
//             <h5>Order Items:</h5>
//             <ul>
//               ${order.items
//                 .map(
//                   (item) => `
//                 <li>
//                   <img src="${item.image}" width="50" height="50" />
//                   <span>${item.name} (x${item.quantity}) - NPR ${item.price}</span>
//                 </li>`
//                 )
//                 .join("")}
//             </ul>
//             <h5>Customer Details:</h5>
//             <p>Email: ${order.customer.email}</p>
//             <p>Phone: ${order.customer.phone}</p>
//           </div>
//         `;

//       // Toggle details
//       orderCard
//         .querySelector(".toggle-details")
//         .addEventListener("click", () => {
//           const detailBox = orderCard.querySelector(".order-details");
//           detailBox.style.display =
//             detailBox.style.display === "none" ? "block" : "none";
//         });

//       // Update status
//       orderCard.querySelector(".next-status").addEventListener("click", () => {
//         const statuses = [
//           "Order Received",
//           "Processing",
//           "Waiting for Delivery",
//           "In Delivery",
//           "Delivered",
//         ];
//         const currentIndex = statuses.indexOf(order.status);
//         if (currentIndex < statuses.length - 1) {
//           order.status = statuses[currentIndex + 1];
//           orderCard.querySelector(
//             ".order-summary p:nth-child(4) strong"
//           ).textContent = order.status;
//           if (order.status === "Waiting for Delivery") {
//             const btn = document.createElement("button");
//             btn.textContent = "Request Delivery";
//             btn.classList.add("request-delivery");
//             btn.addEventListener("click", () => {
//               requestDelivery(order);
//             });
//             orderCard
//               .querySelector(".order-summary div:last-child")
//               .appendChild(btn);
//           }
//         }
//       });

//       // Request Delivery
//       const requestBtn = orderCard.querySelector(".request-delivery");
//       if (requestBtn) {
//         requestBtn.addEventListener("click", () => {
//           requestDelivery(order);
//         });
//       }

//       // Track Delivery
//       const trackBtn = orderCard.querySelector(".track-delivery");
//       if (trackBtn) {
//         trackBtn.addEventListener("click", () => {
//           showTrackingPopup(order);
//         });
//       }

//       orderWrapper.appendChild(orderCard);
//     });
//   }

//   function requestDelivery(order) {
//     // Simulate assigning a deliveryman
//     order.deliveryman = {
//       deliverymanId: "DEL-999",
//       name: "Demo Rider",
//       phone: "9800000000",
//       vehicleType: "Bike",
//     };
//     alert("Delivery requested. Assigned to Demo Rider.");
//     location.reload();
//   }

//   function showTrackingPopup(order) {
//     const popup = document.createElement("div");
//     popup.classList.add("tracking-popup");
//     popup.innerHTML = `
//         <div class="tracking-content">
//           <h4>Tracking ${order.deliveryman.name}</h4>
//           <p>Deliveryman Phone: ${order.deliveryman.phone}</p>
//           <p>Tracking to: ${order.customer.name}</p>
//           <p><i>Simulated map view here...</i></p>
//           <button onclick="this.parentElement.parentElement.remove()">Close</button>
//         </div>
//       `;
//     document.body.appendChild(popup);
//   }

//   renderOrders();
// });

let socket = null ; 
const wsProtocol = location.protocol === 'https' ? 'wss':'ws';
const wsUrl = `${wsProtocol}://${location.host}/ws/socket-server/`;

document.addEventListener("DOMContentLoaded", () => {
  socket = new WebSocket(wsUrl);
  const orderWrapper = document.querySelector("#current-order-wrapper");
  const emptyOrder = document.querySelector("#emptyorder");
  const resid = document.querySelector(".resid").id;
  console.log("resid:",resid);
    let orders = [];

    async function getCurrentOrders(){
      try{
        const response = await fetch(`http://127.0.0.1:8000/json/restaurant-orders-response/${resid}`);
        const {data} = await response.json();
        console.log("response:",data);
        orders = [...data];
      } catch(err){
        console.error("error: ",err);
        showError({message:`${err?.message}`});
      }
    }
    getCurrentOrders();
    renderOrders();

  // const orders = [
  //   {
  //     orderId: "ORD-1001",
  //     orderDate: "2025-08-08T14:30:00Z",
  //     customer: {
  //       customerId: "CUST-001",
  //       name: "Alice Johnson",
  //       email: "alice.johnson@example.com",
  //       phone: "9876543211",
  //     },
  //     items: [
  //       {
  //         id: 1,
  //         name: "Margherita Pizza",
  //         price: 1000,
  //         discount: 0,
  //         quantity: 1,
  //         description: "Classic pizza with tomatoes, mozzarella, and basil",
  //         category: "veg",
  //         image:
  //           "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?q=80&w=869&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  //         availability: "available",
  //       },
  //       {
  //         id: 3,
  //         name: "California Roll",
  //         price: 800,
  //         discount: 10,
  //         quantity: 2,
  //         description: "Crab, avocado, and cucumber",
  //         category: "non-veg",
  //         image:
  //           "https://images.unsplash.com/photo-1559410545-0bdcd187e0a6?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  //         availability: "available",
  //       },
  //     ],
  //     totalAmount: 2440,
  //     status: "Processing",
  //     deliveryman: null,
  //     deliveryRequestTime: null,
  //     estimatedDeliveryTime: null,
  //   },
  //   {
  //     orderId: "ORD-1002",
  //     orderDate: "2025-08-08T15:10:00Z",
  //     customer: {
  //       customerId: "CUST-002",
  //       name: "Bob Smith",
  //       email: "bob.smith@example.com",
  //       phone: "9808766542",
  //     },
  //     items: [
  //       {
  //         id: 2,
  //         name: "Pepperoni Pizza",
  //         price: 1200,
  //         discount: 0,
  //         quantity: 1,
  //         description: "Pepperoni, cheese, and tomato sauce",
  //         category: "non-veg",
  //         image:
  //           "https://plus.unsplash.com/premium_photo-1733259709671-9dbf22bf02cc?q=80&w=580&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  //         availability: "available",
  //       },
  //       {
  //         id: 5,
  //         name: "Beef Taco",
  //         price: 100,
  //         discount: 5,
  //         quantity: 10,
  //         description: "Ground beef, lettuce, cheese, and salsa",
  //         category: "non-veg",
  //         image:
  //           "https://plus.unsplash.com/premium_photo-1664391890333-b6708e34b021?q=80&w=729&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  //         availability: "available",
  //       },
  //     ],
  //     totalAmount: 2150,
  //     status: "Waiting for Delivery",
  //     deliveryman: {
  //       deliverymanId: "DEL-1001",
  //       name: "Ravi Kumar",
  //       phone: "+1122334455",
  //       vehicleType: "Bike",
  //     },
  //     deliveryRequestTime: "2025-08-08T15:15:00Z",
  //     estimatedDeliveryTime: "2025-08-08T15:50:00Z",
  //   },
  //   {
  //     orderId: "ORD-1003",
  //     orderDate: "2025-08-08T16:00:00Z",
  //     customer: {
  //       customerId: "CUST-003",
  //       name: "Catherine Lee",
  //       email: "catherine.lee@example.com",
  //       phone: "+1478523690",
  //     },
  //     items: [
  //       {
  //         id: 1,
  //         name: "Margherita Pizza",
  //         price: 1000,
  //         discount: 0,
  //         quantity: 1,
  //         description: "Classic pizza with tomatoes, mozzarella, and basil",
  //         category: "veg",
  //         image:
  //           "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?q=80&w=869&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
  //         availability: "available",
  //       },
  //     ],
  //     totalAmount: 1000,
  //     status: "Delivered",
  //     deliveryman: {
  //       deliverymanId: "DEL-1001",
  //       name: "Rajesh Hamal",
  //       phone: "+1122334455",
  //       vehicleType: "Bike",
  //     },
  //     deliveryRequestTime: "2025-08-08T15:15:00Z",
  //     estimatedDeliveryTime: "2025-08-08T15:50:00Z",
  //   },
  // ];

  // Listen to new order push from WebSocket
  
  socket.addEventListener("message", (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === "status") {
    console.log("Server status:", msg.status);
    return; 
  }

  if (msg.type === "chat_message") {
    console.log("New order received:", msg.data);
    orders.unshift(msg.order);
    orderWrapper.innerHTML = "";
    renderOrders();
  }
  });

  function renderOrders() {
    let len = orders.length;
    console.log("orderlen:",len);
    if (!orders.length) {
      emptyOrder.style.display = "flex";
      return;
    }
    emptyOrder.style.display = "none";

    orderWrapper.innerHTML = "";

    orders.forEach((order) => {
      const orderCard = document.createElement("div");
      orderCard.classList.add("order-card");

      const showRequestDeliveryBtn =
        order.status === "Waiting for Delivery" && !order.deliveryman;

      orderCard.innerHTML = `
          <div class="order-summary">
            <div>
              <h4>Order ID: ${order.orderId}</h4>
              <p>Customer: ${order.customer.name}</p>
              <p>Total: NPR ${order.totalAmount}</p>
              <p>Status: <strong>${order.status}</strong></p>
            </div>
            <div>
              <button class="toggle-details">Details</button>
              ${
                order.status === "Order Received" ||
                order.status === "Processing"
                  ? '<button class="next-status">Next Status</button>'
                  : ""
              }
              ${
                showRequestDeliveryBtn
                  ? '<button class="request-delivery">Request Delivery</button>'
                  : ""
              }
              ${
                order.status === "Out for Delivery"
                  ? '<button class="track-delivery">Track</button>'
                  : ""
              }
            </div>
          </div>
          <div class="order-details" style="display:none">
            <h5>Order Items:</h5>
            <ul>
              ${order.items
                .map(
                  (item) => `
                <li>
                  <img src="${item.image}" width="50" height="50" />
                  <span>${item.name} (x${item.quantity}) - NPR ${item.price}</span>
                </li>`
                )
                .join("")}
            </ul>
            <h5>Customer Details:</h5>
            <p>Email: ${order.customer.email}</p>
            <p>Phone: ${order.customer.phone}</p>
            <p>Location: (${order.customer.lat}, ${order.customer.lng})</p>
          </div>
        `;

      // Toggle details
      orderCard
        .querySelector(".toggle-details")
        .addEventListener("click", () => {
          const detailBox = orderCard.querySelector(".order-details");
          detailBox.style.display =
            detailBox.style.display === "none" ? "block" : "none";
        });

      // Update status (merchant allowed only up to Waiting for Delivery)
      const statusBtn = orderCard.querySelector(".next-status");
      if (statusBtn) {
        statusBtn.addEventListener("click", async () => {
          const allowedStatuses = [
            "Order Received",
            "Processing",
            "Waiting for Delivery",
          ];
          const nextStatus =
            allowedStatuses[allowedStatuses.indexOf(order.status) + 1];
          if (nextStatus) {
            const res = await fetch(
              `https://your-backend.com/api/merchant/order/${order.orderId}/status`,
              {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ status: nextStatus }),
              }
            );
            if (res.ok) {
              order.status = nextStatus;
              renderOrders();
            }
          }
        });
      }

      // Request Delivery (will forward to all deliverymen)
      const reqBtn = orderCard.querySelector(".request-delivery");
      if (reqBtn) {
        reqBtn.addEventListener("click", async () => {
          const res = await fetch(
            `https://your-backend.com/api/merchant/order/${order.orderId}/request-delivery`,
            {
              method: "POST",
            }
          );
          if (res.ok) {
            alert("Delivery request sent. Awaiting acceptance...");
          }
        });
      }

      // Show map for delivery tracking
      const trackBtn = orderCard.querySelector(".track-delivery");
      if (trackBtn) {
        trackBtn.addEventListener("click", () => showTrackingPopup(order));
      }

      orderWrapper.appendChild(orderCard);
    });
  }

  function showTrackingPopup(order) {
    const popup = document.createElement("div");
    popup.classList.add("tracking-popup");
    popup.innerHTML = `
        <div class="tracking-content">
          <h4>Tracking Delivery</h4>
          <div id="map" style="height: 300px;"></div>
          <button onclick="this.parentElement.parentElement.remove()">Close</button>
        </div>
      `;
    document.body.appendChild(popup);

    const map = L.map("map").setView(
      [order.customer.lat, order.customer.lng],
      13
    );

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: "&copy; OpenStreetMap contributors",
    }).addTo(map);

    L.marker([order.customer.lat, order.customer.lng])
      .addTo(map)
      .bindPopup("Customer Location")
      .openPopup();

    if (order.deliverymanLocation) {
      L.marker([order.deliverymanLocation.lat, order.deliverymanLocation.lng], {
        icon: redIcon,
      })
        .addTo(map)
        .bindPopup("Deliveryman");
    }

    if (order.merchantLocation) {
      L.marker([order.merchantLocation.lat, order.merchantLocation.lng], {
        icon: blueIcon,
      })
        .addTo(map)
        .bindPopup("Restaurant");
    }
  }

  const redIcon = new L.Icon({
    iconUrl: "https://maps.google.com/mapfiles/ms/icons/red-dot.png",
    iconSize: [32, 32],
  });

  const blueIcon = new L.Icon({
    iconUrl: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png",
    iconSize: [32, 32],
  });
});
