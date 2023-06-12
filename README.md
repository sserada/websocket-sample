# WebSocket Sample with Svelte and FastAPI

## About

This repository contains a sample project demonstrating the use of WebSockets with Svelte and FastAPI. The project is built with Svelte for the frontend and FastAPI for the backend, and it supports multiple image selection for image processing tasks performed on the server side.

## Main Features

- WebSocket communication: The project makes use of WebSocket technology for real-time, two-way communication between the client and the server.
- Image Processing: The backend is equipped with an image processing module that can receive image data over WebSocket, process it, and send it back to the client
- Multiple Image Selection: The frontend allows users to select multiple images for processing.

## Languages

The project uses the following languages:

- Svelte (52.3%)
- JavaScript (22.5%)
- Other languages make up the remaining 25.2%.

## Getting Started

The following steps will get you a copy of the project up and running on your local machine.

### Prerequisites

To run this project, you will need:

- Node.js and npm installed for the frontend (Svelte).
- Python 3 installed for the backend (FastAPI).

### Installation

1. Clone the repository
```bash
git clone https://github.com/fightingsou/websocket-sample.git
```
2. Navigate into the frontend directory and install dependencies:
```bash
cd websocket-sample/frontend
npm install
```
3. Start the frontend server:
```bash
npm run dev
```
4. In a new terminal, navigate into the backend directory and install dependencies:
```bash
cd ../backend
pip install -r requirements.txt
```
5. Start the backend server:
```bash
uvicorn main:app --reload
```

Now, both the frontend and backend servers should be running. You can view the application by navigating to `localhost:8080` in your browser.

