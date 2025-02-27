import pymysql
from src.db_utils.db_connection import get_db_connection


def add_user(user_name, user_password):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO user_login (user_name, user_password) VALUES (%s, %s)"
            cursor.execute(sql, (user_name, user_password))
        connection.commit()
    finally:
        connection.close()

def delete_user(user_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM user_login WHERE id = %s"
            cursor.execute(sql, (user_id,))
        connection.commit()
    finally:
        connection.close()

def update_user(user_id, user_name=None, user_password=None):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE user_login SET "
            params = []
            if user_name is not None:
                sql += "user_name = %s, "
                params.append(user_name)
            if user_password is not None:
                sql += "user_password = %s, "
                params.append(user_password)
            sql = sql.rstrip(', ') + " WHERE id = %s"
            params.append(user_id)
            cursor.execute(sql, tuple(params))
        connection.commit()
    finally:
        connection.close()

def search_users(**kwargs):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM user_login"
            if kwargs:
                sql += " WHERE " + " AND ".join(f"{key} = %s" for key in kwargs)
                cursor.execute(sql, tuple(kwargs.values()))
            else:
                cursor.execute(sql)
            return cursor.fetchall()
    finally:
        connection.close()


