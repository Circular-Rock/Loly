import pymysql
from src.db_utils.db_config import DB_CONFIG  # 导入配置信息

def get_db_connection():
    """
    获取数据库连接
    """
    try:
        connection = pymysql.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            port=DB_CONFIG["port"]
        )
        if connection.open:
            print("数据库连接成功")
        return connection
    except pymysql.MySQLError as err:
        print(f"连接数据库失败: {err}")
        return None