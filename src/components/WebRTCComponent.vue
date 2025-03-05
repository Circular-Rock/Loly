<template>
  <div>
    <div class="option">
      <input id="use-stun" type="checkbox" v-model="useStun" />
      <label for="use-stun">Use STUN server</label>
    </div>
    <button @click="start" :disabled="started">Start</button>
    <button @click="stop" :disabled="!started">Stop</button>
    <input type="hidden" id="sessionid" :value="sessionId" />
    <form class="form-inline" id="echo-form" @submit.prevent="sendMessage">
      <div class="form-group">
        <p>input text</p>
        <textarea cols="2" rows="3" style="width:600px;height:50px;" class="form-control" id="message" v-model="message"></textarea>
      </div>
      <button type="submit" class="btn btn-default">Send</button>
    </form>
    <div id="media">
      <h2>Media</h2>
      <audio id="audio" autoplay="true"></audio>
      <video id="video" style="width:600px;" autoplay="true" playsinline="true"></video>
    </div>
  </div>
</template>

<script>
import axios from 'axios'; // 引入 axios

export default {
  data() {
    return {
      pc: null,
      useStun: false,
      started: false,
      sessionId: 0,
      message: ''
    };
  },
  methods: {
    negotiate() {
      this.pc.addTransceiver('video', { direction: 'recvonly' });
      this.pc.addTransceiver('audio', { direction: 'recvonly' });
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
        return axios.post('http://10.10.24.171:5000/offer', {
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
        config.iceServers = [{ urls: ['stun:stun.l.google.com:19302'] }];
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
      axios.post('http://10.10.24.171:5000/human', {
        text: this.message,
        type: 'echo',
        interrupt: true,
        sessionid: parseInt(this.sessionId),
      });
      this.message = '';
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

<style>
button {
  padding: 8px 16px;
}

video {
  width: 100%;
}

.option {
  margin-bottom: 8px;
}

#media {
  max-width: 1280px;
}
</style>