DEBUG_MODE = 0
ADMIN_USERNAME = "122568799"
ADMIN_PASSWORD = "123456"
# 首次登陆token
ADMIN_TMP_TOKEN = "111111"
# 登陆后token
ADMIN_TOKEN = ""
# 萌侠登陆接口
MX_LOGIN_API = "https://zhibojian.mxnet.top/api"
# 萌侠全部课程列表
MX_ALL_CLASS_DICT = {}
# 萌侠正常更新的课程列表（最近两天有更新的）
# {'ID': 851, 'title': '龙头部队尾pan', 'teaname': '', 'msgtime': '1970-01-01 08:00:00'}
MX_RIGHT_CLASS_list =[]
# 萌侠用户列表
MX_USER_DICT = []

MX_USERID= ""

def myPrint(text):
    if DEBUG_MODE == 1:
        print(text)