
document.addEventListener('DOMContentLoaded',()=>{
  const newDeliveryRequest= [];

  if(window.registerWSHandler){
    window.registerWSHandler("deliveryRequestHandler" , (msg)=>{
      console.log("msg:",msg);
     if (msg.type === "chat") {
            try{
              setTimeout(() => {
              if (window.resetDeliveryCount) {
              window.resetDeliveryCount();
            }
          }, 1000);
               console.log("new delivery request received");
              console.log("New delivery request received:", msg.data);
              newDeliveryRequest.unshift(...msg.data);
              orderWrapper.innerHTML = "";
              renderOrders();
            } catch(err){
              console.error("error:",err);
            }
          }

    })
  }

  function renderOrders() {
    if (!newDeliveryRequest.length) {
      emptyOrder.style.display = "flex";
      return;
    }
    emptyOrder.style.display = "none";

    orderWrapper.innerHTML = "";

    newDeliveryRequest.forEach((order) => {
      const orderCard = document.createElement("div");
      orderCard.classList.add("order-card");

      const showRequestDeliveryBtn =
        order.status === "WAITING_FOR_DELIVERY" && !order.deliveryman;

      const mapDivId = `userlocmap-${order.order_id}`;

      orderCard.innerHTML = `
          <div class="order-summary">
            <div>
              <h4>Order ID: ${order.order_id}</h4>
              <p>Customer: ${order.user.first_name}</p>
              <p>Total: NPR ${order.total_price}</p>
              <p>Status: <strong>${order.status}</strong></p>
            </div>
            <div>
              <button class="toggle-details">Details</button>
              ${
                order.status === "WAITING_FOR_DELIVERY" 
                  ? '<button class="accept_request">Accept Request</button>'
                  : ""
              }
            </div>
          </div>
          <div class="order-details">
          <div><h4>Order Items:</h4>
            <ul>
              ${order.order_items
                .map(
                  (item) => `
                <li>
                  <img src="${item.food_item_image}" width="50" height="50" />
                  <span>${item.food_item_name} (x${item.quantity}) - NPR ${item.total_price}</span>
                </li>`
                )
                .join("")}
            </ul>
            <h4>Customer Details:</h4>
            <p>Email: ${order.user.email}</p>
            <p>Phone: ${order.customer_details.phone}</p></div>
            <div><h4>Delivery Location: (${order.latitude}, ${order.longitude})</h4>
            <div id="${mapDivId}" style="height: 200px; width: 400px;"></div>
            </div>
          </div>
        `;

      // Toggle details
       orderCard
        .querySelector(".toggle-details")
        .addEventListener("click", () => {
          const detailBox = orderCard.querySelector(".order-details");
          if (detailBox.style.display === "none") {
            detailBox.style.display = "flex";

            if (!detailBox.dataset.mapInitialized) {
              const map = L.map(mapDivId, {
                boxZoom: false,
                keyboard: false,
                tap: false,
              }).setView([order.latitude, order.longitude], 15);

              L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                maxZoom: 19,
                attribution: "&copy; OpenStreetMap contributors",
              }).addTo(map);

              L.marker([order.latitude, order.longitude], { draggable: false })
                .addTo(map)
                .bindPopup("Customer Location")
                .openPopup();

              detailBox.dataset.mapInitialized = true;
            }
          } else {
            detailBox.style.display = "none";
          }
        });

      // Update status (merchant allowed only up to Waiting for Delivery)
      const statusBtn = orderCard.querySelector(".accept_request");
      if (statusBtn) {
        statusBtn.addEventListener("click", async () => {
         
          if (window.confirm("Do you want to accept the order?")) {
            try{
               const res = await fetch(
              `http://127.0.0.1:8000/api/update-order-status/`,
              {
                method: "POST",
                headers: { "Content-Type": "application/json","X-CSRFToken": csrftoken },
                body: JSON.stringify({ order_id: order.order_id }),
                credentials: "include"
              }
            );
            if (res.ok) {
              order.status = "";
              renderOrders();
            }
            } catch(err){
              console.error("error when updating status in server");
            }
          }
        });
      }

      // Request Delivery (will forward to all deliverymen)
      const reqBtn = orderCard.querySelector(".request-delivery");
      if (reqBtn) {
        reqBtn.addEventListener("click", async () => {
          try{
             const res = await fetch(
            `http://127.0.0.1:8000/api/request-delivery/${order.orderId}/`,
            {
              method: "POST",
            }
          );
          if (res.ok) {
            order.status = "WAITING_FOR_DELIVERY";
            alert("Delivery request sent. Awaiting acceptance...");
            renderOrders();
          }
          } catch(err){
            console.error("error when requesting for deliveryman");
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


})


// registerWSHandler('new_order', handleNewOrder);
// registerWSHandler('order_update', handleOrderUpdate);

// function handleNewOrder(order) {
//   if (orders.some(o => o.id === order.id)) return;
//   order.status = 'pending';
//   orders.unshift(order);
//   renderOrders();
//   showNotification();
//   document.title = `🔔 New Order #${order.id}`;
// }

// function handleOrderUpdate(update) {
//   const o = orders.find(x => x.id === update.id);
//   if (o) {
//     o.status = update.status;
//     renderOrders();
//   }
// }

// function bindButtons() {
//   document.querySelectorAll('.accept-btn').forEach(btn => {
//     btn.onclick = () => sendAction('accept_order', parseInt(btn.dataset.id));
//   });
//   document.querySelectorAll('.decline-btn').forEach(btn => {
//     btn.onclick = () => sendAction('decline_order', parseInt(btn.dataset.id));
//   });
// }

// function sendAction(action, id) {
//   const order = orders.find(o => o.id === id);
//   if (!order) return;
//   order.status = action === 'accept_order' ? 'accepted' : 'declined';
//   renderOrders();
//   sendWSMessage(action,{id});
// }



// /---------------- tala ko simple simulation ------------------------------/
// const orders = [
//   {
//     id: 1,
//     customer: "Sita Rai",
//     address: "Patan, Lalitpur",
//     items: "Burger, Coke",
//     phone_number : 9876543210,
//     time: "2 min ago",
//   },
//   {
//     id: 2,
//     customer: "Ramesh Shrestha",
//     address: "Baneshwor",
//     items: "Pizza",
//     phone_number : 9876543210,
//     time: "5 min ago",
//   },
// ];

// document.addEventListener("DOMContentLoaded", () => renderOrders());

// function renderOrders() {
//   const container = document.querySelector(".order-list");
//   container.innerHTML = "";
//   if(orders.length === 0){
//     container.innerHTML = `<p id="noneworder"><span><i class="fa-solid fa-circle-xmark"></i></span> No new orders at the moment. </p>`;
//     return;
//   }
//   orders.forEach((order) => {
//     if(order.status === "accepted") return;
//     const div = document.createElement("div");
//     div.className = "summary-card";
//     div.innerHTML = `
//       <h3>Order #${order.id}</h3>
//       <p><strong>Customer:</strong> ${order.customer}</p>
//       <p><strong>Address:</strong> ${order.address}</p>
//       <p><strong>Phone number:</strong> ${order.phone_number}</p>
//       <p><em>${order.time}</em></p>
//       <div class="order-actions">
//         <button class="accept-btn" data-id="${order.id}">Accept</button>
//         <button class="cancel-btn" data-id="${order.id}">Cancel</button>
//       </div>
//     `;
//     container.appendChild(div);
//   });
//   bindAcceptButtons();
// }

// function bindAcceptButtons(){
//     const buttons = document.querySelectorAll(".accept-btn");
//     buttons.forEach((btn)=>{
//         btn.addEventListener('click',(e)=>{
//             const id = parseInt(btn.getAttribute("data-id"));
//             acceptOrder(id);
//         })
//     })
// }

// function acceptOrder(id) {
//     const order = orders.find(o => o.id === id);
//     if(order){
//         order.status = "accepted";
//         alert(`You accepted Order #${id} for ${order.customer}`);
//         renderOrders();
//     }
// }

// setTimeout(() => {
//   const newOrder = {
//     id: 3,
//     customer: "Laxmi Thapa",
//     address: "Jawalakhel",
//     items: "Momo",
//     time: "Just now",
//   };
//   orders.push(newOrder);
//   renderOrders();

//   showNotification();

//   document.getElementById("new-order-count").textContent = orders.length;
//   document.title = "🔔 New Order! | GrubMate";
// }, 3000);

