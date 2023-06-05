import changeClassTool
import config

def main():
    # 调试模式
    # config.DEBUG_MODE = 1

    # 登陆获取token
    changeClassTool.login()
    changeClassTool.get_lession_list()
    changeClassTool.look_uid()
    while True:
        choice = input("请选择[1-6]:1.注册 2.加全部课 3.加（正常的）全部课 4.加单个课（根据序号）5。删除账号 6.老师表\n")
        "1。新客户试用：获取后台token；注册账号，取课程列表（取正常更新的老师），取系统时间-+7day，订阅所有课程，"
        "2。试用转套餐：输入账号；取消全部订阅，输入需要订阅的老师序号，取系统时间，设置到期时间"
        "3。老客户换课，输入账号，取"
        if choice == '0':
            config.DEBUG_MODE = 1
        elif choice == '1':
            changeClassTool.register_user()
        elif choice == '2':
            changeClassTool.look_uid()
            changeClassTool.add_all_lession()
        elif choice == '3':
            changeClassTool.look_uid()
            changeClassTool.add_right_lession()
        elif choice == '4':
            changeClassTool.look_uid()
            changeClassTool.add_lession()
        elif choice == '5':
            changeClassTool.look_uid()
            changeClassTool.delete_user()
        elif choice == '6':
            changeClassTool.get_excel_lession()
        # ...
        else:
            print("选择无效，请重新选择")


if __name__ == '__main__':
    main()
