import json
import websocket

url = "ws://127.0.0.1:8000/ws/deliveryman/"

ws = websocket.create_connection(url)
msg = {
    "type": "deliveryman_location",
    "data": [
      {"order_id": 44, "lat": 27.700769, "lng": 85.300140, "accuracy": 12},
        {"order_id": 45, "lat": 27.701000, "lng": 85.301000, "accuracy": 8}
    ]
}
ws.send(json.dumps(msg))
print("sent")
print("recv:", ws.recv())  # maybe ack
ws.close()
