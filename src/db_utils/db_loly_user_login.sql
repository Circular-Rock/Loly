-- 创建数据库
CREATE DATABASE IF NOT EXISTS db_loly;

-- 使用数据库
USE db_loly;

-- 创建表
CREATE TABLE IF NOT EXISTS user_login (
    id INT PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL
);

-- 插入数据
INSERT INTO db_loly.user_login (id, user_name, user_password) VALUES (32, 'user123', '12345678');
INSERT INTO db_loly.user_login (id, user_name, user_password) VALUES (33, 'user12345', '12345678');
INSERT INTO db_loly.user_login (id, user_name, user_password) VALUES (34, 'hyj', '12345678');
INSERT INTO db_loly.user_login (id, user_name, user_password) VALUES (35, '双曲线', '12345678');
INSERT INTO db_loly.user_login (id, user_name, user_password) VALUES (36, 'sqx', '12345678');
