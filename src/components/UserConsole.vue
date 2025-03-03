<template>
  <div class="console-container">
    <div class="left-panel">
      <div class="left-panel-wrapper"> <!-- 添加的包裹容器 -->
        <div class="container">
          <div class="inner-container"> <!-- 新增的内部包裹容器 -->
            <h3>音色</h3>
            <div class="button-group vertical grid">
              <button v-for="(option) in voiceOptions" :key="option" @click="selectVoice(option)" :class="{ selected: selectedVoice === option }">
                {{ option }}
              </button>
            </div>
          </div>
        </div>
        <div class="container">
          <div class="inner-container"> <!-- 新增的内部包裹容器 -->
            <h3>Prompt</h3>
            <div class="button-group">
              <button v-for="option in promptOptions" :key="option" @click="selectPrompt(option)">
                {{ option }}
              </button>
            </div>
          </div>
        </div>
        <div class="container">
          <div class="inner-container"> <!-- 新增的内部包裹容器 -->
            <h3>语速</h3>
            <input type="range" min="1" max="5" v-model="speed" />
            <span>{{ speed }}</span>
          </div>
        </div>
        <div class="container text-area-container"> <!-- 新增的文本框容器 -->
          <div class="inner-container"> <!-- 新增的内部包裹容器 -->
            <textarea v-model="textInput" placeholder="输入文本"></textarea>
          </div>
        </div>
        <div class="container audio-container"> <!-- 新增的声音展示容器 -->
          <div class="inner-container audio-wrapper">
            <div class="audio-display-container">
              <div class="audio-display">
                <h3>声音展示</h3>
                <audio v-if="audioUrl" :src="audioUrl" controls></audio>
              </div>
            </div>
            <div class="audio-button-container">
              <div class="audio-button">
                <button @click="generateAudio">测试声音</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserConsole',
  data() {
    return {
      voiceOptions: ['1', '2', '3', '4', '5', '随机'], // 添加了六个选项
      promptOptions: ['1', '2', '3'],
      speed: 3,
      textInput: '',
      imageUrl: '',
      audioUrl: '',
      selectedVoice: null // 新增的选中音色状态
    };
  },
  methods: {
    selectVoice(option) {
      this.selectedVoice = option; // 设置选中的音色
      console.log('Selected Voice:', option);
    },
    selectPrompt(option) {
      console.log('Selected Prompt:', option);
    },
    generateAvatar() {
      console.log('Generating Avatar...');
      // 这里可以添加生成形象的逻辑
    },
    generateAudio() {
      console.log('Generating Audio...');
      // 这里可以添加生成声音的逻辑
    }
  }
};
</script>

<style scoped>
.console-container {
  display: flex;
  flex-direction: column; /* 修改为列布局 */
  height: 100vh; /* 使容器占满整个视口高度 */
}

.left-panel {
  width: 30%;
  padding: 20px;
  display: flex;
  flex-direction: column; /* 使左侧容器竖直排列 */
  flex: 1; /* 使左侧容器占满整个左侧一列 */
}

.left-panel-wrapper { /* 添加的样式 */
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  background-color: #f9f9f9;
  flex: 1;
}

.container {
  margin-bottom: 20px;
}

.container.text-area-container {
  flex: 1;
  margin-bottom: 0;
}

.container.audio-container { /* 新增的音频容器样式 */
  padding: 20px;
  display: flex;
  justify-content: space-between;
}

.inner-container { /* 新增的样式 */
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  background-color: #fff;
  height: 100%; /* 使内部容器占满文本框容器 */
}

.button-group {
  display: flex;
  gap: 10px;
}

.button-group.vertical {
  flex-direction: column; /* 修改按钮排列方向为竖直 */
}

.button-group.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.button-group button {
  padding: 10px 20px;
}

.button-group button.selected {
  background-color: #007bff; /* 选中按钮的样式 */
  color: white;
}

textarea {
  width: 100%;
  height: 100%;
  resize: none;
}

.audio-wrapper {
  display: flex;
  flex-direction: row;
  width: 100%;
  gap: 20px; /* 添加间距 */
}

.audio-display-container {
  width: 80%;
  border-radius: 10px; /* 添加圆润边框 */
  background-color: lightblue; /* 修改背景色为淡蓝色 */
}

.audio-button-container {
  width: 20%;
  display: flex; /* 添加弹性布局 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}

.audio-display {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.audio-button {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: transparent; /* 设置背景色为透明 */
  border: none; /* 移除边框 */
  padding: 0; /* 移除内边距 */
}

.audio-button button {
  background-color: lightblue; /* 设置按钮背景色 */
  color: white; /* 设置按钮文字颜色 */
  border: none; /* 移除按钮边框 */
  border-radius: 5px; /* 添加按钮圆角 */
  padding: 10px 20px; /* 设置按钮内边距 */
  cursor: pointer; /* 设置鼠标悬停效果 */
}

.audio-button button:hover {
  background-color: #0056b3; /* 设置按钮悬停背景色 */
}
</style>