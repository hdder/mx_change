import changeClassTool
import config

def main():
    # 调试模式
    # config.DEBUG_MODE = 1

    # 登陆获取token
    changeClassTool.login()
    while True:
        choice = input("请选择[1-3]: 0.调试模式 1.注册账号 2.加课\n")
        if choice == '0':
            config.DEBUG_MODE = 1
        elif choice == '1':
            changeClassTool.regist()
        elif choice == '2':
            changeClassTool.add()
        elif choice == '3':
            # 功能3
            print("你选择了功能3")
        # ...
        else:
            print("选择无效，请重新选择")


if __name__ == '__main__':
    main()
