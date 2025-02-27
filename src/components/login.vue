<template>
  <div class="login-container">
    <div class="image-box">
      <img src="@/assets/loli.jpg" alt="Loli Image" class="loli-image" />
    </div>
    <div class="login-box">
      <h2 class="project-title">清纯白毛小萝莉</h2>
      <input v-model="username" type="text" placeholder="用户名" class="login-input" />
      <input v-model="password" type="password" placeholder="密码" class="login-input" />
      <div class="button-container">
        <button @click="login" class="login-button">登录</button>
        <button @click="register" class="register-button">注册</button>
      </div>
      <p v-if="serverMessage" :class="['server-message', serverMessageType]">{{ serverMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserLogin',
  data() {
    return {
      username: '',
      password: '',
      serverMessage: '',
      serverMessageType: ''
    };
  },
  methods: {
    login() {
      if (!this.username || !this.password) {
        this.serverMessage = '用户名和密码不能为空';
        this.serverMessageType = 'error';
        return;
      }

      // 发送登录信息到后端
      axios.post('http://localhost:5000/login', {
        username: this.username,
        password: this.password
      })
      .then(response => {
        this.serverMessage = response.data.message;
        this.serverMessageType = response.data.status === 'success' ? 'success' : 'error';
        console.log('登录成功:', response.data);
      })
      .catch(error => {
        this.serverMessage = error.response.data.message;
        this.serverMessageType = 'error';
        console.error('登录失败:', error);
      });
    },
    register() {
      // 处理注册逻辑
      console.log('Register button clicked');
    }
  }
}
</script>

<style scoped>
.server-message {
  margin-top: 10px;
}

.server-message.success {
  color: green;
}

.server-message.error {
  color: red;
}

.login-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100vh;
}

.image-box {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50%;
  background-color: #f0f0f0; /* 可选：设置背景颜色 */
}

.loli-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain; /* 保持图片比例 */
}

.login-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 50%;
  height: 80%;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #ccc;
  background-color: #fff;
  margin-top: auto;
  margin-bottom: auto;
}

.project-title {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.login-input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-bottom: 10px;
  width: 60%;
}

.button-container {
  display: flex;
  justify-content: space-between;
  width: 60%;
}

.login-button, .register-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  color: white;
  cursor: pointer;
  width: 48%;
}

.login-button {
  background-color: #4CAF50;
}

.login-button:hover {
  background-color: #45a049;
}

.register-button {
  background-color: #008CBA;
}

.register-button:hover {
  background-color: #007bb5;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>