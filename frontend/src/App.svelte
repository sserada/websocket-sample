<script lang="ts">
  import { onMount } from 'svelte';
  import Header from './Header.svelte';

  // Variables to store the selected image files
  let selectedImages: File[] = [];

  // Variable to manage the WebSocket connection
  let connection: WebSocket | null = null;

  // Array to store received data (chunks of the image)
  let receivedData: string[] = [];

  // Handler for the image selection event
  function handleImageChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files) {
      // Save the selected images
      selectedImages = Array.from(input.files);
    }
  }

  // Handler for the drop event
  function handleDrop(event: DragEvent) {
    event.preventDefault();
    const files = event.dataTransfer?.files;
    if (files) {
      // Save the dropped images
      selectedImages = Array.from(files);
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
    console.log(receivedData);
  }

  // Function to send the selected images to the server
  async function sendImages() {
    if (!selectedImages.length || !connection) return;

    let i = 0; // Current image index

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

      i++; // Go to the next image

      // If there are still images to send, read the next one
      if (i < selectedImages.length) {
        reader.readAsDataURL(selectedImages[i]);
      }
    };

    try {
      // Start reading the first image
      reader.readAsDataURL(selectedImages[i]);
    } catch (error) {
      console.error(error);
      handleError();
    }
  }

  function resetPage() {
  // Refresh the page
  location.reload();
  }

  // When the component is mounted, start the connection to the server
  onMount(() => {
    connectToServer();
  });
</script>

<main>
  <Header />
  <div class="container">
    <div
      class="drop-area"
      on:drop={handleDrop}
      on:dragover={handleDragOver}
    >
      <p>Drag and drop files here, or click to select files</p>
      <input
        type="file"
        id="image"
        on:change={handleImageChange}
        style="display: none"
        multiple
      />
      <label for="image">Select Images</label>
    </div>
    <div class="buttons">
      <button on:click={sendImages}>Send</button>
      <button on:click={resetPage}>Reset</button>
    </div>
  </div>

  <table>
    {#if selectedImages.length > 0 && receivedData.length === 0}
      {#each selectedImages as selectedImage, index}
        <tr>
          <img src={URL.createObjectURL(selectedImage)} alt="Selected image" />
        </tr>
      {/each}
    {/if}

    {#if receivedData.length > 0}
      {#each receivedData as data, index}
        <tr>
          <td>
            <img src={URL.createObjectURL(selectedImages[index])} alt="Selected image" />
          </td>
          <td>
            <img src={data} alt="Received image" />
          </td>
        </tr>
      {/each}
    {/if}

    {#if selectedImages.length === 0 && receivedData.length === 0}
      <tr>
        <td>No images selected</td>
      </tr>
    {/if}
  </table>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .container {
    margin-top: 8rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 2rem;
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
    width: 150px;
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
    color: #ccc;
    padding: 1rem;
    width: 250px;
    height: 150px;
    border: 1px solid #eee;
  }

  img {
    max-width: 250px;
    max-height: 150px;
  }
</style>

