// const deliveries = [];
// let mapInstances = {};
// let locationWatchId = null;

// registerWSHandler('assign_order', handleAssignOrder);
// registerWSHandler('delivery_update', handleDeliveryUpdate);

// function handleAssignOrder(order) {
//   if (deliveries.some(d => d.id === order.id)) return;
//   order.status = 'in_progress';
//   deliveries.unshift(order);
//   renderDeliveries();
// }

// function handleDeliveryUpdate(update) {
//   const d = deliveries.find(x => x.id === update.id);
//   if (d) {
//     d.status = update.status;
//     renderDeliveries();
//   }
// }

// function renderDeliveries() {
//   const container = document.querySelector('.delivery-list');
//   if (!container) return;
//   container.innerHTML = '';

//   const active = deliveries.filter(d => d.status !== 'delivered' && d.status !== 'cancelled');
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
//         <button class="btn-status" data-id="${delivery.id}">Change Stauts</button>
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
//       <p><strong>Items:</strong> ${delivery.items}</p>
//       <div class="delivery-actions">${actions}</div>
//       <div id="map-${delivery.id}" class="map-container"></div>
//     `;
//     container.appendChild(div);
//   });
//   bindDeliveryButtons();
// }

// function bindDeliveryButtons() {
//   document.querySelectorAll('.btn-status').forEach(btn => {
//     btn.onclick = () => changeStatus(parseInt(btn.dataset.id));
//   });
//   document.querySelectorAll('.btn-delivered').forEach(btn => {
//     btn.onclick = () => sendDeliveryAction('delivered', parseInt(btn.dataset.id));
//   });
//   document.querySelectorAll('.btn-cancel').forEach(btn => {
//     btn.onclick = () => sendDeliveryAction('cancelled', parseInt(btn.dataset.id));
//   });
//   document.querySelectorAll('.btn-map').forEach(btn => {
//     btn.onclick = () => toggleMap(parseInt(btn.dataset.id));
//   });
// }

// function sendDeliveryAction(action, id) {
//   const delivery = deliveries.find(d => d.id === id);
//   if (!delivery) return;
//   delivery.status = action;
//   renderDeliveries();
// sendWSMessage('delivery_action',{id,status: action})
//   if (action === 'delivered' && locationWatchId) {
//     navigator.geolocation.clearWatch(locationWatchId);
//     locationWatchId = null;
//   }
// }

// function changeStatus(id) {
//   const delivery = deliveries.find(d => d.id === id);
//   if (!delivery) return;
//   delivery.status = 'out_for_delivery';
//   renderDeliveries();
// sendWSMessage('delivery_action',{ id, status: 'out_for_delivery' } );
//   startLocationSharing(id);
// }

// function toggleMap(id) {
//   const mapDiv = document.getElementById(`map-${id}`);
//   if (!mapDiv) return;
//   if (mapDiv.style.display === 'none') {
//     mapDiv.style.display = 'block';
//     initMap(id, mapDiv);
//   } else {
//     mapDiv.style.display = 'none';
//   }
// }

// function initMap(id, container) {
//   if (mapInstances[id]) return;
//   const delivery = deliveries.find(d => d.id === id);
//   if (!delivery) return;

//   const map = L.map(container).setView([delivery.customerLat, delivery.customerLng], 13);
//   L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);

//   if (delivery.restaurantLat && delivery.restaurantLng) {
//     L.marker([delivery.restaurantLat, delivery.restaurantLng]).addTo(map).bindPopup('Restaurant');
//   }
//   if (delivery.customerLat && delivery.customerLng) {
//     L.marker([delivery.customerLat, delivery.customerLng]).addTo(map).bindPopup('Customer');
//   }
  
//   mapInstances[id] = map;
// }

// function startLocationSharing(orderId) {
//   if (!navigator.geolocation) return;
//   locationWatchId = navigator.geolocation.watchPosition(pos => {
//     const { latitude, longitude } = pos.coords;
//     sendWSMessage('location_update',{ orderId, lat: latitude, lng: longitude })

//     // deliveryman ko position update garne map ma
//     const map = mapInstances[orderId];
//     if (map) {
//       if (!map.deliverymanMarker) {
//         map.deliverymanMarker = L.marker([latitude, longitude], { color: 'blue' }).addTo(map).bindPopup('You');
//       } else {
//         map.deliverymanMarker.setLatLng([latitude, longitude]);
//       }
//     }
//   });
// }

// window.addEventListener('DOMContentLoaded', () => {
//   renderDeliveries();
// });

// /json/deliveryman-current-delivery/
document.addEventListener("DOMContentLoaded",()=>{
  let delman_lat;
  let delman_lng;
  let delman_acc;
  const currentDeliveries = [];
  let isassigned = null;

  const mapContainer = document.querySelector("#map-container");
  const mapBox = document.querySelector("#map"); 
  const mapErrContainer = document.querySelector("#map-error");


    async function getCurrentDeliveries() {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/json/deliveryman-current-delivery/`,
        {
          credentials:"include"
        }
      );
    
      const data = await response.json();
      console.log("data:", data);
      const {has_current_assignments,orders} = data;
      isassigned = has_current_assignments;
      if(orders && orders.length>0){
        orders.forEach((item)=> currentDeliveries.push(item));
      }
    } catch (err) {
      console.error("error: ", err);
      showError({ message: `${err?.message}` });
    }
  }

  getCurrentDeliveries();

   setTimeout(()=>{
    renderDeliveries();
  },500);

  function renderDeliveries(){
    if(!currentDeliveries.length && !isassigned){
      mapErrContainer.classList.remove("hidden");
      mapErrContainer.style.display = "flex";
      mapBox.style.display = "none";
       mapErrContainer.innerHTML = `
        <div>
          <p>
            <span><i class="fa-solid fa-triangle-exclamation"></i></span>
            <span>You havenot taken any delivery at the moment.</span> 
          </p>
        </div>
      `;
      return;
    }
     mapErrContainer.classList.add("hidden");
      mapErrContainer.style.display = "none";
      mapBox.style.display = "inline-block";

      if(navigator.geolocation){
  navigator.geolocation.getCurrentPosition((pos)=>{
    console.log(pos);
    const {accuracy,latitude,longitude} = pos.coords;
    delman_lat = latitude;
    delman_lng = longitude;
    delman_acc = accuracy;
    initMap();
  },
  (err)=>{
    console.error("error:",err);
      mapErrContainer.classList.remove("hidden");
      mapErrContainer.style.display = "flex";
      mapBox.style.display = "none";
       let message = "";

      if (err.code === err.PERMISSION_DENIED) {
        message = "Location permission denied. Please allow access to use the map.";
      } else if (err.code === err.POSITION_UNAVAILABLE) {
        message = "Location unavailable. Try again outdoors or check GPS.";
      } else if (err.code === err.TIMEOUT) {
        message = "Location request timed out. Please try again.";
      } else {
        message = "An unknown error occurred while loading the map.";
      }
      mapErrContainer.innerHTML = `
        <div>
          <p>
            <span><i class="fa-solid fa-triangle-exclamation"></i></span>
            <span>${message}</span> 
          </p>
        </div>
      `;
  },
 {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0,
    })
} else {
  mapErrContainer.classList.remove("hidden");
  mapErrContainer.style.display = "flex";
  mapBox.style.display = "none";
  mapErrContainer.innerHTML = `
    <div>
      <p>
        <span><i class="fa-solid fa-triangle-exclamation"></i></span>
        <span>Your device does not support geolocation.</span>
      </p>
    </div>
  `;
}

function initMap(){
   const osmLight = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                maxZoom: 19,
                attribution: "&copy; OpenStreetMap contributors",
              });

  const osmDark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { 
            	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a hre f="https://carto.com/attributions">CARTO</a>',
            	subdomains: 'abcd', 
            	maxZoom: 20 
            }); 

const map = L.map("map",{
  center:[delman_lat,delman_lng],
  zoom:10,
  layers: [osmLight]
})
if(!map) return;
 const baseLayersGrp = {
      "Light mode": osmLight,
      "Dark mode": osmDark
    }
        
    const layersControl = L.control.layers(baseLayersGrp);
    layersControl.addTo(map);

     L.circle([delman_lat, delman_lng], {
        radius: delman_acc,
        color: "#136AEC",
        fillColor: "#136AEC",
        fillOpacity: 0.15
   }).addTo(map);

     L.Routing.control({
            waypoints: [
            L.latLng(delman_lat,delman_lng),
            L.latLng([27.66445,85.433875])
              ],
              createMarker: function(i,waypoint,n){
                const marker = L.marker(waypoint.latLng);
                if(i===0){
                  marker.bindPopup("Your Location").openPopup();
                } else if(i===1){
                  marker.bindPopup("Restaurant Location").openPopup();
                }
                return marker;
              }
            }).addTo(map);

}


  }


})



// let delman_lat;
// let delman_lng;
// let delman_acc;

// const mapContainer = document.querySelector("#map-container");
// const mapBox = document.querySelector("#map");
// const mapErrContainer = document.querySelector("#map-error");

// if(navigator.geolocation){
//   navigator.geolocation.getCurrentPosition((pos)=>{
//     console.log(pos);
//     const {accuracy,latitude,longitude} = pos.coords;
//     delman_lat = latitude;
//     delman_lng = longitude;
//     delman_acc = accuracy;
//     initMap();
//   },
//   (err)=>{
//     console.error("error:",err);
//       mapErrContainer.classList.remove("hidden");
//       mapErrContainer.style.display = "flex";
//       mapBox.style.display = "none";
//        let message = "";

//       if (err.code === err.PERMISSION_DENIED) {
//         message = "Location permission denied. Please allow access to use the map.";
//       } else if (err.code === err.POSITION_UNAVAILABLE) {
//         message = "Location unavailable. Try again outdoors or check GPS.";
//       } else if (err.code === err.TIMEOUT) {
//         message = "Location request timed out. Please try again.";
//       } else {
//         message = "An unknown error occurred while loading the map.";
//       }
//       mapErrContainer.innerHTML = `
//         <div>
//           <p>
//             <span><i class="fa-solid fa-triangle-exclamation"></i></span>
//             <span>${message}</span> 
//           </p>
//         </div>
//       `;
//   },
//  {
//       enableHighAccuracy: true,
//       timeout: 10000,
//       maximumAge: 0,
//     })
// } else {
//   mapErrContainer.classList.remove("hidden");
//   mapErrContainer.style.display = "flex";
//   mapBox.style.display = "none";
//   mapErrContainer.innerHTML = `
//     <div>
//       <p>
//         <span><i class="fa-solid fa-triangle-exclamation"></i></span>
//         <span>Your device does not support geolocation.</span>
//       </p>
//     </div>
//   `;
// }

// function initMap(){
//    const osmLight = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
//                 maxZoom: 19,
//                 attribution: "&copy; OpenStreetMap contributors",
//               });

//   const osmDark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { 
//             	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a hre f="https://carto.com/attributions">CARTO</a>',
//             	subdomains: 'abcd', 
//             	maxZoom: 20 
//             }); 

// const map = L.map("map",{
//   center:[delman_lat,delman_lng],
//   zoom:10,
//   layers: [osmLight]
// })
// if(!map) return;
//  const baseLayersGrp = {
//       "Light mode": osmLight,
//       "Dark mode": osmDark
//     }
        
//     const layersControl = L.control.layers(baseLayersGrp);
//     layersControl.addTo(map);

//      L.circle([delman_lat, delman_lng], {
//         radius: delman_acc,
//         color: "#136AEC",
//         fillColor: "#136AEC",
//         fillOpacity: 0.15
//    }).addTo(map);

//      L.Routing.control({
//             waypoints: [
//             L.latLng(delman_lat,delman_lng),
//             L.latLng([27.66445,85.433875])
//               ],
//               createMarker: function(i,waypoint,n){
//                 const marker = L.marker(waypoint.latLng);
//                 if(i===0){
//                   marker.bindPopup("Your Location").openPopup();
//                 } else if(i===1){
//                   marker.bindPopup("Restaurant Location").openPopup();
//                 }
//                 return marker;
//               }
//             }).addTo(map);

// }
  

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


