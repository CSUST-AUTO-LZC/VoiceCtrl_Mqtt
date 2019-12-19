# encoding: utf-8
import flask
import pyttsx3
import wave
import requests
import time
import base64
from pyaudio import PyAudio, paInt16
import paho.mqtt.client as mqtt


value1 = 0;


framerate = 16000  # 采样率
num_samples = 2000  # 采样点
channels = 1  # 声道
sampwidth = 2  # 采样宽度2bytes
FILEPATH = './AudioResource/speech.wav'

base_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
APIKey = "BPKhT3GsnDvbbWrwCHsazq9Z"
SecretKey = "RLa7VaS7t4qsHd5O1GialxxSVXFPn15X"

HOST = base_url % (APIKey, SecretKey)


# 语音合成引擎初始化
engine = pyttsx3.init()


# 当连接上服务器后回调此函数
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # 放在on_connect函数里意味着
    # 重新连接时订阅主题将会被更新
    client.subscribe("life")


# 从服务器接受到消息后回调此函数
def on_message(client, userdata, msg):
    print("主题:" + msg.topic + " 消息:" + str(msg.payload))


def getToken(host):
    res = requests.post(host)
    return res.json()['access_token']


def save_wave_file(filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))
    wf.close()


def my_record():
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=channels,
                     rate=framerate, input=True, frames_per_buffer=num_samples)
    my_buf = []
    # count = 0
    t = time.time()
    print('正在录音...')

    while time.time() < t + 3:  # 秒
        string_audio_data = stream.read(num_samples)
        my_buf.append(string_audio_data)
    print('录音结束.')
    save_wave_file(FILEPATH, my_buf)
    #保存到音频文件
    stream.close()


def get_audio(file):
    with open(file, 'rb') as f:
        data = f.read()
    return data


def speech2text(speech_data, token, dev_pid=1537):
    FORMAT = 'wav'
    RATE = '16000'
    CHANNEL = 1
    CUID = '*******'
    SPEECH = base64.b64encode(speech_data).decode('utf-8')

    data = {
        'format': FORMAT,
        'rate': RATE,
        'channel': CHANNEL,
        'cuid': CUID,
        'len': len(speech_data),
        'speech': SPEECH,
        'token': token,
        'dev_pid': dev_pid
    }
    url = 'https://vop.baidu.com/server_api'
    headers = {'Content-Type': 'application/json'}
    # r=requests.post(url,data=json.dumps(data),headers=headers)
    print('正在识别...')
    r = requests.post(url, json=data, headers=headers)
    Result = r.json()
    if 'result' in Result:
        return Result['result'][0]
    else:
        return Result


# 指令检索并执行相应命令
def speakDo(text):
    global value1
    maps = {
        '打开一号灯': ['打开一号灯', 'open the red light', 'turn on the red light'],
        '关闭一号灯': ['关闭一号灯', 'close the red light', 'turn off the red light'],
        '打开二号灯': ['打开二号灯', 'open the green light', 'turn on the green light'],
        '关闭二号灯': ['关闭二号灯', 'close the green light', 'turn off the green light'],
        '打开三号灯': ['打开三号灯', 'open the blue light', 'turn on the blue light'],
        '关闭三号灯': ['关闭三号灯', 'close the blue light', 'turn off the blue light'],
        '增加二十': ['增加二十', 'add twenty'],
        '退出': ['退出', 'shutdown', 'exit']

    }
    if text in maps['打开一号灯']:
        client.publish(topic='life', payload='ON1', qos=0, retain=False, properties=None)
        engine.setProperty('rate', 100)
        engine.say("一号灯已开启")
        engine.runAndWait()
        print("一号灯已开启")
        #　webbrowser.open_new_tab('https://www.qq.com')
    elif text in maps['关闭一号灯']:
        client.publish(topic='life', payload='OFF1', qos=0, retain=False, properties=None)
        engine.setProperty('rate', 100)
        engine.say("一号灯已关闭")
        engine.runAndWait()
        print("一号灯已关闭")
        #　webbrowser.open_new_tab('https://www.qq.com')
    elif text in maps['打开二号灯']:
        client.publish(topic='life', payload='ON2', qos=0, retain=False, properties=None)
        engine.setProperty('rate', 100)
        engine.say("二号灯已开启")
        engine.runAndWait()
        print("二号灯已开启")
        #　webbrowser.open_new_tab('https://www.163.com/')
    elif text in maps['关闭二号灯']:
        client.publish(topic='life', payload='OFF2', qos=0, retain=False, properties=None)
        engine.setProperty('rate', 100)
        engine.say("二号灯已关闭")
        engine.runAndWait()
        print("二号灯已关闭")
        #　webbrowser.open_new_tab('https://www.163.com/')
    elif text in maps['打开三号灯']:
        client.publish(topic='life', payload='ON3', qos=0, retain=False, properties=None)
        engine.setProperty('rate', 100)
        engine.say("三号灯已开启")
        engine.runAndWait()
        print("三号灯已开启")
    # 　webbrowser.open_new_tab('https://www.163.com/')
    elif text in maps['关闭三号灯']:
        client.publish(topic='life', payload='OFF3', qos=0, retain=False, properties=None)
        engine.setProperty('rate', 100)
        engine.say("三号灯已关闭")
        engine.runAndWait()
        print("三号灯已关闭")
    # 　webbrowser.open_new_tab('https://www.163.com/')
    elif text in maps['增加二十']:
        value1 += 20
        client.publish(topic='lifeack', payload=str(value1), qos=0, retain=False, properties=None)
        engine.setProperty('rate', 100)
        engine.say('加' + str(value1))
        engine.runAndWait()
        print(value1)
    # 　webbrowser.open_new_tab('https://www.163.com/')
    else:
        engine.setProperty('rate', 100)
        engine.say("Please say again !")
        engine.runAndWait()
        print("Please say again !")
        #　webbrowser.open_new_tab('https://www.baidu.com/s?wd=%s' % text)


client = mqtt.Client(client_id="FlaskServer", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
# 参数有 Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
client.on_connect = on_connect  # 设置连接上服务器回调函数
client.on_message = on_message  # 设置接收到服务器消息回调函数
client.connect("csustauto.xyz", 1883, 60)  # 连接服务器,端口为1883,维持心跳为60秒

# # 往主题chat里发送消息
# a = input("please input a key......")
# client.publish(topic='life', payload='ON1')
# a = input("please input a key......")
# client.publish(topic='life', payload='ON1', qos=0, retain=False, properties=None)
# a = input("please input a key......")


if __name__ == '__main__':
    engine.setProperty('rate', 120)
    engine.say("Welcome to SmartHome two point zero")
    engine.runAndWait()
    while input('Continue?(y/n):') == 'y':
        engine.setProperty('rate', 100)
        engine.say('请说出指令')
        engine.runAndWait()
        print('请输入数字选择语言：')
        devpid = 1536   # input('1536：普通话(简单英文),1537:普通话(有标点),1737:英语,1637:粤语,1837:四川话\n')
        my_record()
        TOKEN = getToken(HOST)
        speech = get_audio(FILEPATH)
        result = speech2text(speech, TOKEN, int(devpid))
        print(result)
        if type(result) == str:
            speakDo(result.strip('，'))
