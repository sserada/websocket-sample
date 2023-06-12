<script lang="ts">
  import { onMount } from 'svelte';
  import Header from './Header.svelte';

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

  // Handler for the drop event
  function handleDrop(event: DragEvent) {
    event.preventDefault();
    const file = event.dataTransfer?.files[0];
    if (file) {
      // Save the dropped image
      selectedImage = file;
    }
  }

  // Prevent the default behavior for the dragover event
  function handleDragOver(event: DragEvent) {
    event.preventDefault();
  }

  // Function to establish a connection to the WebSocket server
  function connectToServer() {
    connection = new WebSocket('ws://localhost:8000/ws');
    // Set the event handler for receiving messages
    connection.onmessage = handleReceivedData;
  }

  // Function to handle data received from the WebSocket
  function handleReceivedData(event: MessageEvent) {
    // Parse the received data as JSON
    const data = JSON.parse(event.data);
    // Save the received data
    receivedData = [...receivedData, data.chunk];
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
  <div class="container">
    <div
      class="drop-area"
      on:drop={handleDrop}
      on:dragover={handleDragOver}
    >
      <p>Drag and drop an image here</p>
      <input
        type="file"
        id="image"
        on:change={handleImageChange}
        style="display: none"
      />
      <label for="image">Select Image</label>
    </div>
    <button on:click={sendImage}>Send</button>
  </div>

  <table>
    <tr>
      {#if selectedImage}
        <td><img src={URL.createObjectURL(selectedImage)} /></td>
      {/if}
      {#if !selectedImage}
        <td>No image selected</td>
      {/if}
      {#if receivedData.length > 0}
        <td><img src={receivedData[receivedData.length - 1]} /></td>
      {/if}
      {#if !receivedData.length}
        <td>No image received yet</td>
      {/if}
    </tr>
  </table>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 90vh;
  }

  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .drop-area {
    width: 900px;
    height: 300px;
    border: 2px dashed #eee;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 2rem;

  }

  input {
    display: none;
  }

  label {
    text-align: center;
    padding: 1rem;
    width: 150px;
    background-color: #0066b2;
    opacity: 0.8;
    color: #fff;
    border-radius: 0.5rem;
    cursor: pointer;
  }

  button {
    padding: 1rem;
    background-color: #0066b2;
    opacity: 0.8;
    color: #fff;
    border-radius: 0.5rem;
    cursor: pointer;
    margin-left: 1rem;
  }

  table {
    margin-top: 2rem;
    border-collapse: collapse;
  }

  td {
    text-align: center;
    padding: 1rem;
    width: 250px;
    height: 150px;
    border: 1px solid #eee;
  }

  img {
    max-width: 400px;
    max-height: 300px;
  }
</style>

