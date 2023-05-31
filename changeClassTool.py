import requests
import json
import config
import time

def debugPrint(text):
    config.myPrint(text)

def decodeClassCode(text):
    return

def login():
    user = config.ADMIN_USERNAME
    password = config.ADMIN_PASSWORD
    token = config.ADMIN_TMP_TOKEN
    url = config.MX_LOGIN_API
    payloadToken = 'type=login&user={}&password={}&ltype=admin&token={}'.format(user, password, token)
    headers = {
        'authority': 'zhibojian.mxnet.top',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://zhibojian.mxnet.top',
        'referer': 'https://zhibojian.mxnet.top/admin/pages/login/login',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payloadToken)

    # 将响应解析为Python对象
    data = json.loads(response.text)

    # 使用键"token"获取令牌
    token = data["Info"]["token"]
    config.ADMIN_TOKEN = token
    debugPrint(token)
    if token == "":
        print("获取token失败")
        return
    else:
        print("获取token成功")


    # 请求课表
    payloadClass = 'type=Get_RoomList&pagesnum=-1&search=undefined&token={}'.format(token)
    headers = {
        'authority': 'zhibojian.mxnet.top',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'X_CACHE_KEY=b81354f65c9b0556b40356ce645ee000',
        'origin': 'https://zhibojian.mxnet.top',
        'referer': 'https://zhibojian.mxnet.top/admin/pages/user/list',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payloadClass)

    # 将响应解析为Python对象
    debugPrint(response.text)
    data = json.loads(response.text)
    # 输出响应结果
    # {"code":404,"message":"账号已存在"}
    if data['code'] == 0:
        print("获取课程成功!")
    else:
        print(f"获取课程失败，错误信息：{data['message']}")

    return

def regist():
    # 获取用户输入
    name = input("请输入 name：")
    user = input("请输入 user：")
    password = input("请输入 password：")
    if config.ADMIN_TOKEN == "":
        print("token为空，退出")
        return
    token = config.ADMIN_TOKEN # 已有的token

    # 构造请求payload
    payload = f'name={name}&user={user}&password={password}&zhibo=&power=&role=user&type=Add_user&token={token}'

    # 设置请求头
    headers = {
        'authority': 'zhibojian.mxnet.top',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://zhibojian.mxnet.top',
        'referer': 'https://zhibojian.mxnet.top/admin/pages/user/add',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }
    url = config.MX_LOGIN_API
    # 发送请求
    response = requests.post(url, headers=headers, data=payload).text
    data = json.loads(response)
    config.MX_CLASS_DICT = data
    debugPrint(response)
    # 输出响应结果
    if config.MX_CLASS_DICT['code'] == 0:
        print("注册成功！\n 昵称:{}\n用户名:{}\n密码:{}".format(name, user, password))
    else:
        print(f"注册失败，错误信息：{config.MX_CLASS_DICT['message']}")
    return

def getUserId():
    token = config.ADMIN_TOKEN
    url = config.MX_LOGIN_API
    payload = 'type=Get_UserList&pagesnum={}&search=&token={}'.format("{}", token)
    headers = {
        'authority': 'zhibojian.mxnet.top',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'X_CACHE_KEY=b81354f65c9b0556b40356ce645ee000',
        'origin': 'https://zhibojian.mxnet.top',
        'referer': 'https://zhibojian.mxnet.top/admin/pages/user/list',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36'
    }

    page_num = 1
    data_list = []

    index = 0
    while True:
        # 最多index次,防止ip被封
        if index == 5:
            print("达到请求保护次数{}，退出".format(index))
            break
        tmpPayload = payload.format(page_num)
        debugPrint(tmpPayload)
        response = requests.post(url, headers=headers, data=tmpPayload).text
        response_json = json.loads(response)
        debugPrint(response)
        time.sleep(0.5)
        if response_json['code'] != 0:
            print(f"请求第{page_num}页失败")
            break
        data = response_json['list']
        if not data:
            print(f"已请求所有数据，共{len(data_list)}条，{page_num}页")
            break
        data1 = response_json['count']
        if data1 == 0:
            print(f"已请求所有数据，共{len(data_list)}条，{page_num}页")
            break
        data_list.extend(data)
        page_num += 1
        index += 1
    # debugPrint(data_list)
    config.MX_USER_DICT = data_list
    return

def add():
    getUserId()
    userId = input("账号：")
    for data in config.MX_USER_DICT:
        if data['user'] == userId:
            debugPrint(f"目标用户 {userId} 的ID为 {data['ID']}")
            break
    else:
        debugPrint(f"未找到用户 {userId}")
