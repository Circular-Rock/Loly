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
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserLogin',
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    login() {
      // 处理登录逻辑
      console.log('用户名:', this.username);
      console.log('密码:', this.password);
    },
    register() {
      // 处理注册逻辑
      console.log('Register button clicked');
    }
  }
}
</script>

<style scoped>
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
</style>
