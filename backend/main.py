from fastapi import FastAPI, WebSocket
from typing import List
from pydantic import BaseModel
import uvicorn
import base64
import cv2
import numpy as np

app = FastAPI()
connected_clients = set()

@app.websocket('/ws')
async def upload_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            image = data['chunk']
            format, image = image.split(',')
            image = base64.b64decode(image)
            image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, buffer = cv2.imencode('.jpg', image)
            image = base64.b64encode(buffer).decode('utf-8')
            data['chunk'] = format + ',' + image
            print(data)
            await websocket.send_json(data)
    except:
        pass

    connected_clients.remove(websocket)
    await websocket.close()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

