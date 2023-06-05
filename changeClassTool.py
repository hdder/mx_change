import requests
import json
import config
import time
from datetime import datetime, timedelta
import pandas as pd
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
            if item['msgtime'] == 0:
                msgtime = datetime.now()  # 设置默认时间为当前时间或其他默认值
            else:
                msgtime = datetime.fromtimestamp(item['msgtime'])
            item['msgtime'] = msgtime.strftime('%Y-%m-%d %H:%M:%S')
            config.MX_ALL_CLASS_LIST.append({
                'ID': item['ID'],
                'title': item['title'],
                'msgtime': item['msgtime']
            })

    two_days_ago = datetime.now() - timedelta(days=2)

    config.MX_RIGHT_CLASS_LIST = [
        item for item in config.MX_ALL_CLASS_LIST
        if datetime.strptime(item['msgtime'], '%Y-%m-%d %H:%M:%S') <= two_days_ago
    ]
    print("最新课表获取成功")
    for index, item in enumerate(config.MX_ALL_CLASS_LIST):
        item['index'] = index + 1
    for index, item in enumerate(config.MX_RIGHT_CLASS_LIST):
        item['index'] = index + 1

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
def add_right_lession():
    url = "https://boke.mxnet.top/api/subscribe/batchadd"
    print("正常老师数")
    print(len(config.MX_RIGHT_CLASS_LIST))
    id_list = [data['ID'] for data in config.MX_RIGHT_CLASS_LIST]
    days = int(input("请输入订阅的有效天数："))
    extime = int((datetime.now() + timedelta(days=days)).timestamp()) * 1000

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

#增加全部老师
def add_all_lession():
    url = "https://boke.mxnet.top/api/subscribe/batchadd"
    print("全部老师数")
    print(len(config.MX_ALL_CLASS_LIST))
    id_list = [data['ID'] for data in config.MX_ALL_CLASS_LIST]
    days = int(input("请输入订阅的有效天数："))
    extime = int((datetime.now() + timedelta(days=days)).timestamp()) * 1000

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

#根据用户名删除账号
def delete_user():
    # 用户输入账号
    account = input("请输入要删除的账号：")
    config.MX_USERID = ""
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

#删单课
def delete_lession():
    # 用户输入账号
    account = input("请输入要删除的账号：")
    config.MX_USERID = ""
    # 根据账号查找对应的 ID
    user_id = None
    for id, name in config.MX_USER_DICT.items():
        if name == account:
            config.MX_USERID = id
            break
    # 如果找到了对应的 ID
    if user_id:
        print("用户id是")
        print(config.MX_USERID)

#增加单课
def add_lession():
    # 用户输入账号
    account = input("请输入要增加的账号：")
    config.MX_USERID=""
    # 根据账号查找对应的 ID
    user_id = None
    for id, name in config.MX_USER_DICT.items():
        if name == account:
            config.MX_USERID = id
            break
    # 如果找到了对应的 ID
    if user_id:
        print("用户id是")
        print(config.MX_USERID)
    url = 'https://boke.mxnet.top/api/subscribe/batchadd'
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

    # 获取用户输入的老师序号
    user_input = input("请选择你要的老师序号（以空格分隔）: ")
    teacher_indexes = user_input.split()

    # 获取用户输入的extime
    extime_input = input("请选择你要的时间（1代表1年，2代表10年）: ")
    extime_dict = {
        '1': 365,  # 1年的天数
        '2': 3650  # 10年的天数
    }

    current_time = datetime.now()
    rlist = [{'id': config.MX_ALL_CLASS_LIST[int(index)]['ID'],
              'extime': int((current_time + timedelta(days=extime_dict[extime_input])).timestamp() * 1000)} for index in
             teacher_indexes]

    data = {
        'ulist': [config.MX_USERID],
        'rlist': rlist,
        'token': config.ADMIN_TOKEN
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    print(response.json())

#生成一个excel，展示现在所有的课程
def get_excel_lession():
    data = config.MX_ALL_CLASS_LIST

    df = pd.DataFrame(data)  # 将字典数据转换为DataFrame

    # 将索引列放到第一列
    df.set_index('index', inplace=True)  # 使用 'index' 列作为索引
    df.reset_index(inplace=True)  # 重置索引，并将原索引列还原为普通列

    # 将DataFrame导出为Excel文件
    df.to_excel('output.xlsx', index=False)  # 文件名为output.xlsx，不包含索引列
