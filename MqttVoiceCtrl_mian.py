# encoding: utf-8
# Author: CSUST-刘志成、龙子鑫
# Date:2019/11/17
# Version:1.0

from MqttFunPart import mqtt_init, mqtt_publish
from VoiceFunPart import Voice_init, Speech2Text, Text2Speech

# analog value
value1 = 0


# 指令检索并执行相应命令
def speakDo(text):
    global value1

    # 语音指令解析映射列表组成的字典
    maps = {
        '打开一号灯': ['打开一号灯', 'open the red light', 'turn on the red light'],
        '关闭一号灯': ['关闭一号灯', 'close the red light', 'turn off the red light'],
        '打开二号灯': ['打开二号灯', 'open the green light', 'turn on the green light'],
        '关闭二号灯': ['关闭二号灯', 'close the green light', 'turn off the green light'],
        '打开三号灯': ['打开三号灯', '打开三号登', 'open the blue light', 'turn on the blue light'],
        '关闭三号灯': ['关闭三号灯', 'close the blue light', 'turn off the blue light'],
        '增加二十': ['增加二十', 'add twenty'],
        '减少二十': ['减少二十', 'reduce twenty'],
        '退出': ['退出', 'shutdown', 'exit']

    }

    if text in maps['打开一号灯']:
        mqtt_publish(topic='life', payload='ON1')
        Text2Speech(100,"一号灯已开启")
        print("一号灯已开启")
        #　webbrowser.open_new_tab('https://www.qq.com')
    elif text in maps['关闭一号灯']:
        mqtt_publish(topic='life', payload='OFF1')
        Text2Speech(100, "一号灯已关闭")
        print("一号灯已关闭")
        # webbrowser.open_new_tab('https://www.qq.com')
    elif text in maps['打开二号灯']:
        mqtt_publish(topic='life', payload='ON2')
        Text2Speech(100, "二号灯已开启")
        print("二号灯已开启")
        #　webbrowser.open_new_tab('https://www.163.com/')
    elif text in maps['关闭二号灯']:
        mqtt_publish(topic='life', payload='OFF2')
        Text2Speech(100, "二号灯已关闭")
        print("二号灯已关闭")
        #　webbrowser.open_new_tab('https://www.163.com/')
    elif text in maps['打开三号灯']:
        mqtt_publish(topic='life', payload='ON3')
        Text2Speech(100, "三号灯已开启")
        print("三号灯已开启")
    # 　webbrowser.open_new_tab('https://www.163.com/')
    elif text in maps['关闭三号灯']:
        mqtt_publish(topic='life', payload='OFF3')
        Text2Speech(100, "三号灯已关闭")
        print("三号灯已关闭")
    # 　webbrowser.open_new_tab('https://www.163.com/')
    elif text in maps['增加二十']:
        value1 += 20
        mqtt_publish(topic='lifeack', payload=str(value1))
        Text2Speech(100, '已加到' + str(value1))
        print(value1)
    # 　webbrowser.open_new_tab('https://www.163.com/')
    elif text in maps['减少二十']:
        value1 -= 20
        mqtt_publish(topic='lifeack', payload=str(value1))
        Text2Speech(100, '已减到' + str(value1))
        print(value1)
    # 　webbrowser.open_new_tab('https://www.163.com/')
    else:
        Text2Speech(100, text="Please say again !")
        print("Please say again !")
        #　webbrowser.open_new_tab('https://www.baidu.com/s?wd=%s' % text)


if __name__ == '__main__':
    # Mqtt客户端，Voice引擎初始化
    mqtt_init()
    Voice_init()

    # 设备启动欢迎语
    Text2Speech(rate=130, text="Welcome to SmartHome")

    while input('Continue?(y/n):') == '':   # 等待回输入：无输入回车键车键继续识别，其他任意键退出
        Text2Speech(rate=120, text='请说出指令')
        # 1536：普通话(简单英文)
        # 1537:普通话(有标点)
        # 1737:英语
        # 1637:粤语
        # 1837:四川话
        result = Speech2Text(1536)  # 语音解析并返回结果
        print(result)   # 打印输出结果
        if type(result) == str:     # 判断是否有
            speakDo(result.strip('，'))  # 数据逗号分隔提取
        else:
            Text2Speech(rate=120, text='未识别，请大点声！')
