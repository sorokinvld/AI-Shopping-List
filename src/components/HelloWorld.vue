<template>
  <div>
    <!-- Heading and the buttons to record audio and send to server  -->
    <h1>AI Shopping List </h1>  
    <button @click="startRecording" :disabled="isRecording">Start Recording</button>    
    <button @click="stopRecording" :disabled="!isRecording">Stop Recording</button>
    <button @click="sendAudio" :disabled="!audioBlob">Genearte list</button>
    
    <div v-if="transcribedText">
      <h2>Genearted Text from the recorded clip</h2>
      <!-- display the value of transcribedText  -->
      <p>{{ transcribedText }}</p>                                
                      
    </div>

    <!-- display the shopping list  -->
    <div v-if="shoppingList">
      <h2>Shopping List:</h2>
      <ul>
        <li v-for="(quantity, item) in shoppingList" :key="item">
          {{ quantity }} x {{ item }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";    // import axios to interact with the backend server


// Audio recording and processing 

export default {
  data() {
    return {
      isRecording: false,
      audioChunks: [],
      audioBlob: null,
      transcribedText: "",
      shoppingList: null
    };
  },

  // Initializes audio recording, creating a MediaRecorder object to capture audio data, and setting up event handlers (to collect the recorded audio data chunks)
  // Manage the recording of audio, start/stop the recording, and send the recorded audio data to a server for further processing
  methods: {
    startRecording() {
      this.audioChunks = [];
      this.isRecording = true;
      navigator.mediaDevices
        .getUserMedia({ audio: true })
        .then(stream => {
          this.mediaRecorder = new MediaRecorder(stream);
          this.mediaRecorder.ondataavailable = e => {
            this.audioChunks.push(e.data);
          };
          this.mediaRecorder.start();
        })
        .catch(err => console.error("Error: ", err));
    },
    stopRecording() {
      this.isRecording = false;
      this.mediaRecorder.stop();
      this.audioBlob = new Blob(this.audioChunks, { type: "audio/wav" });
    },
    sendAudio() {
      const formData = new FormData();
      formData.append("audio", this.audioBlob);

      // Axios code block sends POST request to the server, expects response(JSON) with transcribedText and shoppingList, and updates the corresponding data in the Vue component
      axios
        .post("http://localhost:5000/abc", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(response => {
          this.transcribedText = response.data.transcribedText;
          this.shoppingList = response.data.shoppingList;
        })
        .catch(error => console.error("Error: ", error));
    }
  }
};
</script>

<!-- CSS -->
<style>
button {
  margin: 10px;
  padding: 10px 20px;
  background-color: #2f6bbe; 
  color: white;
  text-align: center;
  display: inline-block;
  font-size: 16px;
  cursor: pointer;
  border-radius: 25px;
}

button:hover {
  background-color: #7daa13; 
}
</style>
