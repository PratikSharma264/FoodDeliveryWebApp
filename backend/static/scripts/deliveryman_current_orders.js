
document.addEventListener("DOMContentLoaded",()=>{
  let delman_lat;
  let delman_lng;
  let delman_acc;
  let res_lat = 27.7172;
  let res_lng = 85.324 ;
  let assigned_to_res = "Pizza Palace";
  let map;
  let layersControl,routingControl;
  // const currentDeliveries = [{
  //     "order_assigned": true,
  //     "order_id": 78,
  //     "user": {
  //       "id": 41,
  //       "username": "bas@gmail.com",
  //       "first_name": "",
  //       "last_name": "",
  //       "email": "bas@gmail.com"
  //     },
  //     "restaurant_id": 1,
  //     "restaurant": {
  //       "id": 1,
  //       "user": null,
  //       "restaurant_name": "Pizza Palace",
  //       "owner_name": "John Doe",
  //       "owner_email": null,
  //       "owner_contact": "9812345678",
  //       "restaurant_address": "123 Main St, Cityville",
  //       "latitude": 27.7172,
  //       "longitude": 85.324,
  //       "cuisine": "Italian",
  //       "description": null,
  //       "restaurant_type": "local",
  //       "profile_picture": null,
  //       "cover_photo": null,
  //       "menu": null,
  //       "created_at": "2025-07-31T10:14:24+00:00",
  //       "approved": false
  //     },
  //     "is_transited": false,
  //     "delivery_charge": "30.00",
  //     "total_price": "9.99",
  //     "order_items": [
  //       {
  //         "id": 73,
  //         "food_item": 1,
  //         "food_item_name": "Margherita Pizza",
  //         "restaurant_name": "Pizza Palace",
  //         "food_item_image": null,
  //         "quantity": 1,
  //         "price_at_order": "9.99",
  //         "total_price": 9.99
  //       }
  //     ],
  //     "order_date": "2025-11-24T10:01:24.814986+00:00",
  //     "status": "WAITING_FOR_DELIVERY",
  //     "payment_method": "cashondelivery",
  //     "latitude": "27.917245",
  //     "longitude": "85.423960",
  //     "customer_details": {
  //       "email": "basnet2@gmail.com",
  //       "phone": "9876543210"
  //     }
  //   },
  //   {
  //     "order_assigned": true,
  //     "order_id": 79,
  //     "user": {
  //       "id": 41,
  //       "username": "net2@gmail.com",
  //       "first_name": "",
  //       "last_name": "",
  //       "email": "net2@gmail.com"
  //     },
  //     "restaurant_id": 1,
  //     "restaurant": {
  //       "id": 1,
  //       "user": null,
  //       "restaurant_name": "Pizza Palace",
  //       "owner_name": "John Doe",
  //       "owner_email": null,
  //       "owner_contact": "9812345678",
  //       "restaurant_address": "123 Main St, Cityville",
  //       "latitude": 27.73885,
  //       "longitude": 85.4776091,
  //       "cuisine": "Italian",
  //       "description": null,
  //       "restaurant_type": "local",
  //       "profile_picture": null,
  //       "cover_photo": null,
  //       "menu": null,
  //       "created_at": "2025-07-31T10:14:24+00:00",
  //       "approved": false
  //     },
  //     "is_transited": false,
  //     "delivery_charge": "30.00",
  //     "total_price": "11.99",
  //     "order_items": [
  //       {
  //         "id": 74,
  //         "food_item": 2,
  //         "food_item_name": "Pepperoni Pizza",
  //         "restaurant_name": "Pizza Palace",
  //         "food_item_image": null,
  //         "quantity": 1,
  //         "price_at_order": "11.99",
  //         "total_price": 11.99
  //       }
  //     ],
  //     "order_date": "2025-11-24T10:33:25.377004+00:00",
  //     "status": "WAITING_FOR_DELIVERY",
  //     "payment_method": "cashondelivery",
  //     "latitude": "27.717245",
  //     "longitude": "85.323960",
  //     "customer_details": {
  //       "email": "basnet2@gmail.com",
  //       "phone": "9876543210"
  //     }
  //   },
  //   {
  //     "order_assigned": true,
  //     "order_id": 80,
  //     "user": {
  //       "id": 41,
  //       "username": "gasnet2@gmail.com",
  //       "first_name": "",
  //       "last_name": "",
  //       "email": "gasnet2@gmail.com"
  //     },
  //     "restaurant_id": 1,
  //     "restaurant": {
  //       "id": 1,
  //       "user": null,
  //       "restaurant_name": "Pizza Palace",
  //       "owner_name": "John Doe",
  //       "owner_email": null,
  //       "owner_contact": "9812345678",
  //       "restaurant_address": "123 Main St, Cityville",
  //       "latitude": 27.4172,
  //       "longitude": 85.524,
  //       "cuisine": "Italian",
  //       "description": null,
  //       "restaurant_type": "local",
  //       "profile_picture": null,
  //       "cover_photo": null,
  //       "menu": null,
  //       "created_at": "2025-07-31T10:14:24+00:00",
  //       "approved": false
  //     },
  //     "is_transited": false,
  //     "delivery_charge": "30.00",
  //     "total_price": "9.99",
  //     "order_items": [
  //       {
  //         "id": 75,
  //         "food_item": 1,
  //         "food_item_name": "Margherita Pizza",
  //         "restaurant_name": "Pizza Palace",
  //         "food_item_image": null,
  //         "quantity": 1,
  //         "price_at_order": "9.99",
  //         "total_price": 9.99
  //       }
  //     ],
  //     "order_date": "2025-11-24T11:34:02.708066+00:00",
  //     "status": "WAITING_FOR_DELIVERY",
  //     "payment_method": "cashondelivery",
  //     "latitude": "27.717245",
  //     "longitude": "85.323960",
  //     "customer_details": {
  //       "email": "basnet2@gmail.com",
  //       "phone": "9876543210"
  //     }
  //   }];
  const currentDeliveries = [];
  let isassigned = null;

  const deliveryItemContainer = document.querySelector("#delivery-list-container");
  const deliveryInfoContainer = document.querySelector("#delivery-info-container");
  const outForDeliveryBtn = document.querySelector("#out-for-deliverybtn");
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
      const {has_current_assignments,assigned_restaurant,latitude,longitude,orders} = data;
      isassigned = has_current_assignments;
      res_lat = latitude;
      res_lng=longitude;
      assigned_to_res = assigned_restaurant;
      // isassigned = true;
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
      deliveryInfoContainer.style.display="none";
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
      deliveryInfoContainer.style.display = "inline-block";
      deliveryInfoContainer.classList.remove("hidden");

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

map = L.map("map",{
  center:[delman_lat,delman_lng],
  zoom:10,
  layers: [osmLight]
})
if(!map) return;
 const baseLayersGrp = {
      "Light mode": osmLight,
      "Dark mode": osmDark
    }
        
  layersControl = L.control.layers(baseLayersGrp);
    layersControl.addTo(map);

     L.circle([delman_lat, delman_lng], {
        radius: delman_acc,
        color: "#136AEC",
        fillColor: "#136AEC",
        fillOpacity: 0.15
   }).addTo(map);

   const iconRed = L.icon({
    iconUrl: ICON_RED,
     iconSize: [25, 41],
   });

     L.Routing.control({
            waypoints: [
            L.latLng(delman_lat,delman_lng),
            L.latLng(res_lat,res_lng)
              ],
              show:false,
              createMarker: function(i,waypoint,n){
                let marker;
                if(i===0){
                  marker = L.marker(waypoint.latLng);
                  marker.bindPopup("Your Location").openPopup();
                } else if(i===1){
                  marker = L.marker(waypoint.latLng,{icon:iconRed});
                  marker.bindPopup(`${assigned_to_res}`).openPopup();
                }
                return marker;
              }
            }).addTo(map);

//             currentDeliveries.forEach((delivery,index) => {
//                 setTimeout(()=>{
//  L.Routing.control({
//       waypoints: [
//         L.latLng(res_lat, res_lng),
//         L.latLng(parseFloat(delivery.latitude), parseFloat(delivery.longitude)),
//       ],
//       show: false,
//       lineOptions: { styles: [{ color: "green", weight: 3 }] },
//       createMarker: function (i, waypoint) {
//         if (i === 0) return null; 
//         return L.marker(waypoint.latLng,{icon:iconGreen}).bindPopup(`${delivery.user.email}`);
//       },
//     }).addTo(map);
//   },index*2000);
//   });

}

function showDeliveryRoute(delivery) {
   const iconGreen = L.icon({
    iconUrl: ICON_GREEN,
     iconSize: [35, 50],
   });
  if (routingControl) {
    map.removeControl(routingControl);
  }

  routingControl = L.Routing.control({
    waypoints: [
      L.latLng(res_lat, res_lng),       
      L.latLng(parseFloat(delivery.latitude), parseFloat(delivery.longitude))
    ],
    show: false,
    lineOptions: { styles: [{ color: "green", weight: 3 }] },
    createMarker: function(i, waypoint) {
      let marker;
      if (i === 0) return;
      if (i===1){  
        marker = L.marker(waypoint.latLng, {icon: iconGreen}).bindPopup(delivery.user.email);
      }
      return marker;
    }
  }).addTo(map);
}


currentDeliveries.forEach((delivery, index) => {
  const divBlock = document.createElement('div');
  divBlock.className = 'delivery-card';
  if (!delivery.order_id) {
    console.warn("Skipping delivery with null order_id", delivery);
    return;
}

  divBlock.innerHTML = `
    <div class="delivery-main-detail">
      <h4>Order ID: ${delivery.order_id}</h4>
      <p><span> Customer: </span> ${delivery.user.first_name}</p>
      <p><span> Total: </span> NPR ${delivery.total_price} (excluding delivery charge)</p>
      <p><span> Delivery charge: </span> NPR ${delivery.delivery_charge} (excluding delivery charge)</p>
      <p><span>Status:</span> <strong>${delivery.status}</strong></p>
      <div class="button-container">
      <button class="view-delivery-btn" data-id="${delivery.order_id}">View Delivery</button>
      ${
      delivery.status === 'OUT_FOR_DELIVERY' ? 
      `<button class="view-delivery-btn" data-id=${delivery.order_id}>Delivery Completed</button> `:
      ""
      }
      </div>
    </div>
    <div class="order-details">
      <div>
        <h4>Order Items:</h4>
        <ul>
          ${delivery.order_items
            .map(
              (item) => `
                <li>
                  <img src="${item.food_item_image}" width="50" height="50" />
                  <span><strong>${item.food_item_name}</strong> (x${item.quantity}) - NPR ${item.total_price}</span>
                </li>`
            )
            .join("")}
        </ul>
      </div>
      <div>
        <h4>Customer Details:</h4>
        <p>Email: ${delivery.user.email}</p>
        <p>Phone: ${delivery.customer_details.phone}</p>
      </div>
      </div>
      <button id="${delivery.order_id}" class="fullpageview-btn"><i class="fa-solid fa-angle-down"></i></button>
  `;

  const btn = divBlock.querySelector(".fullpageview-btn");
  const orderDetails = divBlock.querySelector(".order-details");
  const deliveryCompleted = divBlock.querySelector(`[data-id="${delivery.order_id}"]`);


  btn.addEventListener("click", () => {
    orderDetails.classList.toggle("show");

    const icon = btn.querySelector("i");
    icon.classList.toggle("rotate");

  });

 divBlock.querySelector('.view-delivery-btn').addEventListener('click', (e) => {
    showDeliveryRoute(delivery);
  });

  // delivery complete vaye paxi ko lagi:
  if(deliveryCompleted){
    deliveryCompleted.addEventListener('click',(e)=>{

          async function deliveryCompletedFunc() {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/json/deliveryman-completed-delivery/`,
        {
          credentials:"include"
        }
      );
    } catch (err) {
      console.error("error: ", err);
      showError({ message: `${err?.message}` });
    }
  }
    })
  }


  deliveryItemContainer.appendChild(divBlock);
});

  }

  // ya out for delivery click garda ko logic:
  if(outForDeliveryBtn){
    outForDeliveryBtn.addEventListener("click",(e)=>{
      
    async function outForDeliveryRequest() {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/json/deliveryman-out-delivery/`,
        {
          credentials:"include"
        }
      );
    } catch (err) {
      console.error("error: ", err);
      showError({ message: `${err?.message}` });
    }
  }
    })
  }

})