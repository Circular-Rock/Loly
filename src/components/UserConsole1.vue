<template>
  <div class="console-container">
    <!-- 添加顶部菜单栏 -->
    <div class="top-menu">
      <div class="menu-left">数字主播系统</div>
      <div class="menu-right" @click="toggleUserMenu">
        {{ username }}
        <div v-if="showUserMenu" class="dropdown-menu">
          <div class="dropdown-item" @click="goToProfile">个人信息</div>
          <div class="dropdown-item" @click="goToHomePage">主页面</div>
          <div class="dropdown-item" @click="goToLogin">登录界面</div>
        </div>
      </div>
    </div>
    <div class="content-wrapper"> <!-- 新增的内容容器 -->
      <div class="left-panel">
        <div class="left-panel-wrapper">
          <div class="parallel-video-text">
            <div class="container video-container top large-video"
                 @click="openFileInput('largeVideo')">
              <div class="video-display">
                <video v-if="largeVideoUrl && isVideo(largeVideoFile)" :src="largeVideoUrl" controls class="video-display" autoplay></video>
                <img v-else-if="largeVideoUrl && isImage(largeVideoFile)" :src="largeVideoUrl" alt="Uploaded Image" class="video-display" />
                <span v-else class="upload-prompt">请上传视频或图片</span>
              </div>
              <input type="file" ref="largeVideoFileInput" @change="handleVideoChange()" accept="image/*,video/*"
                     style="display: none;"/>
            </div>
            <div class="text-input-container">
              <div class="text-display" @click="fetchText" :class="{ 'text-clickable': !textInput }">
                {{ textInput || '点击选择参考文本' }}
              </div>
              <div class="upload-prompt-text">↑请朗读以上文本并上传对应音频↓</div> <!-- 新增提示文本 -->
            </div>
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
                  <button @click="submitVideoAndAudio" :disabled="isSubmitting">提交</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="right-panel">
        <div class="right-panel-wrapper">
          <div class="video-container-right top large-video">
            <video id="video" class="video-display-right" autoplay :poster="require('@/assets/loli.png')"
                   style="width: 100%; height: 500px;"></video>
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
                    <el-button @click="start" :disabled="started" type="primary">开启直播</el-button>
                    <el-button @click="stop" :disabled="!started" type="danger">关闭直播</el-button>
                    <el-button @click="sendMessage" type="success">发送文本</el-button>
                  </div>
                  <div class="button-wrapper">
                    <el-button @click="startDVanchor" :disabled="dvAnchorStarted" type="primary">启动主播</el-button>
                    <el-button @click="closeDVanchor" :disabled="!dvAnchorStarted" type="danger">关闭主播</el-button>
                    <el-button @click="useAnchor" type="info">使用主播</el-button>
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
import {useStore} from 'vuex'; // 引入 useStore

export default {
  name: 'UserConsole1',
  setup() {
    const store = useStore(); // 初始化 store
    return {store};
  },
  data() {
    return {
      pc: null,
      useStun: false,
      started: false,
      sessionId: 0,
      message: '',
      textInput: '', // 文本内容
      largeVideoUrl: '',
      audioUrl: '', // 新增的 audioUrl 状态
      dvAnchorStarted: false,
      showUserMenu: false, // 新增状态变量用于控制下拉菜单的显示
      username: sessionStorage.getItem('username') || '',
      largeVideoFile: null,
      isSubmitting: false, // 新增状态变量用于控制提交按钮的禁用状态
    };
  },
  computed: {
    /*username() {
      return this.store.state.username; // 从 Vuex store 获取用户名
    },*/
    // 计算属性来动态设置按钮文本
    //   return this.dvAnchorStarted ? 'Close DV Anchor' : 'Start DV Anchor';
    // }
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
      this.isSubmitting = true; // 提交前禁用按钮
      console.log(this.isSubmitting);
      const formData = new FormData();
      formData.append('username', this.username);
      formData.append('text', this.textInput);
      if (this.largeVideoUrl) {
        fetch(this.largeVideoUrl)
            .then(r => r.blob())
            .then(videoBlob => {
              if (this.isImage(this.largeVideoFile)) {
                formData.append('video', videoBlob, 'video.jpg');
              } else {
                formData.append('video', videoBlob, 'video.mp4');
              }
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
        const allowedExtensions = /(\.mp4|\.jpg)$/i;
        if (!allowedExtensions.exec(file.name)) {
          alert('请上传 mp4 格式的视频文件或 jpg 格式的图片文件');
          this.$refs.largeVideoFileInput.value = ''; // 清空文件输入
        } else {
          this.largeVideoUrl = URL.createObjectURL(file);
          this.largeVideoFile = file; // 保存文件对象以便后续判断类型
        }
      }
    },
    isVideo(file) {
      console.log(file);
      console.log(file.type.startsWith('video/'));
      return file && file.type.startsWith('video/');
    },
    isImage(file) {
      console.log(file);
      console.log(file.type.startsWith('image/'));
      return file && file.type.startsWith('image/');
    },
    handleAudioChange() {
      const file = event.target.files[0];
      if (file) {
        const allowedExtensions = /(\.mp3|\.wav|\.ogg|\.m4a)$/i;
        if (!allowedExtensions.exec(file.name)) {
          alert('请上传 mp3\\wav\\ogg\\m4a 格式的音频文件');
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
        if (response.status === 200) {
          alert('创造数字人成功...');
        }
        console.log('Upload success:', response.data);
        this.isSubmitting = false; // 上传成功后启用按钮
      }).catch(error => {
        console.error('Upload error:', error);
        this.isSubmitting = false; // 上传失败后启用按钮
      });
    },
    startDVanchor() {
      axios.post(start_URL, {
        username: this.username
      }).then(() => {
        this.dvAnchorStarted = true; // 更新状态变量
        console.log('Start DV anchor');
      });
    },
    closeDVanchor() {
      if (this.started) {
        this.stop();
      }
      axios.post(close_URL, {
        username: this.username
      }).then(() => {
        this.dvAnchorStarted = false; // 更新状态变量
        console.log('Close DV anchor');
      }).catch(error => {
        console.error('Close DV anchor error:', error);
      });
    },
    //   if (this.dvAnchorStarted) {
    //     this.closeDVanchor();
    //   } else {
    //     this.startDVanchor();
    //   }
    // },
    useAnchor() {
      this.$router.push('/ImageDisplay');
    },
    toggleUserMenu() {
      this.showUserMenu = !this.showUserMenu; // 切换下拉菜单的显示状态
    },
    goToProfile() {
      this.$router.push('/profile'); // 假设个人信息页面的路由为 /profile
    },
    goToHomePage() {
      this.$router.push('/ImageDisplay');
    },
    goToLogin() {
      sessionStorage.removeItem('username');
      this.$router.push('/UserLogin'); // 假设登录页面的路由为 /login
    },
    fetchText() {
      axios.get('http://192.168.201.159:5000/get_text')
          .then(response => {
            this.textInput = response.data.text; // 假设返回的数据结构为 { text: '...' }
          })
          .catch(error => {
            console.error('Error fetching text:', error);
          });
    }
  },
  beforeUnmount() {
    this.closeDVanchor();
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
  width: 100px;
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
  color: black;
}

.dropdown-item:hover {
  background-color: lightblue;
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
  background-color: #b6b7ff;
}

.right-panel {
  width: 70%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex: 1;
  border-radius: 10px;
  background-color: #bdebff;
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
  background-color: #ffffff;
  flex: 1;
}

.container {
  margin-bottom: 10px;
}

.container.audio-container {
  padding: 10px;
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px; /* 添加此行，减小音频和文本框之间的缝隙 */
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
  border: 1px solid #ccc;
  border-radius: 5px;
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
  justify-content: center;
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
  background-color: #99b7ff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
}

.audio-button button:active {
  background-color: #007aff;
  color: white;
}

.video-container-right {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 10px;
}

.video-container-right.top {
  height: 70%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.video-container-right.top.large-video {
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
  max-height: 400px;
  border-radius: 10px;
}

.video-display-right {
  max-width: 400px;
  max-height: 400px;
  border-radius: 10px;
}

.text-container {
  width: 100%;
  height: 80%;
  padding: 10px;
  box-sizing: border-box;
  background-color: #ffffff;
}

.text-container textarea {
  width: 100%;
  height: 100%;
  resize: none;
  border-radius: 10px;
  padding: 10px;
  box-sizing: border-box;
  background-color: #ffffff;
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
  flex-direction: column;
  justify-content: space-between;
  margin-top: 10px;
}

.button-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.upload-prompt {
  font-family: '幼圆', STKaiti, sans-serif;
  font-size: 24px;
  color: #888;
  text-align: center;
}

.upload-prompt-text {
  font-family: '幼圆', STKaiti, sans-serif;
  font-size: 14px;
  color: #888;
  text-align: center;
  margin: 10px;
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
  height: 100%;
  width: 50%;
  justify-content: center;;
}

.text-input-container {
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 10px;
}

.text-input-container input[type="text"] {
  width: 97%;
  height: 98%;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.square-input {
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.parallel-video-text {
  display: flex;
  width: 100%;
  height: 90%;
}

.text-display {
  font-family: '幼圆', STKaiti, sans-serif;
  width: 97%;
  height: 90%;
  color: #888;
  border: 1px solid #ccc;
  border-radius: 5px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  padding: 10px;
  box-sizing: border-box;
}

.text-clickable {
  background-color: white;
}
</style>

