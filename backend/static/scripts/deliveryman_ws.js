let ws = null;

let newDeliveryCount = 0;
const countElement = document.querySelector(".new-order-count");
countElement.innerHTML = newDeliveryCount;
const wsProtocol = location.protocol === 'https' ? 'wss':'ws';
const wsUrl = `${wsProtocol}://${location.host}/ws/deliveryman/`;

const wsHandlers = {};

function connectWS(){
    ws = new WebSocket(wsUrl);

    ws.addEventListener('open',()=>{
        console.log("Connected to Deliveryman WS");
    })

    ws.addEventListener('close',()=>{
        console.warn("WS connection closed. Reconnecting in 5 sec......");
        setTimeout(connectWS,5000);
    })

    ws.addEventListener('error',(e)=>{
        showError({wsError:"WS error"},"error");
        console.error('WS error',e);
    })

    ws.addEventListener('message',onMessage);
}

function onMessage(evt) {
  try {
    const msg = JSON.parse(evt.data);
    console.log("msg:",msg);

      if (msg.type === "chat") {
        newDeliveryCount++;
        countElement.innerHTML = newDeliveryCount;
        showNotification();
        document.title = `🔔 New Delivery Request Received`;
        setTimeout(() => { document.title = "Delivery Request"; }, 2000);
    }

    Object.values(wsHandlers).forEach(handler => {
        try { handler(msg); } catch(e) { console.error("Handler error", e); }
    });
  } catch (e) {
    console.error('Invalid delivery WS message', e);
  }
}

function sendWSMessage(action, data) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action, data : data }));
    }
}

function resetDeliveryCount() {
    newDeliveryCount = 0;
    countElement.innerHTML = 0;
}

window.resetDeliveryCount = resetDeliveryCount;


function registerWSHandler(name, callback) {
    if(!wsHandlers[name]){
        wsHandlers[name] = callback;
    }
}

window.registerWSHandler = registerWSHandler;

window.addEventListener('DOMContentLoaded', connectWS);
