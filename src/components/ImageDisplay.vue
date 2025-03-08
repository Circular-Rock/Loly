<template>
  <div class="container">
    <div class="sidebar">
      <div class="button-section">
        <button v-for="(option, index) in options" :key="index" @click="handleClick(option)" class="sidebar-button">
          {{ option.label }}
        </button>
        <button @click="toConsole" class="submit-button">控制台</button>
      </div>
      <div class="input-section">
        <textarea v-model="inputText" placeholder="Enter text here" class="input-textarea"></textarea>
        <!-- <button @click="handleSubmit" class="submit-button">控制台</button>  修改提交按钮文本 -->
      </div>
    </div>
    <div class="main-content">
      <div class="video-container">
        <div class="video-container top large-video">
          <video id="video" controls class="video-display" autoplay></video>
        </div>
      </div>
      <div class="audio-player-container">
        <div class="audio-display">
          <audio id="audio" controls autoplay></audio>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'; // 引入 axios
import {sendmessage_URL} from '@/router/config.js';
import {copywriting_generated_URL} from '@/router/config.js';
import {offer_URL, start_URL, close_URL} from "@/router/config";

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
          }
        },
        {
          label: '启动数字人', action: () => {
            this.startDVanchor();
          }
        },
        {
          label: '关闭数字人', action: () => {
            this.closeDVanchor();
          }
        },
        {
          label: '启动直播', action: () => {
            this.start();
          }
        },
        {
          label: '关闭直播', action: () => {
            this.stop();
          }
        }
      ],
      pc: null,
      imageSrc: require('@/assets/logo.png'),
      videoSrc: null,
      inputText: '',
    };
  },
  methods: {
    handleClick(option) {
      option.action();
    },
    toConsole() {
      this.$router.push('/console1');
    },
    sendTextToBackend(payload) {
      console.log(payload);
      console.log(copywriting_generated_URL);
      axios.post(copywriting_generated_URL, payload)
          .then(response => {
            console.log('Backend response:', response.data);
            this.inputText = response.data.response_content;
          })
          .catch(error => {
            console.error('Error sending text to backend:', error);
          });
    },
    sendMessage() {
      console.log('Sending: ' + this.inputText);
      console.log('session_id: ', this.sessionId);
      axios.post(sendmessage_URL, {
        text: this.inputText,
        type: 'echo',
        interrupt: true,
        sessionid: parseInt(this.sessionId),
      });
      this.inputText = '';
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
  /* align-self: flex-start;  使提交按钮左对齐 */
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

.video-container {
  flex: 1; /* 使视频容器占据剩余空间 */
  width: 60%; /* 使视频容器在水平方向上也占满可用空间 */
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px solid #ccc; /* 添加边框 */
  border-radius: 5px; /* 可选：添加圆角 */
}

.display-video {
  width: 100%;
  height: 100%
}

.display-image {
  max-width: 100%;
  max-height: 100%;
}

.audio-player-container {
  margin-top: 20px;
}
</style>