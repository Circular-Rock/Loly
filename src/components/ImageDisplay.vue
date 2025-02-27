<template>
  <div class="container">
    <div class="sidebar">
      <button v-for="(option, index) in options" :key="index" @click="handleClick(option)" class="sidebar-button">
        {{ option.label }}
      </button>
    </div>
    <div class="main-content">
      <div class="image-container">
        <img :src="imageSrc" alt="Display Image" class="display-image" />
      </div>
      <input type="text" v-model="inputText" placeholder="Enter text here" class="input-text" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      options: [
        { label: 'Option 1', action: () => { this.imageSrc = require('@/assets/logo.png'); } },
        { label: 'Option 2', action: () => { alert('Option 2 clicked'); } },
        { label: 'Option 3', action: () => { alert('Option 3 clicked'); } }
      ],
      imageSrc: require('@/assets/logo.png'),
      inputText: ''
    };
  },
  methods: {
    handleClick(option) {
      option.action();
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

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between; /* 使内容在容器内两端对齐 */
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

.input-text {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  margin-top: 20px; /* 添加间距 */
}
</style>
