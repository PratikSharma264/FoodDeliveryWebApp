const orders= [];

registerWSHandler('new_order', handleNewOrder);
registerWSHandler('order_update', handleOrderUpdate);

function handleNewOrder(order) {
  if (orders.some(o => o.id === order.id)) return;
  order.status = 'pending';
  orders.unshift(order);
  renderOrders();
  showNotification();
  document.title = `🔔 New Order #${order.id}`;
}

function handleOrderUpdate(update) {
  const o = orders.find(x => x.id === update.id);
  if (o) {
    o.status = update.status;
    renderOrders();
  }
}

function renderOrders() {
  const container = document.querySelector('.order-list');
  if (!container) return;
  container.innerHTML = '';

  const pending = orders.filter(o => o.status === 'pending');
  if (pending.length === 0) {
    container.innerHTML = `<p id="noneworder"><span><i class="fa-solid fa-circle-xmark"></i></span> No new orders at the moment. </p>`;
    return;
  }

  pending.forEach(order => {
    const div = document.createElement('div');
    div.className = 'summary-card';
    div.innerHTML = `
      <h3>Order #${order.id}</h3>
      <p><strong>Customer:</strong> ${order.customer}</p>
      <p><strong>Address:</strong> ${order.address}</p>
      <p><strong>Items:</strong> ${order.items}</p>
      <p><em>${order.time || 'Just now'}</em></p>
      <button class="accept-btn" data-id="${order.id}">Accept</button>
      <button class="decline-btn" data-id="${order.id}">Decline</button>
    `;
    container.appendChild(div);
  });

  bindButtons();
}

function bindButtons() {
  document.querySelectorAll('.accept-btn').forEach(btn => {
    btn.onclick = () => sendAction('accept_order', parseInt(btn.dataset.id));
  });
  document.querySelectorAll('.decline-btn').forEach(btn => {
    btn.onclick = () => sendAction('decline_order', parseInt(btn.dataset.id));
  });
}

function sendAction(action, id) {
  const order = orders.find(o => o.id === id);
  if (!order) return;
  order.status = action === 'accept_order' ? 'accepted' : 'declined';
  renderOrders();
  sendWSMessage(action,{id});
}

window.addEventListener('DOMContentLoaded', () => {
  renderOrders();
});


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

