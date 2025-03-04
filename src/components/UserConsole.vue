<template>
  <div class="console-container">
    <div class="left-panel">
      <div class="left-panel-wrapper"> <!-- 添加的包裹容器 -->
        <div class="container">
          <div class="inner-container title-button-group"> <!-- 合并后的内部包裹容器 -->
            <h3>音色</h3>
            <div class="button-group vertical grid voice-button-group">
              <button v-for="(option) in voiceOptions" :key="option" @click="selectVoice(option)" :class="{ selected: selectedVoice === option }">
                {{ option }}
              </button>
            </div>
          </div>
        </div>
        <div class="container">
          <div class="inner-container"> <!-- 新增的内部包裹容器 -->
            <h3>Prompt</h3>
            <div class="button-group prompt-button-group">
              <button v-for="option in promptOptions" :key="option" @click="selectPrompt(option)" :class="{ selected: selectedPrompt === option }">
                {{ option }}
              </button>
            </div>
          </div>
        </div>
        <div class="container speed-container"> <!-- 新增的语速容器 -->
          <h3>语速</h3>
          <input type="range" min="1" max="5" v-model="speed" />
          <span>{{ speed }}</span>
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
    <div class="right-panel"> <!-- 新增的右侧容器 -->
      <div class="right-panel-wrapper"> <!-- 添加的包裹容器 -->
        <div class="image-container top large-image"> <!-- 大的图片显示框 -->
          <img :src="largeImageUrl" alt="Image 1" class="image-display" />
        </div>
        <div class="bottom-container"> <!-- 下半部分容器 -->
          <div class="split-container"> <!-- 分割容器 -->
            <div class="image-container bottom small-image"> <!-- 小的图片显示框2 -->
              <img :src="smallImageUrl" alt="Image 2" class="image-display" @click="openFileInput('small')" />
              <input type="file" ref="smallFileInput" @change="handleFileChange('small')" accept="image/*" style="display: none;" />
            </div>
            <div class="text-container"> <!-- 文本输入框容器 -->
              <textarea v-model="textInput" placeholder="输入文本"></textarea>
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
      voiceOptions: ['2222', '7869', '6653', '4099', '5099', '随机'], // 添加了六个选项
      promptOptions: ['oral_2', 'laugh_0', 'break_6'],
      speed: 3,
      textInput: '',
      largeImageUrl: '', // 新增的大图片URL
      smallImageUrl: '', // 新增的小图片URL
      audioUrl: '',
      selectedVoice: null, // 新增的选中音色状态
      selectedPrompt: null // 新增的选中Prompt状态
    };
  },
  methods: {
    selectVoice(option) {
      this.selectedVoice = option; // 设置选中的音色
      console.log('Selected Voice:', option);
    },
    selectPrompt(option) {
      this.selectedPrompt = option; // 设置选中的Prompt
      console.log('Selected Prompt:', option);
    },
    generateAvatar() {
      console.log('Generating Avatar...');
      // 这里可以添加生成形象的逻辑
    },
    generateAudio() {
      console.log('Generating Audio...');
      // 这里可以添加生成声音的逻辑
    },
    openFileInput(type) {
      this.$refs[`${type}FileInput`].click();
    },
    handleFileChange(type) {
      const file = event.target.files[0];
      if (file) {
        this[`${type}ImageUrl`] = URL.createObjectURL(file);
      }
    }
  }
};
</script>

<style scoped>
.console-container {
  display: flex;
  flex-direction: row; /* 修改为行布局 */
  height: 100vh; /* 使容器占满整个视口高度 */
}

.left-panel {
  width: 30%;
  padding: 20px;
  display: flex;
  flex-direction: column; /* 使左侧容器竖直排列 */
  flex: 1; /* 使左侧容器占满整个左侧一列 */
  border-radius: 10px;
  background-color: lightpink;
}

.right-panel {
  width: 70%;
  padding: 20px;
  display: flex;
  flex-direction: column; /* 使右侧容器竖直排列 */
  flex: 1; /* 使右侧容器占满整个右侧一列 */
  border-radius: 10px;
  background-color: lightblue;
}

.right-panel-wrapper {
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  background-color: #fff;
  flex: 1;
  display: flex; /* 添加弹性布局 */
  flex-direction: column; /* 修改为垂直布局 */
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

.container.speed-container { /* 新增的语速容器样式 */
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #fff;
}

.container.speed-container input[type="range"] {
  -webkit-appearance: none;
  width: 100%;
  height: 8px;
  background: #ddd;
  border-radius: 5px;
  outline: none;
  transition: background 0.2s;
}

.container.speed-container input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  background: #007bff;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.2s;
}

.container.speed-container input[type="range"]::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: #007bff;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.2s;
}

.container.speed-container input[type="range"]:hover {
  background: #ccc;
}

.container.speed-container input[type="range"]:hover::-webkit-slider-thumb {
  background: #0056b3;
}

.container.speed-container input[type="range"]:hover::-moz-range-thumb {
  background: #0056b3;
}

.container.speed-container span {
  margin-top: 10px;
  font-size: 16px;
  color: #333;
}

.inner-container { /* 新增的样式 */
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  background-color: #fff;
  height: 100%; /* 使内部容器占满文本框容器 */
}

.inner-container.title-button-group { /* 新增的样式 */
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  background-color: #fff;
  height: 100%; /* 使内部容器占满文本框容器 */
}

.button-group {
  display: flex;
  justify-content: space-between; /* 修改为水平分布并均匀间隔 */
  gap: 10px;
}

.button-group.vertical {
  flex-direction: column; /* 修改按钮排列方向为竖直 */
}

.button-group.voice-button-group {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 修改为三等分 */
  gap: 10px;
}

.button-group.voice-button-group button {
  padding: 10px 40px; /* 增加按钮的宽度 */
  flex: 0 0 30%; /* 设置每个按钮的宽度为30% */
}

.button-group.prompt-button-group {
  display: flex;
  justify-content: space-between; /* 修改为水平分布并均匀间隔 */
  gap: 10px;
}

.button-group.prompt-button-group button {
  padding: 10px 20px; /* 修改按钮的宽度 */
  flex: 1; /* 设置每个按钮的宽度为相等 */
}

.button-group button {
  padding: 10px 40px; /* 增加按钮的宽度 */
  flex: 0 0 30%; /* 设置每个按钮的宽度为30% */
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

.audio-button button:active,
.audio-button button.selected {
  background-color: #0056b3; /* 设置按钮点击背景色 */
  color: white;
}

.image-container {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ccc; /* 添加灰色边框 */
  border-radius: 10px; /* 添加圆润边框 */
}

.image-container.top {
  height: 70%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-container.bottom {
  height: 30%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-container.top.large-image {
  height: 70%;
}

.image-container.bottom.small-image {
  width: 200px; /* 设置固定宽度 */
  height: 150px; /* 设置固定高度 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-container.bottom.small-image img {
  width: 200px; /* 设置固定宽度 */
  height: 200px; /* 设置固定高度 */
  object-fit: cover; /* 保持图片比例并裁剪 */
}

.bottom-container {
  display: flex; /* 添加弹性布局 */
  flex-direction: row; /* 修改为水平布局 */
  flex: 1; /* 使底部容器占满剩余空间 */
}

.split-container {
  display: flex;
  height: 100%; /* 修改高度为100% */
  flex: 1; /* 使分割容器占满底部容器 */
}

.image-display {
  max-width: 100%;
  max-height: 100%;
  border-radius: 10px;
}

.image-container.bottom.small-image {
  width: 50%; /* 修改宽度为50% */
  height: 100%; /* 修改高度为100% */
}

.text-container {
  width: 50%; /* 修改宽度为50% */
  height: 100%; /* 修改高度为100% */
  padding: 10px;
  box-sizing: border-box;
}

.text-container textarea {
  width: 100%;
  height: 100%;
  resize: none;
  border-radius: 10px;
  padding: 10px;
  box-sizing: border-box;
}
</style>
