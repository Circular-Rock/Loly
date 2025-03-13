import json
import random
import requests

from src.backend.config import ROOM_ID

# 字符串列表
text_list = [
    "常年玩太刀的人大都目光清澈,极度自信。",
    "《千恋万花》是由柚子社自主研发的一款文字冒险游戏。",
    "《原神》是由米哈游自主研发的一款全新开放世界冒险游戏。",
    "我好想做嘉然小姐的狗啊，可是嘉然小姐说她喜欢的是猫。",
    "天生万物以养人，世人尤怨天不仁。"
]

# 随机选择一个文本的函数
def get_random_text():
    return random.choice(text_list)

def random_danmu_text(room_id: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
        'Cookie': 'DedeUserID=353166291; DedeUserID__ckMd5=507c6addd139dfd0; buvid4=AE2E200D-B4EE-953C-4E0A-1468A0D1EF3561883-023020714-HpQUW8G7sJu%2B5fg0bnNstA%3D%3D; buvid_fp_plain=undefined; header_theme_version=CLOSE; enable_web_push=DISABLE; buvid3=B9963DC9-39CB-20A6-FBEC-DEAEBE9461C584083infoc; rpdid=0z9Zw2XGm5|9ZszIilK|18g|3w1RLa2M; FEED_LIVE_VERSION=V_DYN_LIVING_UP; PVID=1; hit-dyn-v2=1; LIVE_BUVID=AUTO7917305337136519; CURRENT_QUALITY=80; fingerprint=bca6a2da144f2737bc29db3c2e0ee54a; b_nut=100; _uuid=F83486F2-2986-81A4-C4E8-6D3C710F10526965755infoc; buvid_fp=bca6a2da144f2737bc29db3c2e0ee54a; enable_feed_channel=ENABLE; SESSDATA=2b0c6737%2C1757070374%2Ce2778%2A32CjBaiEdvkTKSjtr7mtllnfmeU1ZOkAzEWWUrNbuqyu1pawq3H6pPHVi4FISZgBV53cwSVm9DX1gtQ2JzcWlDeWd5Vm9JaHpOenFkVnJ0aW9YeVhhaGVHQzRFRHdkMEVPN0R0dmM4SHVtZDRZanhfMTFFWlJWSVlGM1F1Znh6X1FLVmxOM0dRYjNBIIEC; bili_jct=d3671ad828d81fc49a9d3c44ae3ad957; home_feed_column=5; browser_resolution=1699-834; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDE5NTAwNDksImlhdCI6MTc0MTY5MDc4OSwicGx0IjotMX0.J3aS7I0tNIX6S3bZTzgBEehz5xIYefk5qT6hXaBXweI; bili_ticket_expires=1741949989; bp_t_offset_353166291=1043043364863213568; CURRENT_FNVAL=4048; b_lsid=9FF55337_19589547E22; bsource=search_bing'
    }

    req = requests.get(
        f'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid={room_id}',
        headers=headers)
    text = json.loads(req.text)
    text_list = text['data']['room']
    if len(text_list) == 0:
        return u'这是一条弹幕'
    else:
        return text_list[len(text_list) - 1]['text']


