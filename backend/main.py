from fastapi import FastAPI, WebSocket
from typing import List
from pydantic import BaseModel
import uvicorn
import base64
import cv2
import numpy as np

app = FastAPI()
connected_clients = set()

# Variables to store the chunks per image and the number of chunks per image
chunks_per_image = {}
chunks_counts = {}
@app.websocket('/ws/{image_name}')
async def upload_endpoint(websocket: WebSocket, image_name: str):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            chunk = data['chunk']

            # Save the received chunk
            if image_name not in chunks_per_image:
                chunks_per_image[image_name] = []
            chunks_per_image[image_name].append(chunk)

            # Save the number of chunks if provided
            if 'numChunks' in data:
                chunks_counts[image_name] = data['numChunks']

            if len(chunks_per_image[image_name]) == chunks_counts[image_name]:
                # All chunks of the current image have been received
                image = ''.join(chunks_per_image[image_name])
                format, image = image.split(',')
                image = base64.b64decode(image)

                # Convert the image to grayscale
                image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                _, buffer = cv2.imencode('.jpg', image)
                image = base64.b64encode(buffer).decode('utf-8')
                data['chunk'] = format + ',' + image
                await websocket.send_json(data)

                # Reset the chunks for the current image
                del chunks_per_image[image_name]
                del chunks_counts[image_name]

                connected_clients.remove(websocket)
                await websocket.close()
    except:
        pass


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

