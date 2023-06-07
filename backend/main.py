from fastapi import FastAPI, WebSocket
from typing import List
import uvicorn

app = FastAPI()
connected_clients = set()

@app.websocket('/ws')
async def upload_endpoint(websocket: WebSocket):
    await websocket.accept()
    base64_data = b''
    while True:
        data = await websocket.receive_text()
        # 処理
        print(data)
        await websocket.send_text(data)
        break

    base64_data += data.encode('utf-8')
    print(base64_data)
    await websocket.close()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

