<script lang="ts">
  import { onMount } from 'svelte';

  let selectedImage: File | null = null;
  let connection: WebSocket | null = null;
  let receivedData: string[] = [];

  function handleImageChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      selectedImage = input.files[0];
    }
  }

  function connectToServer() {
    connection = new WebSocket('ws://localhost:8000/ws');
    connection.onmessage = handleReceivedData;
  }

  function handleReceivedData(event: MessageEvent) {
    const data = JSON.parse(event.data);
    receivedData.push(data.chunk);

    if (data.isLast) {
      const base64Data = receivedData.join('');
      const image = document.createElement('img');
      image.src = base64Data;
      document.body.appendChild(image);

      receivedData = [];
    }
    console.log(data);
    console.log(data.chunk);
    const image = document.createElement('img');
    image.src = receivedData.join('');
    document.body.appendChild(image);
  }

  async function sendImage() {
    if (!selectedImage) return;
    const reader = new FileReader();
    reader.onloadend = function () {
      const base64Data = reader.result as string;
      console.log(base64Data);

      connection?.send(
        JSON.stringify({
          chunk: base64Data,
        })
      );
      selectedImage = null;
    };

    try {
      reader.readAsDataURL(selectedImage);
    } catch (error) {
      console.error(error);
      selectedImage = null;
      if (connection) {
        connection.close();
        connection = null;
      }
      connectToServer();
      return;
    }
  }

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

