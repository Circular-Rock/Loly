import random

# 字符串列表
text_list = [
    "文本1",
    "文本2",
    "文本3",
    "文本4",
    "文本5"
]

# 随机选择一个文本的函数
def get_random_text():
    return random.choice(text_list)
