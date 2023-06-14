from fastapi import FastAPI, WebSocket
from typing import List
from pydantic import BaseModel
import uvicorn
import base64
import cv2
import numpy as np

app = FastAPI()
connected_clients = set()

chunks_per_image = {}
chunks_counts = {}
outgoing_chunks_per_image = {}
outgoing_chunks_counts = {}

chunk_size = 1024 # This can be adjusted depending on the network conditions

@app.websocket('/ws/{image_name}')
async def upload_endpoint(websocket: WebSocket, image_name: str):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            chunk = data['chunk']

            # Get the image index from the received data
            image_index = data.get('imageIndex', 0)

            if image_name not in chunks_per_image:
                chunks_per_image[image_name] = []
            chunks_per_image[image_name].append(chunk)

            if 'numChunks' in data:
                chunks_counts[image_name] = data['numChunks']

            if len(chunks_per_image[image_name]) == chunks_counts[image_name]:
                image = ''.join(chunks_per_image[image_name])
                format, image = image.split(',')
                image = base64.b64decode(image)

                image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                _, buffer = cv2.imencode('.jpg', image)
                image = base64.b64encode(buffer).decode('utf-8')

                # Split the transformed image into chunks
                outgoing_chunks_per_image[image_name] = [image[i:i+chunk_size] for i in range(0, len(image), chunk_size)]
                outgoing_chunks_counts[image_name] = len(outgoing_chunks_per_image[image_name])

                outgoing_chunks_per_image[image_name][0] = format + ',' + outgoing_chunks_per_image[image_name][0]

                # Send the chunks back to the client
                for i, chunk in enumerate(outgoing_chunks_per_image[image_name]):
                    data = {
                        'chunk': chunk,
                        'index': i,
                        'numChunks': outgoing_chunks_counts[image_name],
                        'imageIndex': image_index  # Send the image index back to the client
                    }
                    await websocket.send_json(data)

                del chunks_per_image[image_name]
                del chunks_counts[image_name]

                connected_clients.remove(websocket)
                await websocket.close()
    except:
        pass

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

