# -*-coding:utf-8 -*-

import os
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')

root = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(root, 'site-packages'))
sys.path.insert(1, os.path.join(root, 'lib/python2.7/site-packages'))

import werobot
from werobot.session.saekvstorage import SaeKVDBStorage
from werobot.client import Client

session_storage = SaeKVDBStorage()
robot = werobot.WeRoBot(token="oneplan", enable_session=True, session_storage=session_storage)


@robot.subscribe
@robot.text
def subscribe(message):
    return [
        "咱们结婚吧",
        '''Hello, Welcome!
My Beautiful Lover!''',
        "http://yinyueshiting.baidu.com/data2/music/134368631/1054947051423814461128.mp3?xcode=6b9fb1852b60d9063dc87741771c2450a43fdd49104df35e"
    ]


@robot.text
def first(message, session):
    if 'last' in session:
        return
    session['last'] = message.content
    return message.content


@robot.key_click("LOVE")
def love():
    return '''
    I Love You Very Much!
	Happy Valentine's Day!
	'''


@robot.key_click("NICE")
def nice():
    return '''
    Thanks! 
    Lovely Baby!
    Kisssssss....
	I Will Accompany You Forever!
	'''

@robot.key_click("MUSIC")
@robot.text
def music(message):
    return [
        "咱们结婚吧",
        "歌曲: 咱们结婚吧 演唱: 齐晨",
        "http://yinyueshiting.baidu.com/data2/music/134368631/1054947051423814461128.mp3?xcode=6b9fb1852b60d9063dc87741771c2450a43fdd49104df35e"
    ]



@robot.text
@robot.key_click("MOMENT")
def moment(message):
    return [
    	[
    		"Our First Day",
    		"This Moment that I will Remember Forever!",
    		"https://mmbiz.qlogo.cn/mmbiz/j3gm1jVss1wbcIEOP1BjFicLUFmueEujCBZERVhZEzT8mWSaIrMoYEMrhc3cQDJVlMA83miaBzyBLt48UZa0GCpA/0",
    		"http://www.ilovechenjia.tk/"
    	],
        [
            "Jiajia's Birthday",
            "HappyBirthday",
            "https://mmbiz.qlogo.cn/mmbiz/j3gm1jVss1wbcIEOP1BjFicLUFmueEujCemgOO8ch6hNxV9SegH0V3jhwE4dDTwYWp6Q33QKKDCCA7tnKsSKPtA/0",
            "http://betterbetterme.lofter.com/"
        ],
        [
            "Liqing's Birthday",
            "HappyBirthday",
            "https://mmbiz.qlogo.cn/mmbiz/j3gm1jVss1wbcIEOP1BjFicLUFmueEujCdo3w2vcsBv6fv4MjfCE84laaKiaQrsEDeDvc4sO2Dolgyo7YAmsNyDw/0",
            "http://unperfectlove.lofter.com/"
        ]
    ]



@robot.text
@robot.key_click("SNS")
def sns(message):
	return [
		[
			"Jiajia's WeiBo",
			"Jiajia's WeiBo",
			"https://mmbiz.qlogo.cn/mmbiz/j3gm1jVss1wbcIEOP1BjFicLUFmueEujCgVsyJ7U4lf2CYcsxHtia9Lia6CWU6ib2tMamvm6DoVDtPn5h0faEDE2Zw/0",
			"http://weibo.com/woaini3721"
		],
		[
			"Jiajia's Qzone",
			"Jiajia's Qzone",
			"https://mmbiz.qlogo.cn/mmbiz/j3gm1jVss1wbcIEOP1BjFicLUFmueEujCvrDdTRSCwKYHh8vaVv6ET1dMnF35XjbDRBcAodtPoCibJPajzxibGYNg/0",
			"http://user.qzone.qq.com/670045284"
		],
		[
			"Jiajia's RenRen",
			"Jiajia's RenRen",
			"https://mmbiz.qlogo.cn/mmbiz/j3gm1jVss1wbcIEOP1BjFicLUFmueEujCSiaJxqmLYNd5zmdhzZWzuEDM6TFb1qtlNVkO5YCdGcrAN0iaDkianLjuA/0",
			"http://www.renren.com/431744788/profile"
		]

	]


client = Client("wx6eff06f20136ac85", "f2cafa0e5900a415e812ac2ef557d0f6")
client.create_menu({
    "button": [
        {
            "type": "view",
            "name": "Valentine",
            "url": "http://create.maka.im/k/1FG29JLU"
        },
        {
            "type": "view",
            "name": "Beautiful",
            "url": "http://create.maka.im/k/EQ52YHUW"
        },
        {
            "name": "More",
            "sub_button": [
                {
                    "type": "click",
                    "name": "Life",
                    "key": "SNS"
                },
                {
                    "type": "click",
                    "name": "Moment",
                    "key": "MOMENT"
                },
                {
                    "type": "click",
                    "name": "Music",
                    "key": "MUSIC"
                },
                {
                    "type": "click",
                    "name": "Kiss Me",
                    "key": "NICE"
                }
            ]
        }
    ]})
