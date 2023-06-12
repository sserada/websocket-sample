<script lang="ts">
  import { onMount } from 'svelte';

  // Variable to store the selected image file
  let selectedImage: File | null = null;

  // Variable to manage the WebSocket connection
  let connection: WebSocket | null = null;

  // Array to store received data (chunks of the image)
  let receivedData: string[] = [];

  // Handler for the image selection event
  function handleImageChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      // Save the selected image
      selectedImage = input.files[0];
    }
  }

  // Function to establish a connection to the WebSocket server
  function connectToServer() {
    connection = new WebSocket('ws://localhost:8000/ws');
    // Set the event handler for receiving messages
    connection.onmessage = handleReceivedData;
  }

  // Function to handle data received from the WebSocket
  function handleReceivedData(event: MessageEvent) {
    const data = JSON.parse(event.data);

    // Add received data to the array
    receivedData.push(data.chunk);

    // If it's the last chunk of data, display the image
    if (data.isLast) {
      appendImage(receivedData.join(''));

      // Reset the data array
      receivedData = [];
    }
  }

  // Function to create and append an image element to the body of the document
  function appendImage(base64Data: string) {
    const image = document.createElement('img');
    image.src = base64Data;
    document.body.appendChild(image);
  }

  // Function to send the selected image to the server
  async function sendImage() {
    if (!selectedImage || !connection) return;

    const reader = new FileReader();
    reader.onloadend = function () {
      // Read the image as Base64 data
      const base64Data = reader.result as string;
      console.log(base64Data);

      // Send the Base64 data to the server via WebSocket
      connection?.send(
        JSON.stringify({
          chunk: base64Data,
        })
      );

      // Reset the selected image
      selectedImage = null;
    };

    try {
      reader.readAsDataURL(selectedImage);
    } catch (error) {
      console.error(error);
      handleError();
    }
  }

  // Function to handle errors: reset the selected image, close the WebSocket connection, and try to reconnect to the server
  function handleError() {
    selectedImage = null;
    if (connection) {
      connection.close();
      connection = null;
    }
    connectToServer();
  }

  // When the component is mounted, start the connection to the server
  onMount(() => {
    connectToServer();
  });
</script>

<main>
  <input type="file" id="image" on:change={handleImageChange} />
  <label for="image">Select Image</label>
  <button on:click={sendImage}>Send</button>
  {#if selectedImage}
    <img src={URL.createObjectURL(selectedImage)} />
  {/if}
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }

  input {
    display: none;
  }

  label {
    padding: 1rem;
    background-color: #000;
    color: #fff;
    border-radius: 0.5rem;
    cursor: pointer;
  }

  button {
    padding: 1rem;
    background-color: #000;
    color: #fff;
    border-radius: 0.5rem;
    cursor: pointer;
  }

  img {
    object-fit: contain;
    max-width: 60%;
  }
</style>

