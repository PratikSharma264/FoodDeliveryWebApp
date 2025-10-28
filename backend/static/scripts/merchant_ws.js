let ws = null;

const wsProtocol = location.protocol === 'https' ? 'wss':'ws';
const wsUrl = `${wsProtocol}://${location.host}/ws/socket-server/`;

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
    const {action,data} = msg;
    if (wsHandlers[action]) {
        wsHandlers[action].forEach(fn => fn(data));
    }
  } catch (e) {
    console.error('Invalid delivery WS message', e);
  }
}


function registerWSHandler(action, callback) {
    if (!wsHandlers[action]) wsHandlers[action] = [];
    wsHandlers[action].push(callback);
}


function sendWSMessage(action, data) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action, data : data }));
    }
}

window.addEventListener('DOMContentLoaded', connectWS);
