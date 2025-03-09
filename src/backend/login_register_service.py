from flask import jsonify, session

from src.db_utils.db_user_login_operations import add_user, search_users

def handle_register_request(request):
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # 判断用户名是否已经存在，如果存在就返回错误信息
    if search_users(user_name=username):
        return jsonify({'status': 'error', 'message': '用户名已存在'}), 400

    # 检测密码是否在6-20位之间，如果不在就返回错误信息
    if len(password) < 6 or len(password) > 20:
        return jsonify({'status': 'error', 'message': '密码长度必须在6-20位之间'}), 400

    if not username or not password:
        return jsonify({'status': 'error', 'message': '用户名和密码不能为空'}), 400

    try:
        user_id = add_user(username, password)
        # 设置会话信息
        session['user_id'] = user_id
        session['username'] = username
        return jsonify({'status': 'success', 'message': '用户注册成功', 'user_id': str(user_id)}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def handle_login_request(request):
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': '用户名和密码不能为空'}), 400

    users = search_users(user_name=username)
    if not users:
        return jsonify({'status': 'error', 'message': '用户不存在'}), 400

    user = search_users(user_name=username, user_password=password)
    if user :
        session['user_id'] = user[0][0]
        session_id = session.sid  # 获取 sessionid
        print(f"Session ID: {session_id}")  # 打印 sessionid
        return jsonify({'status': 'success', 'message': '登录成功', 'session_id': session_id})  # 返回 sessionid
    else:
        return jsonify({'status': 'error', 'message': '用户名或密码错误'})
