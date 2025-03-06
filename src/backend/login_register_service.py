from flask import jsonify

from src.db_utils.db_user_login_operations import add_user,search_users

def handle_register_request(request):
    data = request.json
    username = data.get('username')
    password = data.get('password')

    #我还需要一个功能，就是判断用户名是否已经存在，如果存在就返回错误信息
    if search_users(user_name=username):
        return jsonify({'status': 'error', 'message': '用户名已存在'}), 400

    #我还需要一个功能，检测密码是否在6-20位之间，如果不在就返回错误信息
    if len(password) < 6 or len(password) > 20:
        return jsonify({'status': 'error', 'message': '密码长度必须在6-20位之间'}), 400


    if not username or not password:
        return jsonify({'status': 'error', 'message': '用户名和密码不能为空'}), 400

    try:
        user_id = add_user(username, password)
        return jsonify({'status': 'success', 'message': '用户注册成功','user_id':str(user_id)}), 200
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
    if not user:
        return jsonify({'status': 'error', 'message': '密码错误'}), 400

    return jsonify({'status': 'success', 'message': '登录成功','user_id':str(user[0][0])}), 200