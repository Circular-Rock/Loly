from flask import Flask, request, jsonify, session
from flask_cors import CORS
from src.backend.login_register_service import handle_register_request, handle_login_request
from src.backend.redis_config import configure_redis_session  # 修改导入路径

app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求

# 调用配置函数
configure_redis_session(app)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/receive_text', methods=['POST'])
def receive_text():
    data = request.json
    text = data.get('text', '')
    print('Received text from frontend:', text)
    return jsonify({'status': 'success', 'received_text': text})

@app.route('/register', methods=['POST'])
def register_user():
    return handle_register_request(request)

@app.route('/login', methods=['POST'])
def login_user():
    return handle_login_request(request)

if __name__ == '__main__':
    app.run(debug=True)