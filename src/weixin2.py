#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

import subprocess
import dht11
from sensor import pi_info

from smbus import SMBus
bus = SMBus(1)

import json
import werobot
from werobot.client import Client
robot = werobot.WeRoBot(token='wechatpi', enable_session=True) 

from wechat_sdk import WechatExt
wechat = WechatExt(username='2205955115@qq.com', password='liqing123')

# 获取与最新一条消息用户的对话内容
def get_user_info():
    user_info_json = wechat.get_top_message()
    user_info = json.loads(user_info_json)
    print wechat.get_dialog_message(fakeid=user_info['msg_item'][0]['fakeid'])

# 主动发送消息
def send_msg():
    user_info_json = wechat.get_top_message()
    user_info = json.loads(user_info_json)
    wechat.send_message(user_info['msg_item'][0]['fakeid'], "成功啦！")

err_msg = "出错啦，请重试！"

def get_sensor_data():
    # Reading data back
    output = subprocess.check_output("tail ./data/sensor.log -n 1", shell = True)
    sensor_data = eval(output)
    print "data:", sensor_data
    return sensor_data

@robot.subscribe
def subscribe():
    return "Hello! 这是我的毕设：Pi的呼吸之旅"

@robot.text
def first(message, session):
    if 'last' not in session:
        session['last'] = message.content
        return "这是你第一次跟我说话"
    else:
        return message.content

@robot.filter("报警")
def warning():
    send_msg()
    return "报警啦！"

@robot.key_click("PI_INFO")
def get_Pi_info():
    CPU_temp = pi_info.get_CPU_temp()
    GPU_temp = pi_info.get_GPU_temp()
    CPU_usage = pi_info.get_CPU_use()
    RAM_usage = pi_info.get_RAM_use()
    DISK_percent = pi_info.get_Disk_info()[3]
    return '''
    CPU温度:{0} °C
    GPU温度:{1} °C
    CPU使用率:{2} %
    RAM使用率:{3} %
    硬盘使用率:{4}
    '''.format(CPU_temp, GPU_temp, CPU_usage, RAM_usage, DISK_percent)

@robot.key_click("TEMP")
def get_air_hum():
    sensor_data = get_sensor_data()
    if (sensor_data):
        return "室内温度:{0:.2f} °C".format(float(sensor_data['temp']))
    else:
        return err_msg

@robot.key_click("HUM")
def get_air_hum():
    sensor_data = get_sensor_data()
    if (sensor_data):
        return "室内湿度:{0:.2f} %".format(float(sensor_data['hum']))
    else:
        return err_msg

@robot.key_click("LIGHT")
def get_air_hum():
    #得到光照强度
    bus.write_byte(0x48, 1) # set control register to read channel 1
    light = bus.read_byte(0x48) # read A/D
    if (light):
        return "光照强度:{0:.2f} 勒克斯".format(1080 - float(light))
    else:
        return err_msg

@robot.key_click("SWITCH")
def switch():
    return "open/close"

@robot.key_click("PM2.5")
def switch():
    sensor_data = get_sensor_data()
    # 3000 + = 很差
    # 1050-3000 = 差
    # 300-1050 = 一般
    # 150-300 = 好
    # 75-150 = 很好
    # 0-75 = 非常好
    PM_data = float(sensor_data['PM2_5'])
    if (PM_data > 3000):
        air_index = "很差"
    elif (PM_data > 1050):
        air_index = "差"
    elif (PM_data > 300):
        air_index = "一般"
    elif (PM_data > 150):
        air_index = "好"
    elif (PM_data > 75):
        air_index = "很好"
    else:
        air_index = "非常好"
    if (sensor_data):
        return "粉尘浓度：{0} ug/m3\n空气指数：{1} {2}".format(float(sensor_data['pm2.5']), float(sensor_data['PM2_5']), air_index)
    else:
        return err_msg

@robot.key_click("CO_GAS")
def switch():
    sensor_data = get_sensor_data()
    if (sensor_data):
        return "液化气浓度：{0} ppm".format(float(sensor_data['MQ-2']))
    else:
        return err_msg

@robot.key_click("SMOKE")
def switch():
    sensor_data = get_sensor_data()
    if (sensor_data):
        return "烟雾浓度：{0} ppm".format(float(sensor_data['MQ-5']))
    else:
        return err_msg

@robot.click
def click_event():
    return "我还没有准备好！"

# Reading menu data back
with open('./data/menu.json', 'r') as f:
    menu_data = json.load(f)

client = Client("wx6eff06f20136ac85", "f2cafa0e5900a415e812ac2ef557d0f6")
client.create_menu(menu_data)

robot.run(host='0.0.0.0', port=8889)



