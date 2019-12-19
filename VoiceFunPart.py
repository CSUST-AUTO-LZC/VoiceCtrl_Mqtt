import pyttsx3
import wave
import requests
import time
import base64
from pyaudio import PyAudio, paInt16


# 录音音频编码参数设定
FILEPATH = './AudioResource/speech.wav'
framerate = 16000  # 采样率
num_samples = 2000  # 采样点
channels = 1  # 声道
sampwidth = 2  # 采样宽度2bytes

# Baidu语音API-URL以及接入验证信息
base_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
APIKey = "BPKhT3GsnDvbbWrwCHsazq9Z"
SecretKey = "RLa7VaS7t4qsHd5O1GialxxSVXFPn15X"
HOST = base_url % (APIKey, SecretKey)
token = ''
engine = None   # 创建语音合成引擎空对象


def Voice_init():
    # 语音合成引擎初始化
    global engine, token  # 申明引用全局变量
    engine = pyttsx3.init()     #实例化语音合成引擎空对象
    res = requests.post(HOST)   #发出验证POST请求
    token = res.json()['access_token']  # 接收并获取API接入口令
    return True


def save_wave_file(filepath, data):
    # 配置音频格式参数并保存为WAV音频文件
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
    my_buf = []     # 音频缓冲存储列表
    # count = 0
    t = time.time()
    print('正在录音...')

    while time.time() < t + 3:  # 录取3秒
        string_audio_data = stream.read(num_samples)    # 从音频流中采样获取音频编码数据
        my_buf.append(string_audio_data)    # 数据缓存
    print('录音结束.')
    save_wave_file(FILEPATH, my_buf)    # 保存文件
    #保存到音频文件
    stream.close()      # 关闭音频流


def get_audio(file):
    # 以只读方式打开音频文档
    with open(file, 'rb') as f:
        data = f.read()
    return data


def Speech2Text(dev_pid=1537):
    # 1536：普通话(简单英文),1537:普通话(有标点),1737:英语,1637:粤语,1837:四川话
    global token

    my_record()     # 开始录音
    speech_data = get_audio(FILEPATH)

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


def Text2Speech(rate, text):
    engine.setProperty('rate', rate)    # 设定语音速率
    engine.setProperty('voice', 1)      # 设定语音模式
    engine.setProperty('volume', 8)     # 设定语音音量
    engine.say(text)    # 加载语音文字
    engine.runAndWait()     # 执行并等待语音播放完毕
