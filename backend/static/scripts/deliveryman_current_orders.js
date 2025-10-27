const deliveries = [];
let mapInstances = {};
let locationWatchId = null;

registerWSHandler('assign_order', handleAssignOrder);
registerWSHandler('delivery_update', handleDeliveryUpdate);

function handleAssignOrder(order) {
  if (deliveries.some(d => d.id === order.id)) return;
  order.status = 'in_progress';
  deliveries.unshift(order);
  renderDeliveries();
}

function handleDeliveryUpdate(update) {
  const d = deliveries.find(x => x.id === update.id);
  if (d) {
    d.status = update.status;
    renderDeliveries();
  }
}

function renderDeliveries() {
  const container = document.querySelector('.delivery-list');
  if (!container) return;
  container.innerHTML = '';

  const active = deliveries.filter(d => d.status !== 'delivered' && d.status !== 'cancelled');
  if (active.length === 0) {
    container.innerHTML = `<p id="noneworder"><span><i class="fa-solid fa-circle-xmark"></i></span> No new orders at the moment. </p>`;
    return;
  }

  active.forEach(delivery => {
    const div = document.createElement('div');
    div.className = 'delivery-card';
    let actions = '';

    if (delivery.status === 'waiting_for_delivery') {
      actions = `
        <button class="btn-status" data-id="${delivery.id}">Change Stauts</button>
        <button class="btn-cancel" data-id="${delivery.id}">Cancel</button>
      `;
    } else if (delivery.status === 'out_for_delivery') {
      actions = `
        <button class="btn-delivered" data-id="${delivery.id}">Mark Delivered</button>
        <button class="btn-map" data-id="${delivery.id}">View Map</button>
      `;
    }
    div.innerHTML = `
      <h3>Order #${delivery.id}</h3>
      <p><strong>Customer:</strong> ${delivery.customer}</p>
      <p><strong>Address:</strong> ${delivery.address}</p>
      <p><strong>Items:</strong> ${delivery.items}</p>
      <div class="delivery-actions">${actions}</div>
      <div id="map-${delivery.id}" class="map-container"></div>
    `;
    container.appendChild(div);
  });
  bindDeliveryButtons();
}

function bindDeliveryButtons() {
  document.querySelectorAll('.btn-status').forEach(btn => {
    btn.onclick = () => changeStatus(parseInt(btn.dataset.id));
  });
  document.querySelectorAll('.btn-delivered').forEach(btn => {
    btn.onclick = () => sendDeliveryAction('delivered', parseInt(btn.dataset.id));
  });
  document.querySelectorAll('.btn-cancel').forEach(btn => {
    btn.onclick = () => sendDeliveryAction('cancelled', parseInt(btn.dataset.id));
  });
  document.querySelectorAll('.btn-map').forEach(btn => {
    btn.onclick = () => toggleMap(parseInt(btn.dataset.id));
  });
}

function sendDeliveryAction(action, id) {
  const delivery = deliveries.find(d => d.id === id);
  if (!delivery) return;
  delivery.status = action;
  renderDeliveries();
sendWSMessage('delivery_action',{id,status: action})
  if (action === 'delivered' && locationWatchId) {
    navigator.geolocation.clearWatch(locationWatchId);
    locationWatchId = null;
  }
}

function changeStatus(id) {
  const delivery = deliveries.find(d => d.id === id);
  if (!delivery) return;
  delivery.status = 'out_for_delivery';
  renderDeliveries();
sendWSMessage('delivery_action',{ id, status: 'out_for_delivery' } );
  startLocationSharing(id);
}

function toggleMap(id) {
  const mapDiv = document.getElementById(`map-${id}`);
  if (!mapDiv) return;
  if (mapDiv.style.display === 'none') {
    mapDiv.style.display = 'block';
    initMap(id, mapDiv);
  } else {
    mapDiv.style.display = 'none';
  }
}

function initMap(id, container) {
  if (mapInstances[id]) return;
  const delivery = deliveries.find(d => d.id === id);
  if (!delivery) return;

  const map = L.map(container).setView([delivery.customerLat, delivery.customerLng], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);

  if (delivery.restaurantLat && delivery.restaurantLng) {
    L.marker([delivery.restaurantLat, delivery.restaurantLng]).addTo(map).bindPopup('Restaurant');
  }
  if (delivery.customerLat && delivery.customerLng) {
    L.marker([delivery.customerLat, delivery.customerLng]).addTo(map).bindPopup('Customer');
  }
  
  mapInstances[id] = map;
}

function startLocationSharing(orderId) {
  if (!navigator.geolocation) return;
  locationWatchId = navigator.geolocation.watchPosition(pos => {
    const { latitude, longitude } = pos.coords;
    sendWSMessage('location_update',{ orderId, lat: latitude, lng: longitude })

    // deliveryman ko position update garne map ma
    const map = mapInstances[orderId];
    if (map) {
      if (!map.deliverymanMarker) {
        map.deliverymanMarker = L.marker([latitude, longitude], { color: 'blue' }).addTo(map).bindPopup('You');
      } else {
        map.deliverymanMarker.setLatLng([latitude, longitude]);
      }
    }
  });
}

window.addEventListener('DOMContentLoaded', () => {
  renderDeliveries();
});


// /---------------- tala ko simple simulation ------------------------------/
// const deliveries = [
//   {
//     id: 1,
//     customer: "Sita Rai",
//     address: "Patan, Lalitpur",
//     items: "Burger, Coke",
//     phone_number : 9876543210,
//     time: "2 min ago",
//     status: "waiting_for_delivery"
//   },
//   {
//     id: 2,
//     customer: "Ramesh Shrestha",
//     address: "Baneshwor",
//     items: "Pizza",
//     phone_number : 9876543210,
//     time: "5 min ago",
//     status: "waiting_for_delivery"
//   },
// ];

// document.addEventListener("DOMContentLoaded", () => renderDeliveries());

// function renderDeliveries() {
//   const container = document.querySelector('.delivery-list');
//   if (!container) return;
//   container.innerHTML = '';

//   const active = deliveries.filter(d => d.status !== 'delivered' && d.status !== 'cancelled');
//   console.log("active:",active);
//   if (active.length === 0) {
//     container.innerHTML = `<p id="noneworder"><span><i class="fa-solid fa-circle-xmark"></i></span> No new orders at the moment. </p>`;
//     return;
//   }

//   active.forEach(delivery => {
//     const div = document.createElement('div');
//     div.className = 'delivery-card';
//     let actions = '';

//     if (delivery.status === 'waiting_for_delivery') {
//       actions = `
//         <button class="btn-status" data-id="${delivery.id}">Change Status</button>
//         <button class="btn-cancel" data-id="${delivery.id}">Cancel</button>
//       `;
//     } else if (delivery.status === 'out_for_delivery') {
//       actions = `
//         <button class="btn-delivered" data-id="${delivery.id}">Mark Delivered</button>
//         <button class="btn-map" data-id="${delivery.id}">View Map</button>
//       `;
//     }
//     div.innerHTML = `
//       <h3>Order #${delivery.id}</h3>
//       <p><strong>Customer:</strong> ${delivery.customer}</p>
//       <p><strong>Address:</strong> ${delivery.address}</p>
//       <p><strong>Phone number:</strong> ${delivery.phone_number}</p>
//       <div class="delivery-actions">${actions}</div>
//       <div id="map-${delivery.id}" class="map-container"></div>
//     `;
//     container.appendChild(div);
//   });
// }


