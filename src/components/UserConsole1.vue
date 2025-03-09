<template>
  <div class="console-container">
    <!-- 添加顶部菜单栏 -->
    <div class="top-menu">
      <div class="menu-left">数字主播系统</div>
      <div class="menu-right">{{ username }}</div>
    </div>
    <div class="content-wrapper"> <!-- 新增的内容容器 -->
      <div class="left-panel">
        <div class="left-panel-wrapper">
          <div class="container video-container top large-video" @click="openFileInput('largeVideo')">
            <div class="video-display">
              <video v-if="largeVideoUrl" :src="largeVideoUrl" controls class="video-display"></video>
              <span v-else class="upload-prompt">请上传视频</span>
            </div>
            <input type="file" ref="largeVideoFileInput" @change="handleVideoChange()" accept="video/*"
                   style="display: none;"/>
          </div>
          <div class="container audio-container">
            <div class="audio-wrapper">
              <div class="audio-display-container">
                <div class="audio-display" @click="openFileInput('audio')">
                  <audio v-if="audioUrl" :src="audioUrl" controls></audio>
                  <span v-else class="upload-prompt">请上传音频</span>
                </div>
                <input type="file" ref="audioFileInput" @change="handleAudioChange()" accept="audio/*"
                       style="display: none;"/>
              </div>
              <div class="audio-button-container">
                <div class="audio-button">
                  <button @click="submitVideoAndAudio">提交</button>
                </div>
              </div>
            </div>
          </div>
          <div class="text-input-container">
            <input type="text" v-model="textInput" placeholder="输入文本" class="square-input"/>
          </div>
        </div>
      </div>
      <div class="right-panel">
        <div class="right-panel-wrapper">
          <div class="video-container top large-video">
            <video id="video" controls class="video-display"></video>
          </div>
          <div class="container audio-container"> <!-- 新增的声音展示容器 -->
            <div class="inner-container audio-wrapper">
              <div class="audio-display-container">
                <div class="audio-display">
                  <audio id="audio"></audio>
                </div>
              </div>
            </div>
          </div>
          <div class="bottom-container">
            <div class="split-container">
              <div class="text-container">
                <div class="inline-container">
                  <textarea v-model="message" placeholder="输入文本"></textarea>
                </div>
                <div class="button-container">
                  <div class="button-wrapper">
                    <button @click="start" :disabled="started">Start</button>
                  </div>
                  <div class="button-wrapper">
                    <button @click="stop" :disabled="!started">Stop</button>
                  </div>
                  <div class="button-wrapper">
                    <button @click="toggleDVanchor">{{ dvAnchorButtonText }}</button>
                  </div>
                  <div class="button-wrapper">
                    <button @click="sendMessage">sendMessage</button>
                  </div>
                  <div class="button-wrapper">
                    <button @click="useAnchor">使用主播</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {offer_URL, sendmessage_URL, start_URL, upload_URL, close_URL} from "@/router/config";
import { useStore } from 'vuex'; // 引入 useStore

export default {
  name: 'UserConsole1',
  setup() {
    const store = useStore(); // 初始化 store
    return { store };
  },
  data() {
    return {
      pc: null,
      useStun: false,
      started: false,
      sessionId: 0,
      message: '',
      textInput: '',
      largeVideoUrl: '',
      audioUrl: '', // 新增的 audioUrl 状态
      dvAnchorStarted: false
    };
  },
  computed: {
    username() {
      return this.store.state.username; // 从 Vuex store 获取用户名
    },
    // 计算属性来动态设置按钮文本
    dvAnchorButtonText() {
      return this.dvAnchorStarted ? 'Close DV Anchor' : 'Start DV Anchor';
    }
  },
  methods: {
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
      this.negotiate();
    },
    stop() {
      this.started = false;
      setTimeout(() => {
        this.pc.close();
      }, 500);
    },
    sendMessage() {
      console.log('Sending: ' + this.message);
      console.log('sessionid: ', this.sessionId);
      axios.post(sendmessage_URL, {
        text: this.message,
        type: 'echo',
        interrupt: true,
        sessionid: parseInt(this.sessionId),
      });
      this.message = '';
    },
    submitVideoAndAudio() {
      const formData = new FormData();
      formData.append('username', 'user1');
      formData.append('text', '天生万物以养人，世人犹怨天不仁。');
      if (this.largeVideoUrl) {
        fetch(this.largeVideoUrl)
            .then(r => r.blob())
            .then(videoBlob => {
              formData.append('video', videoBlob, 'video.mp4');
              if (this.audioUrl) {
                fetch(this.audioUrl)
                    .then(r => r.blob())
                    .then(audioBlob => {
                      formData.append('audio', audioBlob, 'audio.mp3');
                      this.uploadFiles(formData);
                    });
              } else {
                this.uploadFiles(formData);
              }
            });
      } else if (this.audioUrl) {
        fetch(this.audioUrl)
            .then(r => r.blob())
            .then(audioBlob => {
              formData.append('audio', audioBlob, 'audio.mp3');
              this.uploadFiles(formData);
            });
      }
    },
    openFileInput(type) {
      this.$refs[`${type}FileInput`].click();
    },
    handleVideoChange() {
      const file = event.target.files[0];
      if (file) {
        const allowedExtensions = /(\.mp4)$/i;
        if (!allowedExtensions.exec(file.name)) {
          alert('请上传 mp4 格式的视频文件');
          this.$refs.largeVideoFileInput.value = ''; // 清空文件输入
        } else {
          this.largeVideoUrl = URL.createObjectURL(file);
        }
      }
    },
    handleAudioChange() {
      const file = event.target.files[0];
      if (file) {
        const allowedExtensions = /(\.wav)$/i;
        if (!allowedExtensions.exec(file.name)) {
          alert('请上传 mp3 格式的音频文件');
          this.$refs.audioFileInput.value = ''; // 清空文件输入
        } else {
          this.audioUrl = URL.createObjectURL(file);
        }
      }
    },
    uploadFiles(formData) {
      axios.post(upload_URL, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(response => {
        console.log('Upload success:', response.data);
      }).catch(error => {
        console.error('Upload error:', error);
      });
    },
    startDVanchor() {
      axios.post(start_URL, {
        username: 'user1'
      }).then(() => {
        this.dvAnchorStarted = true; // 更新状态变量
      });
    },
    closeDVanchor() {
      axios.post(close_URL, {
        username: 'user1'
      }).then(() => {
        this.dvAnchorStarted = false; // 更新状态变量
      });
    },
    toggleDVanchor() {
      if (this.dvAnchorStarted) {
        this.closeDVanchor();
      } else {
        this.startDVanchor();
      }
    },
    useAnchor() {
      this.$router.push('/ImageDisplay');
    }
  },
  mounted() {
    window.onunload = () => {
      setTimeout(() => {
        if (this.pc) this.pc.close();
      }, 500);
    };

    window.onbeforeunload = (e) => {
      setTimeout(() => {
        if (this.pc) this.pc.close();
      }, 500);
      e = e || window.event;
      if (e) {
        e.returnValue = '关闭提示';
      }
      return '关闭提示';
    };
  }
};
</script>

<style scoped>
/* 添加顶部菜单栏样式 */
.top-menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #7fddff;
  color: black;
  border: 2px solid white; /* 添加边框 */
  border-radius: 5px; /* 可选：添加圆角 */
  padding: 10px 20px;
  font-size: 18px;
}

.menu-left {
  font-weight: bold;
}

.menu-right {
  font-style: italic;
}

.console-container {
  display: flex;
  flex-direction: column; /* 修改为垂直方向的flex布局 */
  height: calc(100vh - 50px); /* 减去顶部菜单栏的高度 */
}

.content-wrapper {
  display: flex;
  flex: 1;
}

.left-panel {
  width: 30%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex: 1;
  border-radius: 10px;
  background-color: lightpink;
}

.right-panel {
  width: 70%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex: 1;
  border-radius: 10px;
  background-color: lightblue;
}

.right-panel-wrapper {
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  background-color: #fff;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.left-panel-wrapper {
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  background-color: #f9f9f9;
  flex: 1;
}

.container {
  margin-bottom: 20px;
}

.container.audio-container {
  padding: 20px;
  display: flex;
  justify-content: space-between;
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

.button-group.voice-button-group button {
  padding: 10px 40px;
  flex: 0 0 30%;
}

.button-group.prompt-button-group button {
  padding: 10px 20px;
  flex: 1;
}

.button-group button {
  padding: 10px 40px;
  flex: 0 0 30%;
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
  gap: 20px;
}

.audio-display-container {
  width: 100%;
  border-radius: 10px;
}

.audio-button-container {
  width: 20%;
  display: flex;
  justify-content: center;
  align-items: center;
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
  background-color: transparent;
  border: none;
  padding: 0;
}

.audio-button button {
  background-color: lightblue;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
}

.audio-button button:active {
  background-color: #0056b3;
  color: white;
}

.video-container {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 10px;
}

.video-container.top {
  height: 70%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.video-container.top.large-video {
  height: 70%;
}

.video-container.bottom.small-video .video-display {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.video-container.bottom.small-video .video-display video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-container.bottom.small-video .upload-prompt {
  font-size: 14px;
  color: #888;
  text-align: center;
}

.video-display {
  max-width: 200px;
  max-height: 200px;
  border-radius: 10px;
}

.text-container {
  width: 100%;
  height: 100%;
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

.inline-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.bottom-container {
  display: flex;
  flex-direction: row;
  flex: 1;
}

.split-container {
  display: flex;
  height: 100%;
  flex: 1;
}

.button-container {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.button-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 48%;
}

.upload-prompt {
  font-size: 14px;
  color: #888;
  text-align: center;
}

.text-input-container {
  margin-top: 10px;
}

.text-input-container input[type="text"] {
  width: 95%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.square-input {
  width: 100%;
  height: 40px; /* 设置高度以使其成为方块形 */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>