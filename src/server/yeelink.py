#coding=utf-8
import time
import json
import requests
import subprocess

from smbus import SMBus
bus = SMBus(1)

#yeelink api配置
api_url='http://api.yeelink.net/v1.1'
api_key='64a20e273bf186e50b2cd30b936743dd' #请填入专属的api key
api_headers={'U-ApiKey':api_key,'content-type': 'application/json'}
raspi_device_id = 20814
cpu_sensor_id = 36496
air_temp_sensor_id = 41044
air_hum_sensor_id = 41045
pm_sensor_id = 41047
mq2_sensor_id = 41048
mq5_sensor_id = 41049
light_sensor_id = 41046

#得到光照强度
def read_light():
    bus.write_byte(0x48, 1) # set control register to read channel 1
    light = bus.read_byte(0x48) # read A/D
    return light

#得到CPU温度
def get_cpu_temp():
    cpu_temp_file = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = cpu_temp_file.read()
    cpu_temp_file.close()
    return float(cpu_temp)/1000

#上传到yeelink
def upload_to_yeelink(sensor_value, sensor_id):
    url=r'%s/device/%s/sensor/%s/datapoints' % (api_url,raspi_device_id,sensor_id)

    strftime=time.strftime("%Y-%m-%dT%H:%M:%S")

    data={"timestamp":strftime , "value": sensor_value}
    res=requests.post(url,headers=api_headers,data=json.dumps(data))
    print "status_code:",res.status_code


def main():
    while True:    
        cpu_temp=get_cpu_temp()
        print "cpu_temp:",cpu_temp
        upload_to_yeelink(cpu_temp, cpu_sensor_id)

        strftime=time.strftime("%Y-%m-%dT%H:%M:%S")
        print "time:",strftime

        # Reading data back
        output = subprocess.check_output("tail ../data/sensor.log -n 1", shell = True)
        sensor_data = eval(output)
        print "data:", sensor_data

        air_temp = sensor_data["temp"]
        print "air_temp:",air_temp
        upload_to_yeelink(air_temp, air_temp_sensor_id)

        air_hum = sensor_data["hum"]
        print "air_hum:",air_hum
        upload_to_yeelink(air_hum, air_hum_sensor_id)

        pm = sensor_data["PM2_5"]
        print "air_pm2.5:",pm
        upload_to_yeelink(pm, pm_sensor_id)

        mq2 = sensor_data["MQ-2"]
        print "MQ-2:",mq2
        upload_to_yeelink(mq2, mq2_sensor_id)

        mq5 = sensor_data["MQ-5"]
        print "MQ-5:",mq5
        upload_to_yeelink(mq5, mq5_sensor_id)

        # light = read_light()
        # print "light:",light
        # upload_to_yeelink(light, 1080 - float(light_sensor_id))

        print "*"*40
        #休眠10秒
        time.sleep(10)

if __name__ == '__main__':  
    main()
