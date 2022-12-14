from service import hr_service as hr
from entity import organizations as o
from service import recognize_service as rs
import os
import cv2
import numpy as np

PATH = os.getcwd() + "\\data\\"
PIC_PATH = PATH + "faces\\"
DATA_FILE = PATH + "employee_data.txt"
WORK_TIME = PATH + "work_time.txt"
USER_PASSWORD = PATH + "user_password.txt"
RECORD_FILE = PATH + "lock_record.txt"
IMG_WIDTH = 640
IMG_HEIGHT = 480


def checking_data_files():
    if not os.path.exists(PATH):
        os.mkdir(PATH)
        print("数据文件丢失, 已重新创建:" + PATH)
    if not os.path.exists(PIC_PATH):
        os.mkdir(PIC_PATH)
        print("照片文件夹丢失， 已重新创建:" + PIC_PATH)
    sample1 = PIC_PATH + "1000000000.png"
    if not os.path.exists(sample1):
        sample_img_1 = np.zeros((IMG_HEIGHT, IMG_WIDTH, 3), np.uint8)
        sample_img_1[:, :, 0] = 255
        cv2.imwrite(sample1, sample_img_1)
        print("默认样本1已补充")
    sample2 = PIC_PATH + "2000000000.png"
    if not os.path.exists(sample2):
        sample_img_2 = np.zeros((IMG_HEIGHT, IMG_WIDTH, 3), np.uint8)
        sample_img_2[:, :, 1] = 255

    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, "a+")
        print("员工信息文件丢失， 已重新创建:" + DATA_FILE)
    if not os.path.exists(RECORD_FILE):
        open(RECORD_FILE, "a+")
        print("打卡记录文件丢失, 已重新创建:" + RECORD_FILE)
    if not os.path.exists(USER_PASSWORD):
        file = open(USER_PASSWORD, "a+", encoding="utf-8")
        user = dict()
        user["mr"] = "mrsoft"
        file.write(str(user))
        file.close()
        print("管理员账号密码文件丢失，已重新创建：" + RECORD_FILE)
    if not os.path.exists(WORK_TIME):
        file = open(WORK_TIME, "a+", encoding="utf-8")
        file.write("09:00:00/17:00:00")
        file.close()
        print("上下班时间配置文件丢失，已重新创建：" + RECORD_FILE)


def load_employee_info():
    max_id = 1
    file = open(DATA_FILE, "r", encoding="utf-8")
    for line in file.readlines():
        id, name, code = line.rstrip().split(",")
        o.add(o.Employee(id, name, code))
        if int(id) > max_id:
            max_id = int(id)

    o.MAX_ID = max_id
    file.close()


def load_lock_recode():
    file = open(RECORD_FILE, "r", encoding="utf-8")
    text = file.read()
    if len(text) > 0:
        o.LOCK_RECORD = eval(text)
    file.close()


def load_employee_pic():
    photos = list()
    labels = list()
    pics = os.listdir(PIC_PATH)
    if len(pics) > 0:
        for file_name in pics:
            code = file_name[0:o.CODE_LEN]
            photos.append(cv2.imread(PIC_PATH + file_name, 0))
            labels.append(int(code))
        rs.train(photos, labels)
    else:
        print("Error >> 员工照片文件丢失， 请重新启动程序并录入员工信息!")


def load_work_time_config():
    file = open(WORK_TIME, "r", encoding="utf-8")
    text = file.read().rstrip()
    times = text.split("/")
    o.WORK_TIME = times[0]
    o.CLOSING_TIME = times[1]
    file.close()


def load_users():
    file = open(USER_PASSWORD, "r", encoding="utf-8")
    text = file.read()
    if len(text) > 0:
        o.USERS = eval(text)
    file.close()


def save_employee_all():
    file = open(DATA_FILE, "w", encoding="utf-8")
    info = ""
    for emp in o.EMPLOYEES:
        info += str(emp.id) + "," + str(emp.name) + "," + str(emp.code) + "\n"
    file.write(info)
    file.close()


def save_lock_record():
    file = open(RECORD_FILE, "w", encoding="utf-8")
    info = str(o.LOCK_RECORD)
    file.write(info)
    file.close()


def save_work_time_config():
    file = open(WORK_TIME, "w", encoding="utf-8")
    times = str(o.WORK_TIME) + "/" + str(o.CLOSING_TIME)
    file.write(times)
    file.close()


def remove_pics(id):
    pics = os.listdir(PIC_PATH)
    code = str(hr.get_code_with_id(id))
    for file_name in pics:
        if file_name.startswith(code):
            os.remove(PIC_PATH + file_name)
            print("删除照片：" + file_name)


def create_CSV(file_name, text):
    file = open(PATH + file_name + ".csv", "w", encoding="gdk")
    file.write("text")
    file.close()
    print("已生成文件，请注意查看：" + PATH + file_name + ".csv")
