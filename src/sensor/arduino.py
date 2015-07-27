#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

import serial
import time
import json

from wechat_sdk import WechatExt
wechat = WechatExt(username='lv460051518@gmail.com', password='liqing123')

def cal_vol(voMeasured):
    voMeasured = float(voMeasured)
    # 0 - 5V mapped to 0 - 1023 integer values
    # recover voltage
    cal_voltage = voMeasured * (5.0 / 1024.0)   #将模拟值转换为电压值
    return cal_voltage

def cal_den(cal_voltage):
    cal_voltage = float(cal_voltage)
    # linear eqaution taken from http:#www.howmuchsnow.com/arduino/airquality/
    # Chris Nafis (c) 2012
    dust_density = 0.17 * cal_voltage - 0.1      #将电压值转换为粉尘密度输出单位
    return float("%.6f"%(dust_density))  # 输出单位: 毫克/立方米

def cal_air_index(cal_voltage):
    air_index = (float(cal_voltage*5.0)-0.0356)*120000*0.035
    return air_index

# 主动发送消息
def send_msg(msg="成功啦！"):
    user_info_json = wechat.get_top_message()
    user_info = json.loads(user_info_json)
    print "*"*20 + "报警啦！" + "*"*20
    try:
        wechat.send_message(user_info['msg_item'][0]['fakeid'], msg)
    except:
        print 'ERROR! No more user!'

port = '/dev/ttyUSB0'
def main(port):
    arduino = serial.Serial(port,9600,timeout=1)
    time.sleep(1.5)
    while (True):
        arduino.write("Everything is OK!")
        print ("Message from arduino: ")

        msg = arduino.readline().strip('\n\r') #arduino.read(arduino.inWaiting()).strip('\n\r') 
        print msg
        
        try:
            key = ['pm2.5', 'MQ-2', 'MQ-5', "hum", "temp", "PM2_5"]
            value = msg.split('-')
            data = dict(zip(key,value))
            pm2_5 = data['pm2.5']
            print "MQ-5 - MQ-2 = {0}".format(int(data['MQ-5']) - int(data['MQ-2']))
            voltage = cal_vol(pm2_5)
            dust_density = cal_den(voltage)
            print "PM2_5:{0}, vol:{1} V, den:{2} mg/m3, index:{3}".format(pm2_5, voltage, dust_density, data['PM2_5'])
            data["pm2.5"] = dust_density
            print data
        except:
            print 'ERROR!'

        with open('../data/sensor.log', 'a') as f:
            if (len(data) == 6):
                f.write(str(data) + '\n')
                print "write success!"
                pm = data['pm2.5']
                mq2 = data['MQ-2']
                mq5 = data['MQ-5']
                if (float(mq2) > 40 or float(mq5) > 90):
                    warning_msg = "PM2.5浓度: {0}ug/m3,\n一氧化碳: {1}ppm, 烟雾浓度: {2}ppm".format(pm, mq2, mq5)
                    send_msg("家中险情！请立即采取措施！\n" + warning_msg)
                    print warning_msg
            else:
                print "[ERROR:] write error!"

        print "*"*40
        time.sleep(3)
    else:
        print "Exiting"
    exit()

if __name__ == '__main__':
    try:
        main(sys.argv[1] if len(sys.argv) > 1 else port )
    except KeyboardInterrupt:
        ser.close()