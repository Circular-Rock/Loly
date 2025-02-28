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
    </div>
  </div>
</template>

<script>
import axios from 'axios'; // 引入 axios

export default {
  data() {
    return {
      options: [
        {
          label: 'Option 1', action: () => {
            this.imageSrc = require('@/assets/logo.png');
          }
        },
        {
          label: 'Option 2', action: () => {
            alert('Option 2 clicked');
          }
        },
        {
          label: 'Option 3', action: () => {
            alert('Option 3 clicked');
          }
        }
      ],
      imageSrc: require('@/assets/logo.png'),
      inputText: ''
    };
  },
  methods: {
    handleClick(option) {
      option.action();
    },
    handleSubmit() {
      const payload = {
        text: this.inputText,
        prompt:"",
        custom_voice: 0,
        voice: "2222",
        temperature: 0.3,
        top_p: 0.7,
        top_k: 20,
        skip_refine: 0,
        speed: 5,
        text_seed: 42,
        refine_max_new_token: 384,
        infer_max_new_token: 2048,
        wav: 0,
        is_stream: 0
      };
      this.sendTextToBackend(payload);
    },
    sendTextToBackend(payload) {
      console.log(payload);
      axios.post('http://192.168.228.43:9966/tts', payload)
          .then(response => {
            console.log('Backend response:', response.data);
          })
          .catch(error => {
            console.error('Error sending text to backend:', error);
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
</style>
