from util import camera
from util import public_tools as tool
from service import hr_service as hr

ADMIN_LOGIN = False


def login():
    while True:
        username = input("请输入管理员账号(输入0取消操作)")
        if username == "0":
            return
        password = input("请输入管理员密码:")
        if hr.valid_user(username.strip(), password.strip()):
            global ADMIN_LOGIN
            ADMIN_LOGIN = True
            print(username+"登录成功！请重新选择功能菜单")
            break
        else:
            print("账号或密码错误，请重新输入！")
            print("-----------------------")


def face_clock():
    print("请正面对准摄像头进行打卡")
    name = camera.clock_in()
    if name is not None:
        hr.add_lock_record(name)
        print(name + "打卡成功!")
    else:
        print("无此人")


def check_record():
    menu = """+-------------------------------------------------+
|                 查看记录功能菜单                |
+-------------------------------------------------+
  ①查看员工列表  ②查看打卡记录  ③返回上级菜单
---------------------------------------------------"""
    while True:
        print(menu)
        option = input("请输入菜单序号")
        if option == "1":
            print(hr.get_employee_report())
        elif option == "2":
            report = hr.get_record_all()
            print(report)
        elif option == "3":
            return
        else:
            print("输入的指令有误,请重新输入!")


def employee_management():
    menu = """+-------------------------------------------------+
    |                员工管理功能菜单                 |
    +-------------------------------------------------+
      ①录入新员工  ②删除员工  ③返回上级菜单
    ---------------------------------------------------"""
    while True:
        print(menu)
        option = input("请重新输入菜单序号:")
        if option == "1":
            name = str(input("请重新输入新员工姓名（输入0取消操作）:")).strip()
            if name != "0":
                code = hr.add_new_employee(name)
                print("请面对摄像头，敲击三次回车键完成拍照！")
                camera.register(code)
                print("录入成功")
        elif option == "2":
            print(hr.get_employee_report())
            id = int(input("请输入要删除的员工编号(输入0取消操作)："))
            if id > 0:
                if hr.check_id(id):
                    verification = tool.randomNumber(4)
                    inputVer = input("["+str(verification)+"]请输入验证码:")
                    if str(verification) == str(inputVer).strip():
                        hr.remove_employee(id)
                        print(str(id) + "号员工已删除!")
                    else:
                        print("验证码输入错误, 操作取消")
                else:
                    print("无此员工，操作取消")
        elif option == "3":
            return
        else:
            print("输入的指令有误，请重新输入!")


def report_config():
    menu = """+-------------------------------------------------+
    |                报表设置功能菜单                 |
    +-------------------------------------------------+
    ①作息时间设置  ②返回上级菜单
    ---------------------------------------------------"""
    while True:
        print(menu)
        option = input("请输入菜单序列")
        if option == "1":
            while True:
                work_time = input("请设置上班时间，格式为(08:00:00)：")
                if tool.valid_time(work_time):
                    break
                else:
                    print("上班时间格式有误，请重新输入")
            while True:
                close_time = input("请设置下班时间，格式为(23:59:59)：")
                if tool.valid_time(close_time):
                    break
                else:
                    print("下班时间格式错误， 请重新输入")
            hr.save_work_time(work_time, close_time)
            print("设置完成，上班时间：" + work_time + ",下班时间为：" + close_time)
        elif option == "2":
            return
        else:
            print("输入的指令有误，请重新输入!")


def check_report():
    menu = """+-------------------------------------------------+
    |                考勤报表功能菜单                 |
    +-------------------------------------------------+
       ①日报  ②月报  ③报表设置  ④返回上级菜单
    ---------------------------------------------------"""
    while True:
        print(menu)
        option = input("请输入菜单序号")
        if option == "1":
            while True:
                date = input("输入查询日期，格式为(2008-08-08),输入0查询今天:")
                if date == "0":
                    hr.get_today_report()
                    break
                elif tool.valid_date(date):
                    hr.get_day_report(date)
                    break
                else:
                    print("日期格式输入有误，请重新输入!")
        elif option == "2":
            while True:
                date = input("输入查询月份, 格式为(2008-08),输入0则查询上个月:")
                if date == "0":
                    hr.get_month_report()
                    break
                elif tool.valid_year_month(date):
                    hr.get_month_report(date)
                    break
                else:
                    print("日期格式输入有误，请重新输入!")
        elif option == "3":
            report_config()
        elif option == "4":
            return
        else:
            print("输入的指令有误,请重新输入")


def start():
    finish = False
    menu = """
+--------------------------------------------------+
|                   主功能菜单                     |
+--------------------------------------------------+
 ①打卡  ②查看记录  ③员工管理  ④考勤报表  ⑤退出
---------------------------------------------------"""
    while not finish:
        print(menu)
        option = input("请输入菜单序号")
        if option == "1":
            face_clock()
        elif option == "2":
            if ADMIN_LOGIN:
                check_record()
            else:
                login()
        elif option == "3":
            if ADMIN_LOGIN:
                employee_management()
            else:
                login()
        elif option == "4":
            if ADMIN_LOGIN:
                check_report()
            else:
                login()


hr.load_emp_data()
tital = """
***************************************************
*                MR智能视频打卡系统               *
***************************************************"""
print(tital)
start()

