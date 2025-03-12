<template>
  <div class="container">
    <!-- 添加顶部菜单栏 -->
    <div class="top-menu">
      <div class="menu-left">数字主播系统</div>
      <div class="menu-right" @click="toggleUserMenu">
        {{ username }}
        <div v-if="showUserMenu" class="dropdown-menu">
          <div class="dropdown-item" @click="goToProfile">个人信息</div>
          <div class="dropdown-item" @click="goToHomePage">控制台</div>
          <div class="dropdown-item" @click="goToLogin">退出登录</div>
        </div>
      </div>
    </div>
    <div class="content-wrapper">
      <div class="sidebar">
        <div class="button-section">
          <button v-for="(option, index) in options" :key="index" @click="handleClick(option)" class="sidebar-button"
                  :disabled="option.disabled">
            {{ option.label }}
            <span v-if="option.label === '提交商品信息' && tooltipMessage" class="tooltip">{{ tooltipMessage }}</span>
            <span v-if="option.label === '将文案发送到后端' && tooltipMessageTwo" class="tooltip">{{
                tooltipMessageTwo
              }}</span>
          </button>
          <button @click="toConsole" class="submit-button">控制台</button>
        </div>
        <div class="input-section">
          <textarea v-model="inputText" placeholder="Enter text here" class="input-textarea"></textarea>
          <!-- <button @click="handleSubmit" class="submit-button">控制台</button>  修改提交按钮文本 -->
        </div>
      </div>
      <div class="main-content">
        <div class="video-container top large-video">
          <video id="video" class="video-display" autoplay :poster="require('@/assets/loli.png')"
                 style="width: 100%; height: 500px;"></video>
          <div class="floating-danmu-display">{{ danmuText }}</div>
          <div class="floating-danmu-buttons">
            <button @click="readDanmu" class="floating-danmu-r-button">朗读弹幕</button>
            <button @click="getDanmu" class="floating-danmu-c-button">获取弹幕</button>
          </div>
        </div>
        <div class="audio-player-container">
          <div class="audio-display">
            <audio id="audio" autoplay></audio>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'; // 引入 axios
import {danmu_URL, sendmessage_URL} from '@/router/config.js';
import {copywriting_generated_URL} from '@/router/config.js';
import {offer_URL, start_URL, close_URL} from "@/router/config";
import {useStore} from 'vuex'; // 引入 useStore

export default {
  data() {
    return {
      options: [
        {
          label: '提交商品信息', action: () => {
            this.sendTextToBackend({text: this.inputText});
          }
        },
        {
          label: '将文案发送到后端', action: () => {
            this.sendMessage();
          }, disabled: true
        },
        {
          label: '启动数字人', action: () => {
            this.startDVanchor();
          }, disabled: false
        },
        {
          label: '关闭数字人', action: () => {
            this.closeDVanchor();
          }, disabled: true
        },
        {
          label: '启动直播', action: () => {
            this.start();
          }, disabled: true
        },
        {
          label: '关闭直播', action: () => {
            this.stop();
          }, disabled: true
        }
      ],
      pc: null,
      imageSrc: require('@/assets/logo.png'),
      videoSrc: null,
      inputText: '',
      dvAnchorStarted: false,
      liveStarted: false, // 添加状态变量
      showUserMenu: false,
      tooltipMessage: '', // 添加提示信息变量
      tooltipMessageTwo: '',
      username: sessionStorage.getItem('username') || '',
      danmuText: '这是一条弹幕', // 添加弹幕文本
    };
  },
  setup() {
    const store = useStore(); // 初始化 store
    return {store};
  },
  computed: {
    /*username() {
      return this.store.state.username; // 从 Vuex store 获取用户名
    },*/
  },
  methods: {
    handleClick(option) {
      if (!option.disabled) {
        option.action();
      }
    },
    toConsole() {
      this.$router.push('/console1');
    },
    sendTextToBackend(payload) {
      console.log(payload);
      console.log(copywriting_generated_URL);
      this.options[0].disabled = true;
      this.tooltipMessage = '商品信息已提交,正在火速生成文案'; // 更新提示信息
      axios.post(copywriting_generated_URL, payload, {withCredentials: true}) // 确保携带会话信息
          .then(response => {
            console.log('Backend response:', response.data);
            this.inputText = response.data.response_content;
            this.options[0].disabled = false;
            this.options[1].disabled = false;
            this.tooltipMessage = ''; // 清空提示信息
          })
          .catch(error => {
            console.error('Error sending text to backend:', error);
            this.tooltipMessage = ''; // 清空提示信息
          });
    },
    sendMessage() {
      console.log('Sending: ' + this.inputText);
      console.log('session_id: ', this.sessionId);
      this.options[1].disabled = true;
      this.tooltipMessageTwo = '文案已提交，请等待'; // 使用 tooltipMessageTwo 显示气泡信息
      axios.post(sendmessage_URL, {
        text: this.inputText,
        type: 'echo',
        interrupt: true,
        sessionid: parseInt(this.sessionId),
      }, {withCredentials: true}).then((response) => {
        console.log('Backend response:', response.data);
        this.options[1].disabled = false;
        this.tooltipMessageTwo = ''; // 清空提示信息
      }).catch((error) => {
        if (error.response && error.response.status === 500) {
          this.tooltipMessageTwo = '请先启动数字人'; // 使用 tooltipMessageTwo 显示气泡信息
        } else {
          console.error('Error sending text to backend:', error);
          this.tooltipMessageTwo = ''; // 清空提示信息
        }
      }); // 确保携带会话信息
      //this.inputText = '';
    },
    negotiate() {
      this.pc.addTransceiver('video', {direction: 'recvonly'});
      this.pc.addTransceiver('audio', {direction: 'recvonly'});
      return this.pc.createOffer().then((offer) => {
        return this.pc.setLocalDescription(offer);
      }).then(() => {
        return new Promise((resolve) => {
          if (this.pc.iceGatheringState === 'complete') {
            resolve();
          } else {
            const checkState = () => {
              if (this.pc.iceGatheringState === 'complete') {
                this.pc.removeEventListener('icegatheringstatechange', checkState);
                resolve();
              }
            };
            this.pc.addEventListener('icegatheringstatechange', checkState);
          }
        });
      }).then(() => {
        const offer = this.pc.localDescription;
        return axios.post(offer_URL, {
          sdp: offer.sdp,
          type: offer.type,
        });
      }).then((response) => {
        this.sessionId = response.data.sessionid;
        return this.pc.setRemoteDescription(response.data);
      }).catch((e) => {
        alert(e);
      });
    },
    start() {
      if (!this.dvAnchorStarted) {
        alert('请先开启数字人');
        return;
      }
      const config = {
        sdpSemantics: 'unified-plan'
      };

      if (this.useStun) {
        config.iceServers = [{urls: ['stun:stun.l.google.com:19302']}];
      }

      this.pc = new RTCPeerConnection(config);

      this.pc.addEventListener('track', (evt) => {
        if (evt.track.kind === 'video') {
          document.getElementById('video').srcObject = evt.streams[0];
        } else {
          document.getElementById('audio').srcObject = evt.streams[0];
        }
      });

      this.started = true;
      this.liveStarted = true; // 更新状态变量
      this.options[4].disabled = true; // 禁用开启直播按钮
      this.options[5].disabled = false; // 启用关闭直播按钮
      this.negotiate();

    },
    stop() {
      this.started = false;
      this.liveStarted = false; // 更新状态变量
      this.options[4].disabled = false; // 启用开启直播按钮
      this.options[5].disabled = true; // 禁用关闭直播按钮

      setTimeout(() => {
        this.pc.close();
      }, 500);
    },
    startDVanchor() {
      axios.post(start_URL, {
        username: this.username
      }).then(() => {
        this.dvAnchorStarted = true; // 更新状态变量
        this.options[2].disabled = true; // 禁用启动数字人按钮
        this.options[3].disabled = false; // 启用关闭数字人按钮
        this.options[4].disabled = false; // 启用开启直播按钮
      });
    },
    closeDVanchor() {
      if (this.liveStarted) {
        alert('请先关闭直播');
        return;
      }
      axios.post(close_URL, {
        username: this.username
      }).then(() => {
        this.dvAnchorStarted = false; // 更新状态变量
        this.options[2].disabled = false; // 启用启动数字人按钮
        this.options[3].disabled = true; // 禁用关闭数字人按钮
        this.options[4].disabled = true; // 禁用开启直播按钮
      });
    },
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu; // 切换下拉菜单的显示状态
    },
    goToProfile() {
      this.$router.push('/profile'); // 假设个人信息页面的路由为 /profile
    },
    goToHomePage() {
      this.$router.push('/Console1'); // 假设主页面的路由为 /
    },
    goToLogin() {
      sessionStorage.removeItem('username');
      this.$router.push('/UserLogin'); // 假设登录页面的路由为 /login
    },
    getDanmu() {
      axios.get(danmu_URL)
          .then((response) => {
            console.log('Backend response:', response.data);
            this.danmuText = response.data.text;
          }).catch((error) => {
        console.error('Error getting danmu:', error);
      });
      return this.danmuText;
    },
    readDanmu() {
      this.danmuText = this.getDanmu();
      console.log('Sending: ' + this.danmuText);
      axios.post(sendmessage_URL, {
        text: this.danmuText,
        type: 'echo',
        interrupt: true,
        sessionid: parseInt(this.sessionId),
      }, {withCredentials: true}).then((response) => {
        console.log('Backend response:', response.data);
      }).catch((error) => {
        console.error('Error sending text to backend:', error);
      }); // 确保携带会话信息
      //this.inputText = '';
    },
  }
};
</script>

<style scoped>
/* 添加顶部菜单栏样式 */
.top-menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: rgba(72, 130, 255, 0.78);
  color: black;
  border: 2px solid #ccc; /* 添加边框 */
  border-radius: 5px; /* 可选：添加圆角 */
  padding: 10px 20px;
  font-size: 18px;
}

.menu-left {
  font-family: '幼圆', STKaiti, sans-serif;
  font-weight: bold;
  color: white;
}

.menu-right {
  font-family: '幼圆', STKaiti, sans-serif;
  color: white;
  position: relative; /* 添加相对定位 */
  cursor: pointer; /* 添加鼠标指针样式 */
}

.dropdown-menu {
  position: absolute; /* 绝对定位 */
  top: 100%; /* 菜单显示在用户名下方 */
  right: 0;
  color: black;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.dropdown-item {
  padding: 10px 10px;
  cursor: pointer;
  font-size: 12px;
}

.dropdown-item:hover {
  background-color: lightblue;
}

.container {
  display: flex;
  flex-direction: column; /* 修改为垂直方向的flex布局 */
  height: calc(100vh - 50px); /* 减去顶部菜单栏的高度 */
}

.content-wrapper {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 200px;
  background-color: rgba(113, 224, 246, 0.55);
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
  background-color: #4e80ff;
  font-family: '幼圆', STKaiti, sans-serif;
  font-size: 14px;
  font-weight: bold;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
  cursor: pointer;
  width: 100%;
  text-align: center;
  position: relative; /* 添加相对定位 */
}

.sidebar-button:hover {
  background-color: #0056b3;
}

.sidebar-button:disabled {
  background-color: #9ea9b1;
  cursor: not-allowed;
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
  background-color: rgba(81, 225, 36, 0.93);
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px;
  cursor: pointer;
  /* align-self: flex-start;  使提交按钮左对齐 */
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* 使内容在容器内居中对齐 */
  padding: 20px;
  background-color: rgba(176, 234, 255, 0.44);
}

.video-container {
  flex: 1; /* 使视频容器占据剩余空间 */
  width: 90%; /* 使视频容器在水平方向上也占满可用空间 */
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px solid #ccc; /* 添加边框 */
  border-radius: 5px; /* 可选：添加圆角 */
  background-color: rgb(255, 255, 255); /* 修改背景颜色为不透明 */
}

.audio-player-container {
  margin-top: 20px;
}

.tooltip {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  left: 105%;
  background-color: #333;
  color: #fff;
  padding: 5px 10px;
  border-radius: 5px;
  white-space: nowrap;
  z-index: 10;
  font-size: 14px;
}

.floating-danmu-display {
  position: absolute;
  bottom: 150px; /* 调整位置 */
  right: 100px; /* 调整位置 */
  font-family: '幼圆', STKaiti, sans-serif;
  border: 1px solid #008CBA;
  border-radius: 5px;
  padding: 10px;
  cursor: pointer;
  z-index: 10; /* 确保按钮在视频上方 */
  width: 200px; /* 设置宽度与两个按钮对齐 */
  background-color: rgba(255, 255, 255, 0.8); /* 设置背景颜色 */
}

.floating-danmu-buttons {
  position: absolute;
  bottom: 100px; /* 调整位置 */
  right: 100px; /* 调整位置 */
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  z-index: 10; /* 确保按钮在视频上方 */
}

.floating-danmu-r-button {
  font-family: '幼圆', STKaiti, sans-serif;
  font-weight: bold;
  color: white;
  background-color: lightpink;
  border: none;
  border-radius: 5px;
  padding: 10px;
  cursor: pointer;
  margin-right: 10px;
  width: 100px;
}

.floating-danmu-c-button {
  font-family: '幼圆', STKaiti, sans-serif;
  font-weight: bold;
  color: white;
  background-color: blue;
  border: none;
  border-radius: 5px;
  padding: 10px;
  cursor: pointer;
  width: 100px;
  margin-left: 10px;
}

</style>