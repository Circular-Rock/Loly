<template>
  <div class="container">
    <div class="sidebar">
      <div class="button-section">
        <button v-for="(option, index) in options" :key="index" @click="handleClick(option)" class="sidebar-button">
          {{ option.label }}
        </button>
      </div>
      <div class="input-section">
        <textarea v-model="inputText" placeholder="Enter text here" class="input-textarea"></textarea>
        <button @click="handleSubmit" class="submit-button">提交</button>
      </div>
    </div>
    <div class="main-content">
      <div class="image-container">
        <img :src="imageSrc" alt="Display Image" class="display-image"/>
      </div>
      <div class="audio-player-container">
        <div v-if="audioFiles.length > 0">
          <audio v-for="(audio, index) in audioFiles" :key="index" controls>
            <source :src="audio.url" type="audio/mpeg">
            Your browser does not support the audio element.
          </audio>
        </div>
        <div v-else>
          <!-- 占位内容，当没有音频文件时显示 -->
          <p>暂无音频文件</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'; // 引入 axios
import {copywriting_generated_URL} from '@/router/config.js'; // 引入服务地址配置

export default {
  data() {
    return {
      options: [
        {
          label: '提交商品信息', action: () => {
            this.imageSrc = require('@/assets/logo.png');
          }
        },
        {
          label: '提交文案信息', action: () => {
            alert('Option 2 clicked');
          }
        },
        {
          label: '提交声音信息', action: () => {
            this.sendAudioToBackend();
          }
        }
      ],
      imageSrc: require('@/assets/logo.png'),
      inputText: '',
      audioFiles: []
    };
  },
  methods: {
    handleClick(option) {
      option.action();
    },
    handleSubmit() {
      this.audioFiles = [];
      const payload = {
        text: this.inputText
      };
      this.sendTextToBackend(payload);
    },
    sendTextToBackend(payload) {
      console.log(payload);
      console.log(copywriting_generated_URL);
      axios.post(copywriting_generated_URL, payload) // 使用配置文件中的服务地址
          .then(response => {
            console.log('Backend response:', response.data);
          })
          .catch(error => {
            console.error('Error sending text to backend:', error);
          });
    },
    sendAudioToBackend() {
      const audioUrl = 'http://192.168.228.242:8080/live2d';
      const audioPath = require('@/assets/1.mp3');
      const imagePath = require('@/assets/wrs.jpg');

      Promise.all([
        fetch(audioPath).then(response => response.blob()),
        fetch(imagePath).then(response => response.blob())
      ]).then(([audioBlob, imageBlob]) => {
        const formData = new FormData();
        formData.append('audio', new File([audioBlob], '1.mp3', {type: 'audio/mpeg'}));
        formData.append('image', new File([imageBlob], 'wrs.jpg', {type: 'image/jpeg'}));

        axios.post(audioUrl, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then(() => {
          console.log('Audio and image sent successfully:');
        }).catch(error => {
          console.error('Error sending audio and image:', error);
        });
      }).catch(error => {
        console.error('Error fetching audio or image file:', error);
      });
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 200px;
  background-color: #f4f4f4;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 使按钮和输入框区域在垂直方向上两端对齐 */
}

.button-section {
  flex: 1; /* 使按钮区域占据剩余空间 */
  display: flex;
  flex-direction: column;
  border: 2px solid #ccc; /* 添加边框 */
  border-radius: 5px; /* 可选：添加圆角 */
  padding: 10px;
}

.sidebar-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
  cursor: pointer;
  width: 100%;
  text-align: left;
}

.sidebar-button:hover {
  background-color: #0056b3;
}

.input-section {
  flex: 1; /* 使输入框区域占据剩余空间 */
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 使输入框和提交按钮在垂直方向上两端对齐 */
  border: 2px solid #ccc; /* 添加边框 */
  border-radius: 5px; /* 可选：添加圆角 */
  padding: 10px;
}

.input-textarea {
  flex: 1; /* 使输入框占满剩余空间 */
  width: 90%;
  padding: 10px;
  font-size: 16px;
  margin-bottom: 10px; /* 添加间距 */
  resize: vertical; /* 允许垂直调整大小 */
}

.submit-button {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px;
  cursor: pointer;
  align-self: flex-end; /* 使提交按钮右对齐 */
}

.submit-button:hover {
  background-color: #218838;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* 使内容在容器内居中对齐 */
  padding: 20px;
}

.image-container {
  flex: 1; /* 使图片容器占据剩余空间 */
  width: 100%; /* 使图片容器在水平方向上也占满可用空间 */
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px solid #ccc; /* 添加边框 */
  border-radius: 5px; /* 可选：添加圆角 */
}

.display-image {
  max-width: 100%;
  max-height: 100%;
}

.audio-player-container {
  margin-top: 20px;
}
</style>