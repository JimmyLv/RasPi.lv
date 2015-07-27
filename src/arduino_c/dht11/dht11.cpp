//    FILE: dht11.cpp
// VERSION: 0.4.1
// PURPOSE: DHT11 Temperature & Humidity Sensor library for Arduino
// LICENSE: GPL v3 (http://www.gnu.org/licenses/gpl.html)
//
// DATASHEET: http://www.micro4you.com/files/sensor/DHT11.pdf
//
// HISTORY:
// George Hadjikyriacou - Original version (??)
// Mod by SimKard - Version 0.2 (24/11/2010)
// Mod by Rob Tillaart - Version 0.3 (28/03/2011)
// + added comments
// + removed all non DHT11 specific code
// + added references
// Mod by Rob Tillaart - Version 0.4 (17/03/2012)
// + added 1.0 support
// Mod by Rob Tillaart - Version 0.4.1 (19/05/2012)
// + added error codes
//

#include "dht11.h"

// 此函数读取温度值，并且返回对应的读取状态：
// DHTLIB_OK
// DHTLIB_ERROR_CHECKSUM
// DHTLIB_ERROR_TIMEOUT
int dht11::read(int pin)
{
	uint8_t bits[5]; //存储读取的数据
	uint8_t cnt = 7; //计数器
	uint8_t idx = 0;

    //初始化数组为0
	for (int i=0; i< 5; i++) bits[i] = 0;

    //发送开始信号
	pinMode(pin, OUTPUT);//设置为输出
	digitalWrite(pin, LOW);//保持低电平至少18ms
	delay(18);
	digitalWrite(pin, HIGH);//保持高电平20-40us
	delayMicroseconds(40);
	//开始接受dht响应信号
	pinMode(pin, INPUT);//设置为输入

	unsigned int loopCnt = 10000;
	while(digitalRead(pin) == LOW)
		if (loopCnt-- == 0) return DHTLIB_ERROR_TIMEOUT;

	loopCnt = 10000;
	while(digitalRead(pin) == HIGH)
		if (loopCnt-- == 0) return DHTLIB_ERROR_TIMEOUT;

	// READ OUTPUT - 40 BITS => 5 BYTES or TIMEOUT
	//开始等待温度传感器回应（根据数据手册温度传感器回应时会拉低数据线）
	for (int i=0; i<40; i++)
	{
		//如果此时的电平和当前电平相等说明电平没有发生变化，所以继续等下一次循环
		loopCnt = 10000;
		while(digitalRead(pin) == LOW)
			if (loopCnt-- == 0) return DHTLIB_ERROR_TIMEOUT;

		unsigned long t = micros();

		loopCnt = 10000;
		while(digitalRead(pin) == HIGH)
			if (loopCnt-- == 0) return DHTLIB_ERROR_TIMEOUT;

		if ((micros() - t) > 40) bits[idx] |= (1 << cnt);//左移一位并且将数据1写入（此时最后一位为0）
		if (cnt == 0)   // 是否为下一个字节
		{
			cnt = 7;    // restart at MSB
			idx++;      // 下一个字节
		}
		else cnt--;
	}
    /*
    开始处理数据

    1.因为一次完整的数据输出为40位，所以j应大于40
    2.dht11_val[4]为校验和，此处判断校验和是否正确
    3.只打印dht11_val[0], dht11_val[2]是因为dht11_val[1], dht11_val[3]是小数部分，根据数据手册小数始终为零
    */
	// 写入正确的数据
    // 由于bits[1]和bits[3]总是0，所以就省略格式了
	humidity    = bits[0]; 
	temperature = bits[2]; 

	uint8_t sum = bits[0] + bits[2];  
	//校验正确，返回正确的状态码
	if (bits[4] != sum) return DHTLIB_ERROR_CHECKSUM;
	return DHTLIB_OK;
}
//
// END OF FILE
//
