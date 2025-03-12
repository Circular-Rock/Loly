<template>
  <div class="login-container" :class="{'slide-right': isRegister}">
    <div class="image-box">
      <img src="@/assets/loli.png" alt="Loli Image" class="loli-image"/>
    </div>
    <div class="login-box" :class="{'slide-left': isRegister}">
      <h2 class="project-title">虚拟数字主播</h2>
      <input v-if="!isRegister" v-model="username" type="text" placeholder="用户名" class="login-input"/>
      <input v-if="!isRegister" v-model="password" type="password" placeholder="密码" class="login-input"/>
      <input v-if="isRegister" v-model="username" type="text" placeholder="用户名" class="login-input"/>
      <input v-if="isRegister" v-model="password" type="password" placeholder="密码" class="login-input"/>
      <input v-if="isRegister" v-model="confirmPassword" type="password" placeholder="重复密码" class="login-input"/>
      <div class="button-container">
        <button v-if="!isRegister" @click="login" class="login-button">登录</button>
        <button v-if="isRegister" @click="register" class="register-button">注册</button>
        <button @click="toggleForm" class="toggle-button">{{ isRegister ? '返回登录' : '注册' }}</button>
      </div>
      <p v-if="passwordMismatch && isRegister" class="error-message">两次输入的密码不一致</p>
      <p v-if="emptyFields" class="error-message">用户名和密码不能为空</p>
      <p v-if="serverMessage" :class="['server-message', serverMessageType]">{{ serverMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex'; // 引入 useStore

export default {
  name: 'UserLogin',
  setup() {
    const router = useRouter();
    const store = useStore(); // 初始化 store
    return { router, store }; // 确保 store 返回
  },
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      passwordMismatch: false,
      emptyFields: false,
      serverMessage: '',
      serverMessageType: '',
      isRegister: false
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
      axios.post('http://192.168.201.159:5000/login', {
        username: this.username,
        password: this.password
      }, { withCredentials: true }) // 确保携带会话信息
        .then(response => {
          this.serverMessage = response.data.message;
          this.serverMessageType = response.data.status === 'success' ? 'success' : 'error';
          if (response.data.status === 'success') {
            this.store.dispatch('setUsername', this.username); // 存储用户名到 Vuex store
            sessionStorage.setItem('username', this.username);
            this.router.push('/ImageDisplay');
            console.log('Session ID:', response.data.session_id);  // 打印 sessionid
          }
        })
        .catch(error => {
          console.error('登录失败:', error);
        });
    },
    register() {
      if (!this.username || !this.password) {
        this.emptyFields = true;
        this.serverMessage = '';
        return;
      }
      if (this.password !== this.confirmPassword) {
        this.passwordMismatch = true;
        this.emptyFields = false;
        this.serverMessage = '';
        return;
      }
      this.passwordMismatch = false;
      this.emptyFields = false;

      // 发送注册信息到后端
      axios.post('http://192.168.201.159:5000/register', {
        username: this.username,
        password: this.password
      }, { withCredentials: true }) // 确保携带会话信息
      .then(response => {
        this.serverMessage = response.data.message;
        if (response.data.status === 'success') {
          this.toggleForm();
        }
        console.log('注册成功:', response.data);
      })
      .catch(error => {
        this.serverMessage = error.response.data.message;
        console.error('注册失败:', error);
      });
    },
    toggleForm() {
      this.isRegister = !this.isRegister;
      this.username = '';
      this.password = '';
      this.confirmPassword = '';
      this.passwordMismatch = false;
      this.emptyFields = false;
      this.serverMessage = '';
      this.serverMessageType = '';
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
  overflow: hidden;
  position: relative;
  background-color: white;
}

.image-box {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50%;
  background-color: white; /* 可选：设置背景颜色 */
  transition: transform 0.5s ease-in-out;
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
  transition: transform 0.5s ease-in-out;
}

.slide-right .image-box {
  transform: translateX(100%);
}

.slide-right .login-box {
  transform: translateX(-100%);
}

.slide-left .image-box {
  transform: translateX(0);
}

.slide-left .login-box {
  transform: translateX(0);
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

.login-button, .register-button, .toggle-button {
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

.toggle-button {
  background-color: #FF9800;
}

.toggle-button:hover {
  background-color: #e68a00;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>