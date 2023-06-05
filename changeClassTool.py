import requests
import json
import config
import time
from datetime import datetime, timedelta
def debugPrint(text):
    config.myPrint(text)

def decodeClassCode(text):
    return


#获取token，并获取最新的课程列表
def login():
    url = "https://boke.mxnet.top/api/user/login"

    user = config.ADMIN_USERNAME
    password = config.ADMIN_PASSWORD
    token = config.ADMIN_TMP_TOKEN

    payload = json.dumps({
        "user": user,
        "password": password,
        "admin": True,
        "token": token
    })

    headers = {
        'authority': 'boke.mxnet.top',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://boke.mxnet.top',
        'referer': 'https://boke.mxnet.top/admin/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    response = requests.post(url, headers=headers, data=payload, proxies=None)
    data = response.json()

    if data["code"] == 0:
        config.ADMIN_TOKEN = data["token"]
        print("获取token成功")
    else:
        print("获取token失败")

# 获取课程列表
def get_lession_list():
    print("最新课表获取中")
    url = "https://boke.mxnet.top/api/room/select"
    pages = 8  # 设置获取的总页数

    config.MX_ALL_CLASS_LIST = []  # 重置 MX_ALL_CLASS_LIST 列表

    for page in range(1, pages + 1):
        payload = json.dumps({
            "pages": page,
            "token": config.ADMIN_TOKEN
        })

        headers = {
            'authority': 'boke.mxnet.top',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://boke.mxnet.top',
            'referer': 'https://boke.mxnet.top/admin/',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }

        response = requests.post(url, headers=headers, data=payload)
        data = response.json().get('list', [])

        for item in data:
            msgtime = datetime.strptime(item['createtime'], '%Y-%m-%dT%H:%M:%S.000Z')
            item['createtime'] = msgtime.strftime('%Y-%m-%d %H:%M:%S')
            config.MX_ALL_CLASS_LIST.append({
                'ID': item['ID'],
                'title': item['title'],
                'msgtime': item['createtime']
            })

    two_days_ago = datetime.now() - timedelta(days=2)

    config.MX_RIGHT_CLASS_LIST = [
        item for item in config.MX_ALL_CLASS_LIST
        if datetime.strptime(item['msgtime'], '%Y-%m-%d %H:%M:%S') <= two_days_ago
    ]
    print("最新课表获取成功")
    print(config.MX_ALL_CLASS_LIST)

#校验账号是否可用
def check_user_available(user):
    url = "https://boke.mxnet.top/api/user/v_user"

    payload = json.dumps({
        "user": user,
        "token": config.ADMIN_TOKEN
    })
    headers = {
        'authority': 'boke.mxnet.top',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://boke.mxnet.top',
        'referer': 'https://boke.mxnet.top/admin/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.json()
    return result
#注册账号
def register_user():
    name = "name"
    user = input("请输入用户名：")
    password = input("请输入密码：")

    while True:
        user_check_result = check_user_available(user)

        if user_check_result['code'] != 0:
            error_message = user_check_result.get('message', '未知错误')
            print("用户名不可用，错误信息：", error_message)
            user = input("请重新输入用户名：")
        else:
            break

    url = "https://boke.mxnet.top/api/user/add"

    payload = json.dumps({
        "name": name,
        "user": user,
        "password": password,
        "role": "user",
        "note": "",
        "token": config.ADMIN_TOKEN
    })

    headers = {
        'authority': 'boke.mxnet.top',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://boke.mxnet.top',
        'referer': 'https://boke.mxnet.top/admin/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.json()
    print(result)

    if result['code'] == 0:
        uid = result['uid']
        config.MX_USERID = uid
        print("请求成功，UID：", uid)
    else:
        error_message = result.get('message', '未知错误')
        print("请求失败，错误信息：", error_message)

#增加全部老师，试用7天
def add_all_test():
    url = "https://boke.mxnet.top/api/subscribe/batchadd"

    id_list = [data['ID'] for data in config.MX_RIGHT_CLASS_LIST]
    extime = int((datetime.now() + timedelta(days=7)).timestamp()) * 1000

    payload = json.dumps({
        "ulist": [
            config.MX_USERID
        ],
        "rlist": [
            {
                "ID": id,
                "extime": extime
            } for id in id_list
        ],
        "token":config.ADMIN_TOKEN
    })

    headers = {
        'authority': 'boke.mxnet.top',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://boke.mxnet.top',
        'referer': 'https://boke.mxnet.top/admin/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


#获取账号和uid对应对的字典
def look_uid():
    print("用户id表获取中")
    url = "https://boke.mxnet.top/api/user/select"

    token = config.ADMIN_TOKEN
    total_pages = 10

    headers = {
        'authority': 'boke.mxnet.top',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://boke.mxnet.top',
        'referer': 'https://boke.mxnet.top/admin/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    result = {}  # 存储结果的字典

    for page in range(1, total_pages + 1):
        payload = json.dumps({
            "query": "",
            "pages": page,
            "token": token
        })

        response = requests.request("POST", url, headers=headers, data=payload)

        data = json.loads(response.text)
        users = data["list"]  # 获取当前页的用户列表

        for user in users:
            user_id = user["ID"]
            username = user["user"]
            config.MX_USER_DICT[user_id] = username
    print("用户id表获取成功")
    print(config.MX_USER_DICT)

#根据用户名删除账号
def delete_user():
    # 用户输入账号
    account = input("请输入要删除的账号：")

    # 根据账号查找对应的 ID
    user_id = None
    for id, name in config.MX_USER_DICT.items():
        if name == account:
            user_id = id
            break
    # 如果找到了对应的 ID
    if user_id:
        print("用户id是")
        print(user_id)
        # 构建请求
        url = "https://boke.mxnet.top/api/user/del"
        payload = json.dumps({
            "id": user_id,
            "token": config.ADMIN_TOKEN
        })
        headers = {
            'Content-Type': 'application/json',
            'Referer': 'https://boke.mxnet.top/admin/',
            # 其他请求头字段...
        }

        # 发送请求
        response = requests.post(url, headers=headers, data=payload)

        # 处理响应
        if response.status_code == 200:
            # 成功删除用户
            print("用户删除成功！")
        else:
            # 删除用户失败
            print("用户删除失败！")
    else:
        # 未找到对应的账号
        print("未找到要删除的账号！")

# #删单课
# def delete_lession():
#
# #增加单课
# def add_lession():