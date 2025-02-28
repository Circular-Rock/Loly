<template>
  <div class="register-container">
    <div class="login-box">
      <input v-model="username" type="text" placeholder="用户名" class="login-input" />
      <input v-model="password" type="password" placeholder="密码" class="login-input" />
      <input v-model="confirmPassword" type="password" placeholder="重复密码" class="login-input" />
      <div class="button-container">
        <button @click="register" class="register-button">注册</button>
        <button @click="login" class="login-button">登录</button>
      </div>
      <p v-if="passwordMismatch" class="error-message">两次输入的密码不一致</p>
      <p v-if="emptyFields" class="error-message">用户名和密码不能为空</p>
      <p v-if="serverMessage" class="server-message">{{ serverMessage }}</p>
    </div>
    <div class="image-box">
      <img src="@/assets/loli.jpg" alt="Loli Image" class="loli-image" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router'; // 引入 useRouter

export default {
  name: 'UserRegister',
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      passwordMismatch: false,
      emptyFields: false,
      serverMessage: ''
    };
  },
  setup() {
    const router = useRouter(); // 初始化 router
    return { router };
  },
  methods: {
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
      axios.post('http://localhost:5000/register', {
        username: this.username,
        password: this.password
      })
      .then(response => {
        this.serverMessage = response.data.message;
        if (response.data.status === 'success') {
          this.router.push('/login'); // 修改跳转路径到 login.vue
        }
        console.log('注册成功:', response.data);
      })
      .catch(error => {
        this.serverMessage = error.response.data.message;
        console.error('注册失败:', error);
      });
    },
    login() {
      console.log('Login button clicked');
    }
  }
}
</script>

<style scoped>
.server-message {
  color: green;
  margin-top: 10px;
}

.server-message.error {
  color: red;
}

.register-container {
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

.register-button, .login-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  color: white;
  cursor: pointer;
  width: 48%;
}

.register-button {
  background-color: #008CBA;
}

.register-button:hover {
  background-color: #007bb5;
}

.login-button {
  background-color: #4CAF50;
}

.login-button:hover {
  background-color: #45a049;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>