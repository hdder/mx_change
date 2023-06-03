import changeClassTool
import config

def main():
    # 调试模式
    # config.DEBUG_MODE = 1

    # 登陆获取token
    changeClassTool.login()
    while True:
        choice = input("请选择[1-3]: 0.调试模式 1.新用户试用 2.试用转套餐 3.老用户加课 4.删除客户 5.老客换课 6.帝王客户更新全部课程\n")
        "1。新客户试用：注册账号，取课程列表，订阅所有课程，取系统时间，设置到期时间，"
        "2。试用转套餐：输入账号；取消全部订阅，输入需要订阅的老师序号，取系统时间，设置到期时间"
        "3。老客户加课，输入账号，取"
        if choice == '0':
            config.DEBUG_MODE = 1
        elif choice == '1':
            changeClassTool.regist()
        elif choice == '2':
            changeClassTool.add()
        elif choice == '3':
            changeClassTool.login()
            changeClassTool.get_roomlist()
            print("你选择了功能3")
        # ...
        else:
            print("选择无效，请重新选择")


if __name__ == '__main__':
    main()
