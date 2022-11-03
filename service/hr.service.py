from entity import organizations as o
from util import public_tools as tool
from util import io_tools as io
import datetime
import calendar


def load_emp_data():
    io.checking_data_files()
    io.load_employee_pic()
    io.load_users()
    io.load_employee_info()
    io.load_lock_recode()
    io.load_work_time_config()


def add_new_employee(name):
    code = tool.randomCode()
    newEmp = o.Employee(o.get_new_id(), name, code)
    o.add(newEmp)
    io.save_employee_all()
    return code


def remove_employee(id):
    io.remove_pics(id)
    o.remove(id)
    io.save_employee_all()
    io.save_lock_record()


def add_lock_record(name):
    record = o.LOCK_RECORD
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if name in record.keys():
        r_list = record[name]
        if len(r_list):
            r_list = list()
        r_list.append(now_time)
    else:
        r_list = list()
        r_list.append(now_time)
        record[name] = r_list
    io.save_lock_record()

def get_employee_report():
    report = "####################################"
    report += "员工信息如下:\n"
    i = 0
    for emp in o.EMPLOYEES:
        report += "(" + str(emp.id) +") " + str(emp.name) + "\t"
        i += 1
        if i == 4:
            report += "\n"
            i = 0
    report = report.strip()
    report += "\n####################################"
    return report


def check_id(id):
    for emp in o.EMPLOYEES:
        if str(emp.id) == str(id):
            return True
    return False


def get_name_with_code(code):
    for emp in o.EMPLOYEES:
        if emp.code == code:
            return emp.name


def get_code_with_id(id):
    for emp in o.EMPLOYEES:
        if str(emp.id) == str(id):
            return emp.code


def valid_user(username, password):
    if username in o.USERS.keys():
        if password == o.USERS.get(username):
            return True
    return False


def save_work_time(work_time, close_time):
    o.WORK_TIME = work_time
    o.CLOSING_TIME = close_time
    io.save_work_time_config()


def get_day_report(date):
    io.load_work_time_config()
    earliest_time = datetime.datetime.strptime(date + "00:00:00", "%Y-%m-%d %H-%M-%S")
    noon_time = datetime.datetime.strptime(date + "12:00:00", "%Y-%m-%d %H-%M-%S")
    latest_time = datetime.datetime.strptime(date + "23:59:59", "%Y-%m-%d %H-%M-%S")
    work_time = datetime.datetime.strptime(date + "" + o.WORK_TIME, "%Y-%m-%d %H-%M-%S")
    closing_time = datetime.datetime.strptime(date + "" + o.CLOSING_TIME, "%Y-%m-%d %H-%M-%S")

    late_list = []
    left_early = []
    absent_list = []

    for emp in o.EMPLOYEES:
        if emp.name in o.LOCK_RECORD.keys():
            emp_lock_list = o.LOCK_RECORD.get(emp.name)
            is_absent = True
            for lock_time_str in emp_lock_list:
                lock_time = datetime.datetime.strptime(lock_time_str, "%Y-%m-%d %H:%M:%S")
                if earliest_time < lock_time < latest_time:
                    is_absent = False
                    if work_time < lock_time <= noon_time:
                        late_list.append(emp.name)
                    if noon_time < lock_time < closing_time:
                        left_early.append(emp.name)
            if is_absent:
                absent_list.append(emp.name)
        else:
            absent_list.append(emp.name)

    emp_count = len(o.EMPLOYEES)
    print("---------" + date + "-----------")
    print("应到人数:" + str(emp_count))
    print("缺勤人数:" + str(len(absent_list)))
    absent_name = ""
    if len(absent_list) == 0:
        absent_name = "(空)"
    else:
        for name in absent_list:
            absent_name += name + " "
    print("缺勤名单:" + absent_name)
    print("迟到人数:" + str(len(late_list)))
    late_name = ""
    if len(late_list) == 0:
        late_name += "(空)"
    else:
        for name in late_list:
            late_name += name + " "
    print("迟到名单:" + late_name)

    print("早退人数:" + str(len(left_early)))
    early_name = ""
    if len(left_early) == 0:
        early_name += "(空)"
    else:
        for name in left_early:
            early_name += name + " "
    print("早退名单:" + early_name)

def get_today_report():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    get_day_report(str(date))

            
def get_month_report(month):
    io.load_work_time_config()
    date = datetime.datetime.strptime(month, "%Y-%m")
    monthRange = calendar.monthrange(date.year, date.month)[1]
    month_first_day = datetime.date(date.year, date.month, 1)
    month_last_day = datetime.date(date.year, date.month, monthRange)

    clock_in = "I"
    clock_out = "O"
    late = "L"
    left_early = "E"
    absent = "A"

    lock_report = dict()

    for emp in o.EMPLOYEES:
        emp_lock_data = []
        

