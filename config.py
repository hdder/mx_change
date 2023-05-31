DEBUG_MODE = 0
ADMIN_USERNAME = "122568799"
ADMIN_PASSWORD = "123456"
# 首次登陆token
ADMIN_TMP_TOKEN = "111111"
# 登陆后token
ADMIN_TOKEN = ""
# 萌侠登陆接口
MX_LOGIN_API = "https://zhibojian.mxnet.top/api"
# 萌侠课程列表
MX_CLASS_DICT = {}
# 萌侠用户列表
MX_USER_DICT = []

def myPrint(text):
    if DEBUG_MODE == 1:
        print(text)