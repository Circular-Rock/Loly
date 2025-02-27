import pymysql

from db_connection import get_db_connection  # 确保正确导入

def fetch_user_login_data():
    """
    获取user_login表中的所有数据
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM user_login")
        result = cursor.fetchall()
        return result
    except pymysql.MySQLError as err:
        print(f"查询数据失败: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

def insert_user_login_data(username, password):
    """
    插入一条新的user_login数据
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO user_login (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))
        connection.commit()
        print("数据插入成功")
    except pymysql.MySQLError as err:
        print(f"插入数据失败: {err}")
    finally:
        cursor.close()
        connection.close()