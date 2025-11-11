
document.addEventListener("DOMContentLoaded", () => {
  console.log("csrf:",csrftoken);
  const orderWrapper = document.querySelector("#current-order-wrapper");
  const emptyOrder = document.querySelector("#emptyorder");
  const resid = document.querySelector(".resid").id;
  console.log("resid:", resid);
  let orders = [];

  async function getCurrentOrders() {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/json/restaurant-orders-response/${resid}`
      );
      const { data } = await response.json();
      console.log("response:", data);
      data.forEach((item)=> orders.unshift(item));
    } catch (err) {
      console.error("error: ", err);
      showError({ message: `${err?.message}` });
    }
  }
  getCurrentOrders();

  setTimeout(()=>{
      if(orders && orders.length>0){
    renderOrders();
  }
  },1000);

  // ws.addEventListener("message", (event) => {
  //   const msg = JSON.parse(event.data);
  //   if (msg.type === "status") {
  //     console.log("Server status:", msg.status);
  //     return;
  //   }

  //   if (msg.type === "chat_message") {
  //     console.log("New order received:", msg.data);
  //     orders.unshift(msg.order);
  //     orderWrapper.innerHTML = "";
  //     renderOrders();
  //   }
  // });

  function renderOrders() {
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
        order.status === "PROCESSING" && !order.deliveryman;

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
                order.status === "PENDING" 
                  ? '<button class="next-status">Next Status</button>'
                  : ""
              }
              ${
                showRequestDeliveryBtn
                  ? '<button class="request-delivery">Request Delivery</button>' 
                  : ""
              }
              ${
                order.status === "OUT_FOR_DELIVERY"
                  ? '<button class="track-delivery">Track</button>' // TRACK HANDLER ADD GARNA BAKI
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
            <p>Phone: ${order.customer_details.phone_number}</p></div>
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
      const statusBtn = orderCard.querySelector(".next-status");
      if (statusBtn) {
        statusBtn.addEventListener("click", async () => {
          const allowedStatuses = [
            "PENDING",
            "PROCESSING",
          ];
          const nextStatus =
            allowedStatuses[allowedStatuses.indexOf(order.status) + 1];
          if (nextStatus) {
            try{
               const res = await fetch(
              `http://127.0.0.1:8000/api/update-order-status/`,
              {
                method: "POST",
                headers: { "Content-Type": "application/json","X-CSRFToken": csrftoken },
                body: JSON.stringify({ status: nextStatus, order_id: order.order_id }),
                credentials: "include"
              }
            );
            if (res.ok) {
              order.status = nextStatus;
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
